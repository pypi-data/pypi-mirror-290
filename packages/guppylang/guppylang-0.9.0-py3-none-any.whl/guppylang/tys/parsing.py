import ast
from collections.abc import Sequence

from guppylang.ast_util import (
    AstNode,
    set_location_from,
    shift_loc,
)
from guppylang.checker.core import Globals
from guppylang.definition.parameter import ParamDef
from guppylang.definition.ty import TypeDef
from guppylang.error import GuppyError
from guppylang.tys.arg import Argument, ConstArg, TypeArg
from guppylang.tys.const import ConstValue
from guppylang.tys.param import Parameter, TypeParam
from guppylang.tys.ty import NoneType, NumericType, TupleType, Type


def arg_from_ast(
    node: AstNode,
    globals: Globals,
    param_var_mapping: dict[str, Parameter] | None = None,
) -> Argument:
    """Turns an AST expression into an argument."""
    # A single identifier
    if isinstance(node, ast.Name):
        x = node.id
        if x not in globals:
            raise GuppyError("Unknown identifier", node)
        match globals[x]:
            # Either a defined type (e.g. `int`, `bool`, ...)
            case TypeDef() as defn:
                return TypeArg(defn.check_instantiate([], globals, node))
            # Or a parameter (e.g. `T`, `n`, ...)
            case ParamDef() as defn:
                if param_var_mapping is None:
                    raise GuppyError(
                        "Free type variable. Only function types can be generic", node
                    )
                if x not in param_var_mapping:
                    param_var_mapping[x] = defn.to_param(len(param_var_mapping))
                return param_var_mapping[x].to_bound()
            case defn:
                raise GuppyError(
                    f"Expected a type, got {defn.description} `{defn.name}`", node
                )

    # A parametrised type, e.g. `list[??]`
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
        x = node.value.id
        if x in globals:
            defn = globals[x]
            if isinstance(defn, TypeDef):
                arg_nodes = (
                    node.slice.elts
                    if isinstance(node.slice, ast.Tuple)
                    else [node.slice]
                )
                # Hack: Flatten argument lists to support the `Callable` type. For
                # example, we turn `Callable[[int, int], bool]` into
                # `Callable[int, int, bool]`.
                # TODO: We can get rid of this once we added support for variadic params
                arg_nodes = [
                    n
                    for arg in arg_nodes
                    for n in (arg.elts if isinstance(arg, ast.List) else (arg,))
                ]
                args = [
                    arg_from_ast(arg_node, globals, param_var_mapping)
                    for arg_node in arg_nodes
                ]
                ty = defn.check_instantiate(args, globals, node)
                return TypeArg(ty)
            # We don't allow parametrised variables like `T[int]`
            if isinstance(defn, ParamDef):
                raise GuppyError(
                    f"Variable `{x}` is not parameterized. Higher-kinded types are not "
                    f"supported",
                    node,
                )

    # We allow tuple types to be written as `(int, bool)`
    if isinstance(node, ast.Tuple):
        ty = TupleType(
            [type_from_ast(el, globals, param_var_mapping) for el in node.elts]
        )
        return TypeArg(ty)

    # `None` is represented as a `ast.Constant` node with value `None`
    if isinstance(node, ast.Constant) and node.value is None:
        return TypeArg(NoneType())

    # Integer literals are turned into nat args since these are the only ones we support
    # right now.
    # TODO: Once we also have int args etc, we need proper inference logic here
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        # Fun fact: int ast.Constant values are never negative since e.g. `-5` is a
        # `ast.UnaryOp` negation of a `ast.Constant(5)`
        assert node.value >= 0
        nat_ty = NumericType(NumericType.Kind.Nat)
        return ConstArg(ConstValue(nat_ty, node.value))

    # Finally, we also support delayed annotations in strings
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        try:
            [stmt] = ast.parse(node.value).body
            if not isinstance(stmt, ast.Expr):
                raise GuppyError("Invalid Guppy type", node)
            set_location_from(stmt, loc=node)
            shift_loc(
                stmt,
                delta_lineno=node.lineno - 1,  # -1 since lines start at 1
                delta_col_offset=node.col_offset + 1,  # +1 to remove the `"`
            )
            return arg_from_ast(stmt.value, globals, param_var_mapping)
        except (SyntaxError, ValueError):
            raise GuppyError("Invalid Guppy type", node) from None

    raise GuppyError("Not a valid type argument", node)


_type_param = TypeParam(0, "T", True)


def type_from_ast(
    node: AstNode,
    globals: Globals,
    param_var_mapping: dict[str, Parameter] | None = None,
) -> Type:
    """Turns an AST expression into a Guppy type."""
    # Parse an argument and check that it's valid for a `TypeParam`
    arg = arg_from_ast(node, globals, param_var_mapping)
    return _type_param.check_arg(arg, node).ty


def type_row_from_ast(node: ast.expr, globals: "Globals") -> Sequence[Type]:
    """Turns an AST expression into a Guppy type row.

    This is needed to interpret the return type annotation of functions.
    """
    # The return type `-> None` is represented in the ast as `ast.Constant(value=None)`
    if isinstance(node, ast.Constant) and node.value is None:
        return []
    ty = type_from_ast(node, globals)
    if isinstance(ty, TupleType):
        return ty.element_types
    else:
        return [ty]
