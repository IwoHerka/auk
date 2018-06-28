"""
    compiler
    ~~~~~~~~

    Core functionality of auk.
    Public interface consists of `compile_predicate` and 
    `read_argnames`. The former takes an s-expression and compiles it 
    into a function (or lambda). The latter is included as a 
    convienience, as compiling a list of arguments for target function 
    separetely is often handy.
"""
import ast
import os
import uuid
from types import FunctionType, LambdaType
from typing import Dict, List, Optional, Set, Union

import sexpr

from . import nodes

cd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

grammar = sexpr.load(os.path.join(cd, 'predicate.yml'))
rules = grammar.yaml


def read_argnames(sexp: List) -> Set[str]:
    """
    Builds expression's argument list. Traversal is performeed in a
    DFS manner.
    """
    names = set()

    if isinstance(sexp, list) and sexp and sexp[0] in grammar.top_tags:
        if sexp[0] == 'identifier':
            return set([sexp[1]])
        else:
            for child in sexp[1:]:
                names = names.union(read_argnames(child))

    return names


def compile_sexpr(sexp: List, closure: Optional[Dict] = None) -> ast.AST:
    """
    Compiles s-expression into AST expresssion. For a list of possible
    types, check out `auk.nodes` module.

    For explanation regarding `closure` see `compile_terminal`.
    """
    closure = closure or {}
    args = []

    if not (isinstance(sexp, list) and sexp and sexp[0] in grammar.top_tags):
        return compile_terminal(sexp, closure)

    tag = sexp[0]

    # ast.Name expects string, not ast.Str.
    # Therefore, we must stop recursion here.
    if tag == 'identifier':
        args = sexp[1:]
    else:
        for exp in sexp[1:]:
            arg, closure = compile_sexpr(exp, closure)
            args.append(arg)

    return getattr(nodes, 'compile_%s' % tag)(*args), closure


def compile_terminal(sexp: List, closure: Dict) -> ast.AST:
    """
    Compiles primitive type variable (language built-in) to AST node.

    `closure` contains name bindings for target function. Variables of
    non-primitive (built-in) types (without corresponding AST node) 
    are given a unique random name, converted to ast.Name and stored
    in closure for the target function.
    """
    if type(sexp) is bool:
        return ast.NameConstant(value = sexp), closure

    elif type(sexp) in (int, float, complex):
        return ast.Num(n = sexp), closure

    elif type(sexp) is str:
        return ast.Str(s = sexp), closure

    elif type(sexp) is bytes:
        return ast.Bytes(s = sexp), closure

    elif type(sexp) is list:
        elts = []
        for e in sexp:
            e, closure = compile_terminal(e, closure)
            elts.append(e)
        return ast.List(elts = elts, ctx = ast.Load()), closure

    elif type(sexp) is tuple:
        elts = []
        for e in sexp:
            e, closure = compile_terminal(e, closure)
            elts.append(e)
        return ast.Tuple(elts = elts, ctx = ast.Load()), closure

    elif type(sexp) is dict:
        keys, values = [], []
        for k, v in sexp.items():
            k, closure = compile_terminal(k, closure)
            v, closure = compile_terminal(v, closure)
            keys.append(k)
            values.append(v)
        return ast.Dict(keys = keys, values = values), closure

    elif type(sexp) is set:
        elts = []
        for e in sexp:
            e, closure = compile_terminal(e, closure)
            elts.append(e)
        return ast.Set(elts=elts), closure

    else:
        # Generate random name and store variable in closure.
        name = '_%s' % uuid.uuid4().hex
        closure[name] = sexp
        return ast.Name(id = name, ctx = ast.Load()), closure


def define_func(name, args, body):
    """
    Construct AST function definition with specified name, args and 
    body.
    """
    return ast.FunctionDef(
        name = name,
        args = args,
        body = [ast.Return(value = body)],
        decorator_list = [],
        returns = None,
    )


def define_lambda(name, args, body):
    """
    Construct AST lambda assignment with specified name, args and 
    body. Because lambdas are anonymous, we must assign them to some 
    variable in order to reference them. This variable is returned to 
    end-user.
    """
    return ast.Assign(
        targets = [
            ast.Name(
                id = name,
                ctx = ast.Store()
            )
        ],
        value = ast.Lambda(
            args = args,
            body = body
        )
    )


def compile_predicate(
        sexp: List,
        funcname: str = None,
        force_func: bool = False,
        force_lambda: bool = False) -> Union[FunctionType, LambdaType]:
    """
    Compiles s-expression into predicate function.

    S-expression is validated by the grammar (`predicate.yml`) and,
    if ill-formed, `None` is returned.

    By default, s-expressions with one or zero arguments are compiled
    to lambdas and everything else to proper Python function. This is
    in order to allow passing arguments via kwargs instead of regular
    args. Although argument names are always read in a DFS manner,
    with complex s-expressions, keeping track of the argument order is
    very cumbersome. Compilation to either lambda or function can be
    forced with `force_lambda` and `force_function`, respectively.

    If compiling to function, `compile_predicate` can be provided with
    the name. If `funcname` is null, random UUID is generated.
    """
    if not grammar.matches(sexp):
        return None

    argnames = read_argnames(sexp)
    exp, env = compile_sexpr(sexp, closure = {})
    funcname = funcname or '_%s' % uuid.uuid4().hex
    arglist  = [ast.arg(arg = name, annotation = None) for name in argnames]

    args = ast.arguments(
        args        = arglist,
        vararg      = None,
        kwonlyargs  = [],
        kw_defaults = [],
        kwarg       = None,
        defaults    = [],
    )

    if force_func or not force_lambda and len(argnames) > 1:
        define = define_func
    else:
        define = define_lambda

    func_def = define(funcname, args, exp)
    func_def = ast.fix_missing_locations(func_def)
    module   = ast.Module(body = [func_def])

    exec(compile(module, '<string>', mode = 'exec'), env)
    return env[funcname]
