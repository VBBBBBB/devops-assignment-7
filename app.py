"""Simple application used for the Jenkins + GitHub CI pipeline demonstration.

Assignment 7 - Continuous Integration Using Jenkins and GitHub.
"""


def greet(name: str = "DevOps") -> str:
    """Return a friendly greeting."""
    if not name:
        raise ValueError("Name must not be empty.")
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def is_even(number: int) -> bool:
    """Return True when the number is even."""
    return number % 2 == 0


if __name__ == "__main__":
    print(greet("DevOps"))
    print("2 + 3 =", add(2, 3))
    print("Is 4 even?", is_even(4))
