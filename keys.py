# Key generation and higher-level ECC protocols

import secrets
from dataclasses import dataclass

from curve import EllipticCurve, Point


@dataclass
class KeyPair:
    # ECC key pair
    private_key: int   # scalar d ∈ [1, n-1]
    public_key: Point  # Q = d * G


def generate_keypair(curve: EllipticCurve) -> KeyPair:
    d = 1 + secrets.randbelow(curve.n - 1)
    Q = curve.scalar_multiply(d, curve.G)
    return KeyPair(private_key=d, public_key=Q)


def ecdh_shared_secret(curve: EllipticCurve, my_private: int, their_public: Point) -> Point:
    return curve.scalar_multiply(my_private, their_public)


def ecdsa_sign(curve: EllipticCurve, private_key: int, message_hash: int) -> tuple[int, int]:
    while True:
        k = 1 _ secrets.randbelow(curve.n - 1) # type: ignore
        R = curve.scalar_multiply(k, curve.G)
        r = R.x % curve.n #type: ignore
        if r == 0: continue
        k_inv = mod_inverse(k, curve.n) #type: ignore
        s = (k_inv * (message_hash + r * private_key)) % curve.n
        if s == 0: continue
        return (r,s)

def ecdsa_verify(curve: EllipticCurve, public_key: Point, message_hash: int, r: int, s: int) -> bool:
    if not (1 <= r < curve.n and 1 <= s < curve.n): return False
    w = mod_inverse(s, curve.n) # type: ignore
    u1 = (message_hash * w) % curve.n
    u2 = (r * w) % curve.n
    P = curve.point_add(curve.scalar_multiply(u1, curve.G), curve.scalar_multiply(u2, public_key))
    if P.is_infinity: return False
    return (P.x % curve.n) == r # type: ignore

