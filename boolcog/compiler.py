import os
import uuid
from ast import *

import sexpr

from . import nodes

cd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file_path = os.path.join(cd, 'predicate.yml')

grammar = sexpr.load(file_path)
tags = grammar.rules.keys()


def coerce(sexp, scope = None):
    scope = scope or {}
    args = []

    if not (isinstance(sexp, list) and sexp and sexp[0] in tags):
        return compile_terminal(sexp, scope)

    tag = sexp[0]

    # ast.Name expects string, not ast.Str.
    # Therefore, we must stop recursion here.
    if tag == 'identifier':
        args = sexp[1:]
    else:
        for exp in sexp[1:]:
            arg, scope = coerce(exp)
            args.append(arg)

    return getattr(nodes, 'compile_%s' % tag)(*args), scope


def compile_terminal(sexp, scope):
    if type(sexp) is bool:
        return NameConstant(value=sexp), scope

    elif type(sexp) in (int, float, complex):
        return Num(n=sexp), scope

    elif type(sexp) is str:
        return Str(s=sexp), scope

    elif type(sexp) is bytes:
        return Bytes(s=sexp), scope

    elif type(sexp) is list:
        elts = []
        for e in sexp:
            e, scope = compile_terminal(e, scope)
            elts.append(e)
        return List(elts=elts, ctx=Load()), scope

    elif type(sexp) is tuple:
        elts = []
        for e in sexp:
            e, scope = compile_terminal(e, scope)
            elts.append(e)
        return Tuple(elts = elts, ctx = Load()), scope

    elif type(sexp) is dict:
        keys, values = [], []
        for k, v in sexp.items():
            k, scope = compile_terminal(k, scope)
            v, scope = compile_terminal(v, scope)
            keys.append(k)
            values.append(v)
        return Dict(keys = keys, values = values), scope

    elif type(sexp) is set:
        elts = []
        for e in sexp:
            e, scope = compile_terminal(e, scope)
            elts.append(e)
        return Set(elts=elts), scope

    else:
        name = '_v%s' % uuid.uuid4().hex
        scope[name] = sexp
        return Name(id = name, ctx = ast.Load()), scope


def compile_predicate(sexp, argnames = None, funcname = None):
    if not grammar.matches(sexp):
        return None

    funcname = funcname or 'foo'
    argnames = argnames or []
    scope = {}
    exp, scope = coerce(sexp, scope)
    arg_list = [arg(arg = name, annotation = None) for name in argnames]

    func_def = FunctionDef(
        name = funcname,
        args = arguments(
            args        = arg_list,
            vararg      = None,
            kwonlyargs  = [],
            kw_defaults = [],
            kwarg       = None,
            defaults    = [],
        ),
        body = [Return(value = exp)],
        decorator_list = [],
        returns = None,
    )

    func_def = ast.fix_missing_locations(func_def)
    exec(compile(Module(body = [func_def]), '<string>', mode = 'exec'), scope)
    return scope[funcname]
