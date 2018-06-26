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

It provides a single function - ``compile_predicate``, accepting s-expression and returning Python's function.
