"""Simple recursive math functions and a small test runner.

This module provides a recursive implementation of factorial.
Run it as a script or import `factorial` into other code.
"""

from typing import Any


def factorial(n: int) -> int:
    """Return n! (factorial) computed recursively.

    Args:
        n: non-negative integer

    Returns:
        int: n factorial

    Raises:
        TypeError: if `n` is not an int
        ValueError: if `n` is negative

    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
    """

    if not isinstance(n, int):
        raise TypeError("factorial() only accepts integers")
    if n < 0:
        raise ValueError("factorial() not defined for negative values")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


if __name__ == "__main__":
    import sys

    # Quick demonstration values
    demo_values = [0, 1, 2, 5, 10]
    for v in demo_values:
        print(f"{v}! = {factorial(v)}")

    # If an argument is provided, try to compute its factorial
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except Exception as e:
            print("Please provide an integer as an argument. Error:", e)
        else:
            try:
                print(f"{n}! = {factorial(n)}")
            except Exception as e:
                print("Error computing factorial:", e)
