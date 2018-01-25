from functools import reduce


def factors(n):
    """
    Function returns the factors of a given integer, n
    cite: https://stackoverflow.com/questions/6800193
    """
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0)))

