"""Tabla Normal estándar de la cátedra (UADE — 2.º parcial).

El parcial se resuelve con la **tabla Z** (z a 2 decimales → Φ a 4 decimales),
no con el valor exacto de scipy. Usar esta tabla hace que el número final y el
paso a paso coincidan con la clave del profesor.

    Φ(z) = P(Z ≤ z)      con Z ~ Normal(0, 1)
    Φ(−z) = 1 − Φ(z)     (simetría)

Funciones:
    phi(z)            → Φ(z) leído de la tabla (z redondeado a 2 decimales).
    z_critico(alpha)  → z tal que Φ(z) = alpha (fractiles típicos exactos +
                        búsqueda en la tabla para el resto).
    phi_pdf(z)        → densidad normal estándar φ(z) (para H(x), esperanza parcial).
    fmt_z(z)          → z redondeado a 2 decimales (para mostrar en el paso a paso).
"""

from __future__ import annotations

import math

# Φ(z) para z = 0.00 .. 3.09  (filas = décimos, columnas = centésimos .00–.09)
# Copiada de la tabla del FORMULARIO del 2.º parcial.
_ROWS: dict[int, list[float]] = {
    0:  [.5000, .5040, .5080, .5120, .5160, .5199, .5239, .5279, .5319, .5359],
    1:  [.5398, .5438, .5478, .5517, .5557, .5596, .5636, .5675, .5714, .5753],
    2:  [.5793, .5832, .5871, .5910, .5948, .5987, .6026, .6064, .6103, .6141],
    3:  [.6179, .6217, .6255, .6293, .6331, .6368, .6406, .6443, .6480, .6517],
    4:  [.6554, .6591, .6628, .6664, .6700, .6736, .6772, .6808, .6844, .6879],
    5:  [.6915, .6950, .6985, .7019, .7054, .7088, .7123, .7157, .7190, .7224],
    6:  [.7257, .7291, .7324, .7357, .7389, .7422, .7454, .7486, .7517, .7549],
    7:  [.7580, .7611, .7642, .7673, .7704, .7734, .7764, .7794, .7823, .7852],
    8:  [.7881, .7910, .7939, .7967, .7995, .8023, .8051, .8078, .8106, .8133],
    9:  [.8159, .8186, .8212, .8238, .8264, .8289, .8315, .8340, .8365, .8389],
    10: [.8413, .8438, .8461, .8485, .8508, .8531, .8554, .8577, .8599, .8621],
    11: [.8643, .8665, .8686, .8708, .8729, .8749, .8770, .8790, .8810, .8830],
    12: [.8849, .8869, .8888, .8907, .8925, .8944, .8962, .8980, .8997, .9015],
    13: [.9032, .9049, .9066, .9082, .9099, .9115, .9131, .9147, .9162, .9177],
    14: [.9192, .9207, .9222, .9236, .9251, .9265, .9279, .9292, .9306, .9319],
    15: [.9332, .9345, .9357, .9370, .9382, .9394, .9406, .9418, .9429, .9441],
    16: [.9452, .9463, .9474, .9484, .9495, .9505, .9515, .9525, .9535, .9545],
    17: [.9554, .9564, .9573, .9582, .9591, .9599, .9608, .9616, .9625, .9633],
    18: [.9641, .9649, .9656, .9664, .9671, .9678, .9686, .9693, .9699, .9706],
    19: [.9713, .9719, .9726, .9732, .9738, .9744, .9750, .9756, .9761, .9767],
    20: [.9772, .9778, .9783, .9788, .9793, .9798, .9803, .9808, .9812, .9817],
    21: [.9821, .9826, .9830, .9834, .9838, .9842, .9846, .9850, .9854, .9857],
    22: [.9861, .9864, .9868, .9871, .9875, .9878, .9881, .9884, .9887, .9890],
    23: [.9893, .9896, .9898, .9901, .9904, .9906, .9909, .9911, .9913, .9916],
    24: [.9918, .9920, .9922, .9925, .9927, .9929, .9931, .9932, .9934, .9936],
    25: [.9938, .9940, .9941, .9943, .9945, .9946, .9948, .9949, .9951, .9952],
    26: [.9953, .9955, .9956, .9957, .9959, .9960, .9961, .9962, .9963, .9964],
    27: [.9965, .9966, .9967, .9968, .9969, .9970, .9971, .9972, .9973, .9974],
    28: [.9974, .9975, .9976, .9977, .9977, .9978, .9979, .9979, .9980, .9981],
    29: [.9981, .9982, .9982, .9983, .9984, .9984, .9985, .9985, .9986, .9986],
    30: [.9987, .9987, .9987, .9988, .9988, .9989, .9989, .9989, .9990, .9990],
}

# z máximo tabulado (3.09). Más allá, Φ ≈ 1.
_Z_MAX = 3.09
_PHI_MAX = 0.9990

# Fractiles típicos de la cátedra (valores exactos usados en el formulario).
# alpha (cola izquierda acumulada) → z.
_FRACTILES = {
    0.50: 0.0000,
    0.75: 0.6745,
    0.80: 0.8416,
    0.85: 1.0364,
    0.90: 1.2816,
    0.95: 1.6449,
    0.975: 1.9600,
    0.98: 2.0537,
    0.99: 2.3263,
    0.995: 2.5758,
    0.999: 3.0902,
}


def fmt_z(z: float) -> float:
    """z redondeado a 2 decimales, como se busca en la tabla."""
    return round(z, 2)


def phi(z: float) -> float:
    """Φ(z) = P(Z ≤ z) leído de la tabla de la cátedra.

    z se redondea a 2 decimales. Para z < 0 usa Φ(−z) = 1 − Φ(z).
    Para |z| > 3.09 devuelve 0.9990 / 0.0010 (tope de la tabla).
    """
    if z < 0:
        return round(1.0 - phi(-z), 4)
    z = round(z, 2)
    if z > _Z_MAX:
        return _PHI_MAX
    i100 = int(round(z * 100))                # ej. 0.67 → 67
    tenths = i100 // 10                        # fila (0..30): 67 → 6
    hundredths = i100 % 10                     # columna (0..9): 67 → 7
    row = _ROWS.get(tenths)
    if row is None:
        return _PHI_MAX
    return row[hundredths]


def phi_pdf(z: float) -> float:
    """Densidad normal estándar φ(z) = (1/√2π)·e^(−z²/2).

    La tabla de la cátedra es de Φ (acumulada); la ordenada se calcula con la
    fórmula. Se usa en la esperanza parcial H(x) = μ·Φ(z) − σ·φ(z).
    """
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def z_critico(alpha: float) -> float:
    """z tal que Φ(z) = alpha (fractil de la Normal estándar).

    - Fractiles típicos del formulario → valor exacto de la cátedra.
    - alpha < 0.5 → −z_critico(1 − alpha) por simetría.
    - Resto → z de la tabla cuyo Φ está más cerca de alpha (z a 2 decimales).
    """
    if not (0.0 < alpha < 1.0):
        raise ValueError(f"alpha debe estar en (0, 1); recibí {alpha}")
    if abs(alpha - 0.5) < 1e-12:
        return 0.0
    # Fractil típico (tolerancia chica para aceptar 0.90, 0.95, etc.).
    for a, z in _FRACTILES.items():
        if abs(alpha - a) < 1e-6:
            return z
    if alpha < 0.5:
        return -z_critico(round(1.0 - alpha, 6))
    # Búsqueda en la tabla: z cuyo Φ esté más cerca de alpha.
    best_z, best_err = _Z_MAX, abs(_PHI_MAX - alpha)
    for tenths, row in _ROWS.items():
        for hundredths, val in enumerate(row):
            err = abs(val - alpha)
            if err < best_err:
                best_err = err
                best_z = tenths / 10.0 + hundredths / 100.0
    return round(best_z, 2)


__all__ = ["phi", "phi_pdf", "z_critico", "fmt_z"]
