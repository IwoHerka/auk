[![Build Status](https://travis-ci.com/IwoHerka/auk.svg?branch=master)](https://travis-ci.com/IwoHerka/auk)
[![Coverage Status](https://coveralls.io/repos/github/IwoHerka/auk/badge.svg?branch=master)](https://coveralls.io/github/IwoHerka/auk?branch=master)

**auk** is a micro-package for compiling s-expressions into
predicate functions.

```python
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

It provides a single function - ``compile_predicate``, accepting s-expression and returning Python's `FunctionType`.
Above s-expression, for example, is compiled to the following AST (excluding boilerplate `ast.Module`, `lineno` and `col_offset`):

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

Compiled function returns value of the predicate s-expression (e.g. `UnaryOp` as above), which, by the definition of a predicate, is always a boolean. Expressions are compiled to function (a not lambdas) to allow passing kwargs. This method of passing arguments should be always preferred when constructing more complex expressions. Allowable expressions are defined by the following grammar:

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
For a detailed explanation of the grammar notation check out <a href="https://github.com/IwoHerka/sexpr">**sexpr**  library documentation</a>. In practice, almost every valid Python expression can be translated to valid s-expression. This includes
constructs such as `in`, callables and references:

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
