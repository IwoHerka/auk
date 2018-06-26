import os
import ast
import uuid

import sexpr

from . import nodes

cd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file_path = os.path.join(cd, 'predicate.yml')

grammar = sexpr.load(file_path)
tags = grammar.rules.keys()


def read_argnames(sexp):
    names = set()

    if isinstance(sexp, list) and sexp and sexp[0] in tags:
        if sexp[0] == 'identifier':
            return set([sexp[1]])
        else:
            for child in sexp[1:]:
                names = names.union(read_argnames(child))

    return names


def compile_sexpr(sexp, scope = None):
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
            arg, scope = compile_sexpr(exp, scope)
            args.append(arg)

    return getattr(nodes, 'compile_%s' % tag)(*args), scope


def compile_terminal(sexp, scope):
    if type(sexp) is bool:
        return ast.NameConstant(value = sexp), scope

    elif type(sexp) in (int, float, complex):
        return ast.Num(n = sexp), scope

    elif type(sexp) is str:
        return ast.Str(s = sexp), scope

    elif type(sexp) is bytes:
        return ast.Bytes(s = sexp), scope

    elif type(sexp) is list:
        elts = []
        for e in sexp:
            e, scope = compile_terminal(e, scope)
            elts.append(e)
        return ast.List(elts = elts, ctx = ast.Load()), scope

    elif type(sexp) is tuple:
        elts = []
        for e in sexp:
            e, scope = compile_terminal(e, scope)
            elts.append(e)
        return ast.Tuple(elts = elts, ctx = ast.Load()), scope

    elif type(sexp) is dict:
        keys, values = [], []
        for k, v in sexp.items():
            k, scope = compile_terminal(k, scope)
            v, scope = compile_terminal(v, scope)
            keys.append(k)
            values.append(v)
        return ast.Dict(keys = keys, values = values), scope

    elif type(sexp) is set:
        elts = []
        for e in sexp:
            e, scope = compile_terminal(e, scope)
            elts.append(e)
        return ast.Set(elts=elts), scope

    else:
        name = '_v%s' % uuid.uuid4().hex
        scope[name] = sexp
        return ast.Name(id = name, ctx = ast.Load()), scope


def compile_predicate(sexp, funcname = None, debug = False):
    if not grammar.matches(sexp):
        return None

    funcname = funcname or 'foo'
    argnames = read_argnames(sexp)
    scope = {}
    exp, scope = compile_sexpr(sexp, scope)
    arg_list = [ast.arg(arg = name, annotation = None) for name in argnames]

    func_def = ast.FunctionDef(
        name = funcname,
        args = ast.arguments(
            args        = arg_list,
            vararg      = None,
            kwonlyargs  = [],
            kw_defaults = [],
            kwarg       = None,
            defaults    = [],
        ),
        body = [ast.Return(value = exp)],
        decorator_list = [],
        returns = None,
    )

    func_def = ast.fix_missing_locations(func_def)
    mod = ast.Module(body = [func_def])

    if debug:
        try:
            from astpretty import pprint
            pprint(func_def, show_offsets = False)
        except ImportError:
            print('Cannot import astpretty')

    exec(compile(mod, '<string>', mode = 'exec'), scope)
    return scope[funcname]
