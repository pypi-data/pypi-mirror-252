[![PyPI version](https://badge.fury.io/py/mud-examples.svg)](https://badge.fury.io/py/mud-examples)
![unit testing workflow](https://github.com/mathematicalmichael/mud-examples/actions/workflows/main.yml/badge.svg)
![example workflow](https://github.com/mathematicalmichael/mud-examples/actions/workflows/examples.yml/badge.svg)
![publish workflow](https://github.com/mathematicalmichael/mud-examples/actions/workflows/publish.yml/badge.svg)
[![codecov](https://codecov.io/gh/mathematicalmichael/mud-examples/branch/main/graph/badge.svg?token=JQZao81BSp)](https://codecov.io/gh/mathematicalmichael/mud-examples)
[![coveralls](https://coveralls.io/repos/github/mathematicalmichael/mud-examples/badge.svg?branch=main)](https://coveralls.io/github/mathematicalmichael/mud-examples?branch=main)

# MUD-Examples
## Examples for _Existence, Uniqueness, and Convergence of Parameter Estimates with Maximal Updated Densities_

Authors: Troy Butler & Michael Pilosov

# Installation
For Python 3.7-3.12:

```sh
pip install mud-examples
```

To reproduce the results in Michael's thesis, use `mud-examples==0.1`. However, this comes with `mud==0.0.28`.
Newer versions should still produce the same figures.

TeX is recommended (but not required):

```
apt-get install -yqq \
    texlive-base \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-science \
    latexmk \
    dvipng \
    cm-super
```


# Quickstart

Generate all of the figures the way they are referenced in the paper:
```sh
mud_run_all
```
The above is equivalent to running all of the examples sequentially:

```sh
mud_run_inv
mud_run_lin
mud_run_ode
mud_run_pde
```

# Usage

The `mud_run_X` scripts all call the same primary entrypoint, which you can call with the console script `mud_examples`.

Here are two examples:
```sh
mud_examples --example ode
```

```sh
mud_examples --example lin
```

and so on. (More on this later, once argparsing is better handled, they might just be entrypoints to the modules themselves rather than a central `runner.py`, which really only exists to compare several experiments, so perhaps it warrants renaming to reflect that).
