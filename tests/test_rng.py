import random

from evo import rng


def test_seed_global_repeatability():
    rng.seed_global(123)
    seq1 = [random.randint(0, 100) for _ in range(5)]
    rng.seed_global(123)
    seq2 = [random.randint(0, 100) for _ in range(5)]
    assert seq1 == seq2


def test_make_subseed_stability():
    s1 = rng.make_subseed("alpha", 100)
    s2 = rng.make_subseed("alpha", 100)
    s3 = rng.make_subseed("beta", 100)
    assert s1 == s2
    assert s1 != s3
    assert 0 <= s1 < 2**32


def test_rng_context_isolation():
    rng.seed_global(42)
    outside = random.randint(0, 9999)
    with rng.rng_context("inner", 42):
        inside1 = [random.randint(0, 100) for _ in range(3)]
    with rng.rng_context("inner", 42):
        inside2 = [random.randint(0, 100) for _ in range(3)]
    assert inside1 == inside2
    new_outside = random.randint(0, 9999)
    assert outside != new_outside  # RNG advanced only outside contexts


def test_hash_dict_stable_ordering():
    d1 = {"a": 1, "b": 2, "c": 3}
    d2 = {"c": 3, "b": 2, "a": 1}
    assert rng.hash_dict(d1) == rng.hash_dict(d2)


def test_hash_bytes_matches_known_vector():
    data = b"hello world"
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert rng.hash_bytes(data) == expected
