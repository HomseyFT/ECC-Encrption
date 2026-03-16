"""
Test suite for the ECC implementation.

Run with: python -m pytest test_ecc.py -v
Or just:  python test_ecc.py

Implement tests incrementally — start with field ops, then point ops,
then key gen, then protocols.
"""

from field import mod_inverse, legendre_symbol
from curve import EllipticCurve, Point, INFINITY
from params import SECP256K1, TOY_CURVE


# ── Field arithmetic tests ───────────────────────────────────────────

def test_mod_inverse():
    """mod_inverse(a, p) * a ≡ 1 (mod p)"""
    p = 97
    for a in range(1, p):
        inv = mod_inverse(a, p)
        assert (a * inv) % p == 1, f"Failed for a={a}"
    print("✓ mod_inverse")


def test_mod_inverse_known_values():
    """Spot-check against pow(a, p-2, p) (Fermat)."""
    p = 97
    assert mod_inverse(3, p) == pow(3, p - 2, p)
    assert mod_inverse(50, p) == pow(50, p - 2, p)
    print("✓ mod_inverse known values")


# ── Curve validation tests ───────────────────────────────────────────

def test_point_on_curve():
    """Generator point should be on the curve."""
    assert TOY_CURVE.is_on_curve(TOY_CURVE.G)
    assert SECP256K1.is_on_curve(SECP256K1.G)
    print("✓ points on curve")


def test_infinity_on_curve():
    """Point at infinity is always on the curve."""
    assert TOY_CURVE.is_on_curve(INFINITY)
    print("✓ infinity on curve")


# ── Point operation tests ────────────────────────────────────────────

def test_add_identity():
    """P + ∞ = P"""
    G = TOY_CURVE.G
    assert TOY_CURVE.point_add(G, INFINITY) == G
    assert TOY_CURVE.point_add(INFINITY, G) == G
    print("✓ add identity")


def test_add_inverse():
    """P + (-P) = ∞"""
    G = TOY_CURVE.G
    neg_G = TOY_CURVE.point_negate(G)
    result = TOY_CURVE.point_add(G, neg_G)
    assert result.is_infinity
    print("✓ add inverse")


def test_double():
    """2 * G should be on the curve."""
    result = TOY_CURVE.point_double(TOY_CURVE.G)
    assert TOY_CURVE.is_on_curve(result)
    assert not result.is_infinity
    print("✓ point doubling")


def test_scalar_multiply_identity():
    """1 * G = G"""
    result = TOY_CURVE.scalar_multiply(1, TOY_CURVE.G)
    assert result == TOY_CURVE.G
    print("✓ scalar multiply identity")


def test_scalar_multiply_order():
    """n * G = ∞ (where n is the order of G)"""
    result = TOY_CURVE.scalar_multiply(TOY_CURVE.n, TOY_CURVE.G)
    assert result.is_infinity
    print("✓ scalar multiply by order")


def test_scalar_multiply_associative():
    """(a * b) * G == a * (b * G)"""
    a, b = 3, 4
    lhs = TOY_CURVE.scalar_multiply(a * b, TOY_CURVE.G)
    intermediate = TOY_CURVE.scalar_multiply(b, TOY_CURVE.G)
    rhs = TOY_CURVE.scalar_multiply(a, intermediate)
    assert lhs == rhs
    print("✓ scalar multiply associative")


# ── secp256k1 smoke test ─────────────────────────────────────────────

def test_secp256k1_generator_on_curve():
    """The published secp256k1 generator must satisfy the curve equation."""
    assert SECP256K1.is_on_curve(SECP256K1.G)
    print("✓ secp256k1 generator on curve")


# ── Run all tests ────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError:
            print(f"⏭ {test.__name__} (not yet implemented)")
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
        except Exception as e:
            print(f"✗ {test.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
