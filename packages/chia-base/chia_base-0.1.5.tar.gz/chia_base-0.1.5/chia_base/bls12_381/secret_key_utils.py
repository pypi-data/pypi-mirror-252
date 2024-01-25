"""
Some secret key utilities that need to know the group order and return `blspy`
structures.
"""


import blspy  # type: ignore


GROUP_ORDER = (
    52435875175126190479447740508185965837690552500527637822603658699938581184513
)


def private_key_from_int(secret_exponent: int) -> blspy.PrivateKey:
    "convert an `int` into the `blspy.PrivateKey`"
    secret_exponent %= GROUP_ORDER
    blob = secret_exponent.to_bytes(32, "big")
    return blspy.PrivateKey.from_bytes(blob)


def public_key_from_int(secret_exponent: int) -> blspy.G1Element:
    "convert an `int` into the corresponding `blspy.G1Element` multiple of generator"
    return private_key_from_int(secret_exponent).get_g1()
