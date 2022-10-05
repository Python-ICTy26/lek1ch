import random
from typing import Tuple


def multiplicative_inverse(e: int, phi: int) -> int:
    def gcd_extended(a, b):
        if a == 0:
            return b, 0, 1
        else:
            d, y, x = gcd_extended(b % a, a)
            return d, x - y * (b // a), y

    d, x, y = gcd_extended(e, phi)
    return x % phi


def gcd(a: int, b: int) -> int:
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def is_prime(n: int) -> bool:
    return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q can not be equal")
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)
