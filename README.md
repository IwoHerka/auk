[![Build Status](https://travis-ci.com/IwoHerka/booldog.svg?branch=master)](https://travis-ci.com/IwoHerka/booldog)
[![Coverage Status](https://coveralls.io/repos/github/IwoHerka/booldog/badge.svg?branch=master)](https://coveralls.io/github/IwoHerka/booldog?branch=master)

**booldog** is a micro-package for compiling s-expressions into
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

It provides a single function - ``compile_predicate``, accepting s-expression and returning Python's function.
