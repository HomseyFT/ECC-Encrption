from curve import EllipticCurve, Point


# ── secp256k1 ────────────────────────────────────────────────────────
# Used by Bitcoin and Ethereum. Defined over a 256-bit prime field.
# Curve: y^2 = x^3 + 7  (a=0, b=7)

SECP256K1 = EllipticCurve(
    a=0,
    b=7,
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    G=Point(
        x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    ),
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    ) # type: ignore


# ── NIST P-256 (secp256r1 / prime256v1) ─────────────────────────────
# NIST standard curve widely used in TLS, etc.
# Curve: y^2 = x^3 - 3x + b

P256 = EllipticCurve(
    a=-3,
    b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    G=Point(
        x=0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
        y=0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
    ),
    n=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    ) # type: ignore


# Practice curve
TOY_CURVE = EllipticCurve(
    a=2,
    b=3,
    p=97,
    G=Point(x=3, y=6),
    n=5,  # TODO: Compute the actual order of G on this curve
    ) # type: ignore
