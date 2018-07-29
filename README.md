<img align="right" width="375" height="400" src="https://upload.wikimedia.org/wikipedia/commons/0/0f/Alca_impennisAMF064LB.png">

## Auk

[![Build Status](https://travis-ci.com/IwoHerka/auk.svg?branch=master)](https://travis-ci.com/IwoHerka/auk)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7b8a7e7f2e5b4a748f34932ef112040a)](https://www.codacy.com/app/IwoHerka/auk?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=IwoHerka/auk&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/IwoHerka/auk/badge.svg?branch=master)](https://coveralls.io/github/IwoHerka/auk?branch=master)

**auk** is a micro-package for compiling s-expressions into
predicate functions.

```python
P, Q = True, False

sexp = \
    ['not',
        ['or',
            ['identifier', 'P'],
            ['identifier', 'Q'],
        ]
    ]

func = compile_predicate(sexp)
assert func(P, Q) == (not P and not Q)
```

### Interface

**auk**'s interface consists almost entirely of a single function -
``compile_predicate``, which accepts an s-expression and compiles it into
Python's function or lambda. Its signature is as follows:

```python
def compile_predicate(
        sexp: List,
        funcname: str = None,
        force_func: bool = False,
        force_lambda: bool = False) -> Union[FunctionType, LambdaType]
```

Above s-expression, for example, is compiled down to the following AST
(excluding boilerplate `ast.Module`, `lineno` and `col_offset`):

```python
FunctionDef(
    name = '_a5c28596600346faa54c0b092500fc48',
    args = arguments(
        args = [
            arg(arg = 'P', annotation = None),
            arg(arg = 'Q', annotation = None),
        ],
        vararg      = None,
        kwonlyargs  = [],
        kw_defaults = [],
        kwarg       = None,
        defaults    = [],
    ),
    body = [
        Return(
            value = UnaryOp(
                op = Not(),
                operand = BoolOp(
                    op = Or(),
                    values = [
                        Name(id = 'P', ctx = Load()),
                        Name(id = 'Q', ctx = Load()),
                    ],
                ),
            ),
        ),
    ],
    decorator_list = [],
    returns = None,
)
```

Compiled function returns value of the predicate s-expression (e.g. `UnaryOp`
as above), which, by the definition of a predicate, is always a truth value (I
explicitly avoid here saying "boolean", as it may happen that the target
function returns an object instead of `bool`. This is desired, however, as
every object in Python *is* in fact a truth value. For example, a list in
`is_not_empty = lambda array: array`

By default, expressions with up to one argument are compiled to lambdas and
everything else to functions. This is in order to allow passing arguments via
kwargs. This method of passing arguments should be a preferred one when
constructing complex expressions, as keeping track of the argument order
quickly becomes cumbersome. Compilation to lambda and function can be forced
with `force_lambda` and `force_function` options, respectively.

As you can see in the above example, when no name is specified for the target
function, random name is generated. Specifically, the name is generated using
this expression: `'_%s' % uuid.uuid4().hex`. In case of lambdas, the name
becomes a variable to which expression is assigned.

Because only a handful of built-in types (such as `num`, `str` or `list`) have
corresponding AST nodes, non-primitive types (e.g. user-defined classes) have
to be compiled into an `ast.Name` node (name binding) with random name (same
as above) and stored in target function's closure. Therefore, instances of
classes such as `class Foo: pass` end up as free-variables. For more details
see `eav.compiler.compile_terminal`.

### Grammar

Allowable expressions are defined by the following grammar:

```yaml
rules:
    predicate:
        - identifier
        - tautology
        - contradiction
        - not
        - and
        - or
        - eq
        - neq
        - lt
        - lte
        - gt
        - gte
        - in
        - literal
        - callable
    tautology:
        - [ ]
    contradiction:
        - [ ]
    identifier:
        - [ name ]
    not:
        - [ predicate ]
    and:
        - [ predicate+ ]
    or:
        - [ predicate+ ]
    eq:
        - [ term, term ]
    neq:
        - [ term, term ]
    lt:
        - [ term, term ]
    lte:
        - [ term, term ]
    gt:
        - [ term, term ]
    gte:
        - [ term, term ]
    in:
        - [ term, term ]
    callable:
        - [ '=FunctionType' ]
    term:
        - var_ref
        - literal
    var_ref:
        - identifier
    literal:
        - '~object'
    name:
        !regexpr '[a-zA-Z_][a-zA-Z0-9_]*'
```
For a detailed explanation of the grammar notation check out
<a href="https://github.com/IwoHerka/sexpr">**sexpr**  library documentation</a>.
In practice, almost every valid expression in Python can be translated to
valid s-expression. This includes constructs such as `in`, callables and
references:

```python
sexp = ['in', ['identifier', 'num', [1, 2, 3]]
func = compile_predicate(sexp)
assert func(2)
assert not func(4)

dice_roll = lambda: randint(1, 6)
sexp = ['eq', ['callable', dice_roll], 6]
lucky_six = compile_predicate(sexp)
assert lucky_six() # Luck required to pass

obj = object()
sexp = ['eq', ['identifier', 'obj'], obj]
func = compile_predicate(sexp)
assert func(obj)
assert not func(object())
 ```

For more examples, check out <a href="https://github.com/IwoHerka/booldog/blob/master/tests/examples.py">unit tests</a>.
