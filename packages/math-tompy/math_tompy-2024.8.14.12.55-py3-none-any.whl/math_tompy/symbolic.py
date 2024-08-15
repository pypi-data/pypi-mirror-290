from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Self, Optional

from sympy import Expr, Rational, Integer, Mul, Pow, S
from sympy.core.numbers import Half, Float


@dataclass
class Calculation:
    operation: Callable
    value0: Self | Decimal
    value1: Self | Decimal

    def result(self):
        value0: Calculation | Decimal = self.value0
        value1: Calculation | Decimal = self.value1

        if isinstance(value0, Calculation):
            value0 = value0.result()
        if isinstance(value1, Calculation):
            value1 = value1.result()

        return self.operation(value0, value1)


def expr_to_calc(expression: S) -> Calculation:
    calculation: Calculation | None = None
    operation: Optional[Callable] = None
    value0: Calculation | Decimal | None = None
    value1: Calculation | Decimal | None = None

    if len(expression.args) == 0:
        if isinstance(expression, Rational | Integer | Half):
            operation = Decimal.__truediv__
            value0 = Decimal(expression.p)
            value1 = Decimal(expression.q)
        elif isinstance(expression, Float):
            operation = Decimal.__add__
            value0 = Decimal(float(expression.num))
            value1 = Decimal(0)
        else:
            raise TypeError(f"Expression type '{type(expression)}' not yet supported.")
    else:
        if isinstance(expression, Mul):
            operation = Decimal.__mul__
        elif isinstance(expression, Pow):
            operation = Decimal.__pow__
        elif isinstance(expression, Expr):
            if isinstance(expression.args[0], Expr):
                calculation = expr_to_calc(expression=expression.args[0])
            elif isinstance(expression.args[0], int):
                calculation = Calculation(Decimal.__add__, value0=expression.args[0], value1=Decimal(0))
        else:
            raise TypeError(f"Expression type '{type(expression)}' not yet supported.")

        if calculation is None:
            value0 = expr_to_calc(expression=expression.args[0])
            value1 = expr_to_calc(expression=expression.args[1])

    if calculation is None and operation is not None and value0 is not None and value1 is not None:
        calculation = Calculation(operation=operation, value0=value0, value1=value1)
    else:
        raise ValueError(f"Unexpected values of operation '{operation}', value0 '{value0}', and value1 '{value1}'.")

    return calculation
