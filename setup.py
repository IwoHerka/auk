from setuptools import setup

setup(
    name             = 'booldog',
    version          = '0.1.0',
    license          = 'MIT',
    requires         = ['python (>= 3.4)'],
    provides         = ['booldog'],
    description      = 'Micro-package for compiling s-expressions into Python\'s predicate functions' ,
    url              = 'http://github.com/IwoHerka/booldog',
    packages         = ['booldog', 'tests'],
    maintainer       = 'Iwo Herka',
    maintainer_email = 'hi@iwoherka.eu',
    author           = 'Iwo Herka',
    author_email     = 'hi@iwoherka.eu',

    include_package_data = True,
    package_data = dict(booldog = ['predicate.yml']),
    install_requires = [
        'sexpr'
    ],

    classifiers  = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python'
    ],
)
