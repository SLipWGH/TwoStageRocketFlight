G = 6.674 * (10 ** (-11))
r0 = 6371 * (10 ** 3)
M = 5.9726 * (10 ** 24)


def g(
    h: float,
)-> float:
    return G *  M / ((r0 + h) ** 2)


def aerodynamic_force(
    Cx: float,
    rho: float,
    v: float,
    S: float
)-> float:
    return Cx * rho * (v ** 2) * S / 2


def thirst_force(
    dot_m: float,
    v_a: float,
    F_a: float,
    p_a: float,
    p_h: float
)-> float:
    return dot_m * v_a + F_a * (p_a - p_h)