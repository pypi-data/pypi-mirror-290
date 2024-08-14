"""
  Provides factorial of given number.
"""


def factorial(num: int) -> int:
    """
    Provides factorial of given number.

    Parameters:
    - num (int): given number.

    Returns:
    - int: The factorial of passed number.
    """
    fact=1
    for i in range(1,num+1):
        fact*=i;
   
    return fact
