import ast

from hugr.serialization import ops, tys
from pydantic import BaseModel

from guppylang.ast_util import AstNode, get_type, with_loc
from guppylang.checker.core import Context
from guppylang.checker.expr_checker import (
    ExprSynthesizer,
    check_call,
    check_num_args,
    check_type_against,
    synthesize_call,
)
from guppylang.definition.custom import (
    CustomCallChecker,
    CustomCallCompiler,
    CustomFunctionDef,
    DefaultCallChecker,
)
from guppylang.definition.value import CallableDef
from guppylang.error import GuppyError, GuppyTypeError, InternalGuppyError
from guppylang.hugr_builder.hugr import UNDEFINED, OutPortV
from guppylang.nodes import GlobalCall, ResultExpr
from guppylang.tys.arg import ConstArg, TypeArg
from guppylang.tys.builtin import (
    bool_type,
    int_type,
    is_array_type,
    is_bool_type,
    list_type,
)
from guppylang.tys.const import Const, ConstValue
from guppylang.tys.subst import Inst, Subst
from guppylang.tys.ty import (
    FunctionType,
    NoneType,
    NumericType,
    Type,
    type_to_row,
    unify,
)


class ConstInt(BaseModel):
    """Hugr representation of signed and unsigned integers in the arithmetic extension.

    Hugr always uses a u64 for the value. The interpretation is:
      - as an unsigned integer, (value mod `2^N`);
      - as a signed integer, (value mod `2^(N-1) - 2^(N-1)*a`)
    where `N = 2^log_width` and `a` is the (N-1)th bit of `x` (counting from 0 = least
    significant bit).
    """

    log_width: int
    value: int


class ConstF64(BaseModel):
    """Hugr representation of float values."""

    value: float


def bool_value(b: bool) -> ops.Value:
    """Returns the Hugr representation of a boolean value."""
    return ops.Value(
        ops.SumValue(tag=int(b), typ=tys.SumType(tys.UnitSum(size=2)), vs=[])
    )


def int_value(i: int) -> ops.Value:
    """Returns the Hugr representation of an integer value."""
    return ops.Value(
        ops.ExtensionValue(
            extensions=["arithmetic.int.types"],
            typ=NumericType(NumericType.Kind.Int).to_hugr(),
            value=ops.CustomConst(
                c="ConstInt", v=ConstInt(log_width=NumericType.INT_WIDTH, value=i)
            ),
        )
    )


def float_value(f: float) -> ops.Value:
    """Returns the Hugr representation of a float value."""
    return ops.Value(
        ops.ExtensionValue(
            extensions=["arithmetic.float.types"],
            typ=NumericType(NumericType.Kind.Float).to_hugr(),
            value=ops.CustomConst(c="ConstF64", v=ConstF64(value=f)),
        )
    )


def list_value(v: list[ops.Value], ty: Type) -> ops.Value:
    """Returns the Hugr representation of a list value."""
    return ops.Value(
        ops.ExtensionValue(
            extensions=["Collections"],
            typ=list_type(ty).to_hugr(),
            value=ops.CustomConst(c="ListValue", v=(v, ty.to_hugr())),
        )
    )


def logic_op(op_name: str, args: list[tys.TypeArg] | None = None) -> ops.OpType:
    """Utility method to create Hugr logic ops."""
    return ops.OpType(
        ops.CustomOp(extension="logic", name=op_name, args=args or [], parent=UNDEFINED)
    )


def int_op(
    op_name: str,
    ext: str = "arithmetic.int",
    args: list[tys.TypeArg] | None = None,
    num_params: int = 1,
) -> ops.OpType:
    """Utility method to create Hugr integer arithmetic ops."""
    if args is None:
        args = num_params * [tys.TypeArg(tys.BoundedNatArg(n=NumericType.INT_WIDTH))]
    return ops.OpType(
        ops.CustomOp(extension=ext, name=op_name, args=args, parent=UNDEFINED)
    )


def float_op(op_name: str, ext: str = "arithmetic.float") -> ops.OpType:
    """Utility method to create Hugr integer arithmetic ops."""
    return ops.OpType(
        ops.CustomOp(extension=ext, name=op_name, args=[], parent=UNDEFINED)
    )


class CoercingChecker(DefaultCallChecker):
    """Function call type checker that automatically coerces arguments to float."""

    def synthesize(self, args: list[ast.expr]) -> tuple[ast.expr, Type]:
        for i in range(len(args)):
            args[i], ty = ExprSynthesizer(self.ctx).synthesize(args[i])
            if isinstance(ty, NumericType) and ty.kind != NumericType.Kind.Float:
                to_float = self.ctx.globals.get_instance_func(ty, "__float__")
                assert to_float is not None
                args[i], _ = to_float.synthesize_call([args[i]], self.node, self.ctx)
        return super().synthesize(args)


class ReversingChecker(CustomCallChecker):
    """Call checker that reverses the arguments after checking."""

    base_checker: CustomCallChecker

    def __init__(self, base_checker: CustomCallChecker | None = None):
        self.base_checker = base_checker or DefaultCallChecker()

    def _setup(self, ctx: Context, node: AstNode, func: CustomFunctionDef) -> None:
        super()._setup(ctx, node, func)
        self.base_checker._setup(ctx, node, func)

    def check(self, args: list[ast.expr], ty: Type) -> tuple[ast.expr, Subst]:
        expr, subst = self.base_checker.check(args, ty)
        if isinstance(expr, GlobalCall):
            expr.args = list(reversed(args))
        return expr, subst

    def synthesize(self, args: list[ast.expr]) -> tuple[ast.expr, Type]:
        expr, ty = self.base_checker.synthesize(args)
        if isinstance(expr, GlobalCall):
            expr.args = list(reversed(args))
        return expr, ty


class FailingChecker(CustomCallChecker):
    """Call checker for Python functions that are not available in Guppy.

    Gives the uses a nicer error message when they try to use an unsupported feature.
    """

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def synthesize(self, args: list[ast.expr]) -> tuple[ast.expr, Type]:
        raise GuppyError(self.msg, self.node)

    def check(self, args: list[ast.expr], ty: Type) -> tuple[ast.expr, Subst]:
        raise GuppyError(self.msg, self.node)


class UnsupportedChecker(CustomCallChecker):
    """Call checker for Python builtin functions that are not available in Guppy.

    Gives the uses a nicer error message when they try to use an unsupported feature.
    """

    def synthesize(self, args: list[ast.expr]) -> tuple[ast.expr, Type]:
        raise GuppyError(
            f"Builtin method `{self.func.name}` is not supported by Guppy", self.node
        )

    def check(self, args: list[ast.expr], ty: Type) -> tuple[ast.expr, Subst]:
        raise GuppyError(
            f"Builtin method `{self.func.name}` is not supported by Guppy", self.node
        )


class DunderChecker(CustomCallChecker):
    """Call checker for builtin functions that call out to dunder instance methods"""

    dunder_name: str
    num_args: int

    def __init__(self, dunder_name: str, num_args: int = 1):
        assert num_args > 0
        self.dunder_name = dunder_name
        self.num_args = num_args

    def _get_func(self, args: list[ast.expr]) -> tuple[list[ast.expr], CallableDef]:
        check_num_args(self.num_args, len(args), self.node)
        fst, *rest = args
        fst, ty = ExprSynthesizer(self.ctx).synthesize(fst)
        func = self.ctx.globals.get_instance_func(ty, self.dunder_name)
        if func is None:
            raise GuppyTypeError(
                f"Builtin function `{self.func.name}` is not defined for argument of "
                f"type `{ty}`",
                self.node.args[0] if isinstance(self.node, ast.Call) else self.node,
            )
        return [fst, *rest], func

    def synthesize(self, args: list[ast.expr]) -> tuple[ast.expr, Type]:
        args, func = self._get_func(args)
        return func.synthesize_call(args, self.node, self.ctx)

    def check(self, args: list[ast.expr], ty: Type) -> tuple[ast.expr, Subst]:
        args, func = self._get_func(args)
        return func.check_call(args, ty, self.node, self.ctx)


class CallableChecker(CustomCallChecker):
    """Call checker for the builtin `callable` function"""

    def synthesize(self, args: list[ast.expr]) -> tuple[ast.expr, Type]:
        check_num_args(1, len(args), self.node)
        [arg] = args
        arg, ty = ExprSynthesizer(self.ctx).synthesize(arg)
        is_callable = (
            isinstance(ty, FunctionType)
            or self.ctx.globals.get_instance_func(ty, "__call__") is not None
        )
        const = with_loc(self.node, ast.Constant(value=is_callable))
        return const, bool_type()

    def check(self, args: list[ast.expr], ty: Type) -> tuple[ast.expr, Subst]:
        args, _ = self.synthesize(args)
        subst = unify(ty, bool_type(), {})
        if subst is None:
            raise GuppyTypeError(
                f"Expected expression of type `{ty}`, got `bool`", self.node
            )
        return args, subst


class ArrayLenChecker(CustomCallChecker):
    """Function call checker for the `array.__len__` function."""

    @staticmethod
    def _get_const_len(inst: Inst) -> ast.expr:
        """Helper function to extract the static length from the inferred type args."""
        # TODO: This will stop working once we allow generic function defs. Then, the
        #  argument could also just be variable instead of a concrete number.
        match inst:
            case [_, ConstArg(const=ConstValue(value=int(n)))]:
                return ast.Constant(value=n)
        raise InternalGuppyError(f"array.__len__: Invalid instantiation: {inst}")

    def synthesize(self, args: list[ast.expr]) -> tuple[ast.expr, Type]:
        _, _, inst = synthesize_call(self.func.ty, args, self.node, self.ctx)
        return self._get_const_len(inst), int_type()

    def check(self, args: list[ast.expr], ty: Type) -> tuple[ast.expr, Subst]:
        _, subst, inst = check_call(self.func.ty, args, ty, self.node, self.ctx)
        return self._get_const_len(inst), subst


class ResultChecker(CustomCallChecker):
    """Call checker for the `result` function."""

    def synthesize(self, args: list[ast.expr]) -> tuple[ast.expr, Type]:
        check_num_args(2, len(args), self.node)
        [tag, value] = args
        if not isinstance(tag, ast.Constant) or not isinstance(tag.value, str):
            raise GuppyTypeError("Expected a string literal", tag)
        value, ty = ExprSynthesizer(self.ctx).synthesize(value)
        # We only allow numeric values or vectors of numeric values
        err = (
            f"Expression of type `{ty}` is not a valid result. Only numeric values or "
            "arrays thereof are allowed."
        )
        if self._is_numeric_or_bool_type(ty):
            base_ty = ty
            array_len: Const | None = None
        elif is_array_type(ty):
            [ty_arg, len_arg] = ty.args
            assert isinstance(ty_arg, TypeArg)
            assert isinstance(len_arg, ConstArg)
            if not self._is_numeric_or_bool_type(ty_arg.ty):
                raise GuppyError(err, value)
            base_ty = ty_arg.ty
            array_len = len_arg.const
        else:
            raise GuppyError(err, value)
        node = ResultExpr(value, base_ty, array_len, tag.value)
        return with_loc(self.node, node), NoneType()

    def check(self, args: list[ast.expr], ty: Type) -> tuple[ast.expr, Subst]:
        expr, res_ty = self.synthesize(args)
        subst, _ = check_type_against(res_ty, ty, self.node)
        return expr, subst

    @staticmethod
    def _is_numeric_or_bool_type(ty: Type) -> bool:
        return isinstance(ty, NumericType) or is_bool_type(ty)


class NatTruedivCompiler(CustomCallCompiler):
    """Compiler for the `nat.__truediv__` method."""

    def compile(self, args: list[OutPortV]) -> list[OutPortV]:
        from .builtins import Float, Nat

        # Compile `truediv` using float arithmetic
        [left, right] = args
        [left] = Nat.__float__.compile_call(
            [left], [], self.dfg, self.graph, self.globals, self.node
        )
        [right] = Nat.__float__.compile_call(
            [right], [], self.dfg, self.graph, self.globals, self.node
        )
        [out] = Float.__truediv__.compile_call(
            [left, right], [], self.dfg, self.graph, self.globals, self.node
        )
        return [out]


class IntTruedivCompiler(CustomCallCompiler):
    """Compiler for the `int.__truediv__` method."""

    def compile(self, args: list[OutPortV]) -> list[OutPortV]:
        from .builtins import Float, Int

        # Compile `truediv` using float arithmetic
        [left, right] = args
        [left] = Int.__float__.compile_call(
            [left], [], self.dfg, self.graph, self.globals, self.node
        )
        [right] = Int.__float__.compile_call(
            [right], [], self.dfg, self.graph, self.globals, self.node
        )
        [out] = Float.__truediv__.compile_call(
            [left, right], [], self.dfg, self.graph, self.globals, self.node
        )
        return [out]


class FloatBoolCompiler(CustomCallCompiler):
    """Compiler for the `float.__bool__` method."""

    def compile(self, args: list[OutPortV]) -> list[OutPortV]:
        from .builtins import Float

        # We have: bool(x) = (x != 0.0)
        zero_const = self.graph.add_constant(
            float_value(0.0), get_type(self.node), self.dfg.node
        )
        zero = self.graph.add_load_constant(zero_const.out_port(0), self.dfg.node)
        [out] = Float.__ne__.compile_call(
            [args[0], zero.out_port(0)],
            [],
            self.dfg,
            self.graph,
            self.globals,
            self.node,
        )
        return [out]


class FloatFloordivCompiler(CustomCallCompiler):
    """Compiler for the `float.__floordiv__` method."""

    def compile(self, args: list[OutPortV]) -> list[OutPortV]:
        from .builtins import Float

        # We have: floordiv(x, y) = floor(truediv(x, y))
        [div] = Float.__truediv__.compile_call(
            args, [], self.dfg, self.graph, self.globals, self.node
        )
        [floor] = Float.__floor__.compile_call(
            [div], [], self.dfg, self.graph, self.globals, self.node
        )
        return [floor]


class FloatModCompiler(CustomCallCompiler):
    """Compiler for the `float.__mod__` method."""

    def compile(self, args: list[OutPortV]) -> list[OutPortV]:
        from .builtins import Float

        # We have: mod(x, y) = x - (x // y) * y
        [div] = Float.__floordiv__.compile_call(
            args, [], self.dfg, self.graph, self.globals, self.node
        )
        [mul] = Float.__mul__.compile_call(
            [div, args[1]], [], self.dfg, self.graph, self.globals, self.node
        )
        [sub] = Float.__sub__.compile_call(
            [args[0], mul], [], self.dfg, self.graph, self.globals, self.node
        )
        return [sub]


class FloatDivmodCompiler(CustomCallCompiler):
    """Compiler for the `__divmod__` method."""

    def compile(self, args: list[OutPortV]) -> list[OutPortV]:
        from .builtins import Float

        # We have: divmod(x, y) = (div(x, y), mod(x, y))
        [div] = Float.__truediv__.compile_call(
            args, [], self.dfg, self.graph, self.globals, self.node
        )
        [mod] = Float.__mod__.compile_call(
            args, [], self.dfg, self.graph, self.globals, self.node
        )
        return [self.graph.add_make_tuple([div, mod], self.dfg.node).out_port(0)]


class MeasureCompiler(CustomCallCompiler):
    """Compiler for the `measure` function."""

    def compile(self, args: list[OutPortV]) -> list[OutPortV]:
        from .quantum import quantum_op

        [qubit] = args
        measure = self.graph.add_node(quantum_op("Measure"), inputs=args)
        self.graph.add_node(
            quantum_op("QFree"), inputs=[measure.add_out_port(qubit.ty)]
        )
        return [measure.add_out_port(bool_type())]


class QAllocCompiler(CustomCallCompiler):
    """Compiler for the `qubit` function."""

    def compile(self, args: list[OutPortV]) -> list[OutPortV]:
        from .quantum import quantum_op

        [qubit_ty] = type_to_row(get_type(self.node))
        qalloc = self.graph.add_node(quantum_op("QAlloc"), inputs=args)
        qalloc_result = qalloc.add_out_port(qubit_ty)
        reset = self.graph.add_node(quantum_op("Reset"), inputs=[qalloc_result])
        return [reset.add_out_port(qubit_ty)]
