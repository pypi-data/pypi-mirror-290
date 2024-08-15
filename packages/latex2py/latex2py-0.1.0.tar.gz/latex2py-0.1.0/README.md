# LaTeX-to-Python Parser (`latex2py`)

This is a lightweight **LaTeX-to-Python** parser.

We needed a parser that could convert LaTeX math expressions into Python-like expressions. However, [SymPy](https://github.com/sympy/sympy) is an extremely large library (`~50 MB`) and leads to bundle size issues when deploying code as an AWS lambda function (max. size `250MB`). This codebase strips out the minimal code that we need, and is around `~200kb` in size.

The parser is inspired by the `sympy` LaTeX parser, but instead of returning symbolic SymPy expressions, we return lines of Python-like code which could can then be evaluated in the interpreter.

## Setup

Run `pipenv install` to create a virtual environment and install dependencies.

## Usage

```python
from latex2py.parser import parse_latex

latex = r'\frac{1}{2} + \frac{3}{4}'
python = parse_latex(latex)
print(python)

# Output:
# (1 / 2) + (3 / 4)
```

## Tests

Run `pytest tests` to run the test suite. You can find examples of parseable LaTeX syntex there too.