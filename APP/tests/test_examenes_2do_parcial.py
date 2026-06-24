"""
Tests de regresion: ejercicios reales/modelo del 2do parcial (continuas,
Proceso de Poisson, TCL, Bayes continuo).

Fuentes (carpeta EJEMPLOS/, fuera de APP/):
  - "Estadistica General MODELO 2do Parcial - 2025.md"      (botellas)
  - "Estadistica General MODELO PARCIAL 2 (2-2025).md"      (fintech)
  - Segundo_Parcial/*.jpeg 2024 (combustible/generador/graduados)
  - Segundo_Parcial/*.jpeg Segundo Recuperatorio 2023 (fosforos/sierra/muebles)

Donde hay un valor de la catedra ya verificado (FORMULARIO / plan), se
assertea con tolerancia ajustada. Donde NO hay clave oficial (ejercicios
compuestos con datos parcialmente ambiguos en la foto), se calcula y se
imprime el valor para validacion manual -- no se assertea un numero externo.

Ejecutar desde APP/:
    C:\\Python314\\python tests\\test_examenes_2do_parcial.py
"""

from __future__ import annotations

import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)
if _APP not in sys.path:
    sys.path.insert(0, _APP)

from models.continuous.normal import Normal
from models.continuous.gamma import Gamma
from models.continuous.pareto import Pareto
from models.continuous.exponencial import Exponencial
from models.continuous.uniforme import Uniforme
from models.continuous import derivations as deriv
from calculation.normal_table import phi as phi_table, z_critico
from tcl.sum_of_rvs import SumOfRVs, Component
from probability.bayes_continuo import bayes_continuo_tail_right, bayes_continuo_same_model_thresholds


TOL_STRICT = 1e-6
TOL_LOOSE = 5e-3   # tolera la cuantizacion de la tabla Z (z a 2 decimales)


def _assert_close(got, expected, tol, label):
    err = abs(got - expected)
    assert err <= tol, f"{label}: |{got:.6f} - {expected:.6f}| = {err:.2e} > tol={tol}"
    print(f"  OK {label}: got={got:.6f} expected={expected:.6f}")


# ---------------------------------------------------------------------
# 1. Botellas (MODELO 2do Parcial 2025)
# ---------------------------------------------------------------------

def test_botellas_2025():
    print("\n[1] Botellas 2025 — Normal/Gamma/Pareto desde datos indirectos")

    # mu=600, "solo se llena menos de 561.55345ml el 10% de las veces" -> F(x0)=0.10
    m, res = deriv.normal_from_one_percentile(600, 561.55345, 0.10)
    _assert_close(m.sigma, 30.0, 0.01, "botellas sigma derivado ~30")

    n = Normal(m.mu, m.sigma)
    g620 = n.cdf_right(620).final_value
    _assert_close(g620, 0.2514, TOL_STRICT, "P(X>620) tabla = 0.2514")

    # rango con borde fractil: entre la media y el octavo decil
    mu = n.mean().final_value
    x08 = n.fractile(0.80).final_value
    rango = n.cdf_left(x08).final_value - n.cdf_left(mu).final_value
    print(f"  Pr(mu <= X <= x(0.8)) = {rango:.4f}  (mu={mu}, x(0.8)={x08:.4f})")
    assert 0.0 < rango < 0.5, "el rango entre la media y un fractil debe ser una proporcion chica"

    # demanda electrica: Gamma media=16 MWh, varianza=4
    gm, _ = deriv.gamma_from_mean_variance(16, 4)
    _assert_close(gm.lam, 4.0, TOL_STRICT, "Gamma demanda lambda = mu/var")
    _assert_close(gm.r, 64.0, TOL_STRICT, "Gamma demanda r = mu^2/var")

    # 2 generadores de 9 MWh c/u = 18 MWh; demanda total = Gamma(r=128, lam=4) exacta
    # (misma lambda -> la suma de Gammas es exacta, no requiere TCL)
    demanda_total = Gamma(r=2 * gm.r, lam=gm.lam)
    p_no_cumple = demanda_total.cdf_right(18).final_value
    print(f"  P(no se cubre demanda con 2 generadores de 9MWh) = {p_no_cumple:.4f}  (sin clave oficial, validar a mano)")
    assert 0.0 <= p_no_cumple <= 1.0

    # stock: Pareto media=25 (miles six-packs), moda=20
    pm, _ = deriv.pareto_from_mean_mode(25, 20)
    _assert_close(pm.theta, 20.0, TOL_STRICT, "Pareto stock theta = moda")
    _assert_close(pm.b, 5.0, TOL_STRICT, "Pareto stock b = mu/(mu-moda)")

    p = Pareto(pm.theta, pm.b)
    g27 = p.cdf_right(27).final_value
    expected_g27 = (20.0 / 27.0) ** 5.0
    _assert_close(g27, expected_g27, TOL_STRICT, "P(stock>27mil) = (theta/x)^b")


# ---------------------------------------------------------------------
# 2. Fintech (MODELO PARCIAL 2, 2-2025)
# ---------------------------------------------------------------------

def test_fintech_2025():
    print("\n[2] Fintech 2025 — Normal/Gamma/Pareto + esperanza condicional")

    # password: Normal media=0.92s, 17% tarda menos de 0.82458s -> F(0.82458)=0.17
    m, _ = deriv.normal_from_one_percentile(0.92, 0.82458, 0.17)
    n = Normal(m.mu, m.sigma)
    p_espera = n.cdf_right(0.8).final_value
    print(f"  P(espera, X>0.8s) = {p_espera:.4f}")
    assert 0.0 < p_espera < 1.0

    # codigo 2FA: Gamma media=20s, varianza=5
    gm, _ = deriv.gamma_from_mean_variance(20, 5)
    _assert_close(gm.lam, 4.0, TOL_STRICT, "Gamma 2FA lambda")
    _assert_close(gm.r, 80.0, TOL_STRICT, "Gamma 2FA r")

    # transacciones: Pareto, "tarda siempre" 1 min (moda) y media 1.4 min
    pm, _ = deriv.pareto_from_mean_mode(1.4, 1.0)
    _assert_close(pm.theta, 1.0, TOL_STRICT, "Pareto transacciones theta = moda")
    _assert_close(pm.b, 3.5, TOL_STRICT, "Pareto transacciones b")

    p = Pareto(pm.theta, pm.b)
    g144 = p.cdf_right(1.44).final_value
    _assert_close(g144, (1.0 / 1.44) ** 3.5, TOL_STRICT, "P(transaccion>1.44min)")

    # E[X | X > media] -- formula cerrada Pareto: b*k/(b-1)
    cond = p.cond_expectation_right(1.4).final_value
    _assert_close(cond, 1.96, TOL_STRICT, "E[X|X>media] Pareto = b*mu/(b-1)")

    # monto operado: Normal, P(X>584.5824)=0.10 ; P(X<400)=0.06487
    m2, _ = deriv.normal_from_two_percentiles(584.5824, 0.90, 400, 0.06487)
    print(f"  monto operado: mu={m2.mu:.4f}, sigma={m2.sigma:.4f}")
    assert m2.sigma > 0


# ---------------------------------------------------------------------
# 3. Real 2024 — combustible (Normal directa + derivada + TCL)
# ---------------------------------------------------------------------

def test_real_2024_combustible():
    print("\n[3] Real 2024 — combustible: Normal directa/derivada + TCL")

    n = Normal(246, 25)
    g263 = n.cdf_right(263).final_value
    print(f"  P(consumo > 263) = {g263:.4f}")
    assert 0.0 < g263 < 1.0

    x_080 = n.fractile(0.80).final_value
    print(f"  consumo superado solo el 20% de los dias = x(0.80) = {x_080:.4f}")

    # dias frios: media sube 9%, 61% de dias frios no superan 274.28502 litros
    mu_frio = 246 * 1.09
    m, _ = deriv.normal_from_one_percentile(mu_frio, 274.28502, 0.61)
    print(f"  sigma_frio = {m.sigma:.4f}  vs sigma_habitual = 25  "
          f"({'menor' if m.sigma < 25 else 'mayor'} dispersion en dias frios)")
    assert m.sigma > 0

    # TCL: 17 dias frios consecutivos, P(suma <= 4605)
    s = SumOfRVs([Component("dia_frio", mean=mu_frio, variance=m.sigma ** 2, count=17)])
    ES, VS = s.expected_value_raw(), s.variance_raw()
    res = s.probability("cdf_left", s=4605)
    expected = phi_table((4605 - ES) / math.sqrt(VS))
    _assert_close(res.final_value, expected, TOL_STRICT, "P(S17 <= 4605) via tabla Z")


# ---------------------------------------------------------------------
# 4. Real 2024 — generador electrico: Poisson process + memoryless
# ---------------------------------------------------------------------

def test_real_2024_generador_poisson_process():
    print("\n[4] Real 2024 — generador: proceso de Poisson (memoryless + E[T])")

    lam = 1.0 / 36.0  # 1 falla cada 36 horas
    e = Exponencial(lam)

    # memoryless: ya funciono 2 dias sin detenerse; P(no se detenga en las prox 17h)
    # = P(T > 17) sin importar lo ya transcurrido
    p17 = e.cdf_right(17).final_value
    _assert_close(p17, math.exp(-17.0 / 36.0), TOL_STRICT, "P(T>17) exponencial (memoryless)")

    # E[T] hasta la 1ra desconexion, y P(T > E[T])
    mu_t = e.mean().final_value
    _assert_close(mu_t, 36.0, TOL_STRICT, "E[T] = 1/lambda = 36h")
    p_mayor_media = e.cdf_right(mu_t).final_value
    _assert_close(p_mayor_media, math.exp(-1.0), TOL_STRICT, "P(T>E[T]) = e^-1 (cualquier exponencial)")

    # E[X|X>k] = k + 1/lambda (residual de vida = memoryless)
    cond = e.cond_expectation_right(17).final_value
    _assert_close(cond, 17.0 + 36.0, TOL_STRICT, "E[T|T>17] = 17 + 1/lambda")


# ---------------------------------------------------------------------
# 5. Real 2023 (recuperatorio) — sierra electrica (Normal derivada) + ART (Pareto)
# ---------------------------------------------------------------------

def test_real_2023_sierra_y_art():
    print("\n[5] Real 2023 — sierra (Normal derivada) + ART (Pareto)")

    # reflejo: Normal media=2ms, 90% retira la mano en menos de 3ms -> F(3)=0.90
    m, _ = deriv.normal_from_one_percentile(2, 3, 0.90)
    n = Normal(m.mu, m.sigma)

    rango = n.cdf_left(1.5).final_value - n.cdf_left(1.0).final_value
    print(f"  P(1 <= tiempo_reflejo <= 1.5 ms) = {rango:.4f}")
    assert 0.0 < rango < 1.0

    # accidente si la mano no se retiro antes de los 2.8ms -> G(2.8)
    g28 = n.cdf_right(2.8).final_value
    print(f"  P(accidente) = G(2.8) = {g28:.4f}")
    assert 0.0 < g28 < 1.0

    # ART: pago minimo (moda) = 1 millon, promedio de reclamos = 4 millones
    pm, _ = deriv.pareto_from_mean_mode(4, 1)
    _assert_close(pm.theta, 1.0, TOL_STRICT, "ART Pareto theta = moda")
    _assert_close(pm.b, 4.0 / 3.0, TOL_STRICT, "ART Pareto b")
    p = Pareto(pm.theta, pm.b)
    g3 = p.cdf_right(3).final_value
    _assert_close(g3, (1.0 / 3.0) ** (4.0 / 3.0), TOL_STRICT, "P(reclamo > 3M)")


# ---------------------------------------------------------------------
# 6. Real 2023 — muebles: Gamma generadores + TCL (mesas/sillas)
# ---------------------------------------------------------------------

def test_real_2023_muebles_gamma_tcl():
    print("\n[6] Real 2023 — muebles: Gamma (consumo elec.) + TCL (carga camion)")

    # consumo de las lineas de produccion: Gamma media=22 MWh, desvio=3 (var=9)
    gm, _ = deriv.gamma_from_mean_variance(22, 9)
    print(f"  Gamma consumo: r={gm.r:.4f}, lambda={gm.lam:.4f}  (r no entero/grande -> Wilson-Hilferty)")
    assert gm.r > 30  # confirma que se ejerce la rama Wilson-Hilferty, no Poisson exacto

    # carga de camion: 3 mesas N(25,25) + 12 sillas N(9,4); gasoil = 0.1 L/km/kg, viaje 3km
    # P(consumo de gasoil >= 50L) = P(peso_total >= 50/0.3)
    s = SumOfRVs([
        Component("Mesa", mean=25, variance=25, count=3),
        Component("Silla", mean=9, variance=4, count=12),
    ])
    ES, VS = s.expected_value_raw(), s.variance_raw()
    _assert_close(ES, 183.0, TOL_STRICT, "E(peso total) = 3*25 + 12*9")
    _assert_close(VS, 123.0, TOL_STRICT, "V(peso total) = 3*25 + 12*4")

    thresh = 50.0 / 0.3
    res = s.probability("cdf_right", s=thresh)
    expected = round(1.0 - phi_table((thresh - ES) / math.sqrt(VS)), 4)
    _assert_close(res.final_value, expected, TOL_STRICT, "P(gasoil consumido >= 50L) via tabla Z")


# ---------------------------------------------------------------------
# 7. Bayes continuo — transacciones internacionales (cola derecha, dos Pareto)
# ---------------------------------------------------------------------

def test_bayes_continuo_transacciones():
    print("\n[7] Bayes continuo — transacciones internacionales (G(x), dos Pareto)")

    dom_m, _ = deriv.pareto_from_mean_mode(1.4, 1.0)
    intl_m, _ = deriv.pareto_from_mean_mode(1.5, 1.2)
    dom = Pareto(dom_m.theta, dom_m.b)
    intl = Pareto(intl_m.theta, intl_m.b)

    bayes, res = bayes_continuo_tail_right(
        ["Domestica", "Internacional"], [0.80, 0.20], [dom, intl], 1.5,
    )
    posts = dict(bayes.posteriors())
    total = sum(posts.values())
    _assert_close(total, 1.0, TOL_STRICT, "posteriores suman 1")

    # verificacion independiente: posterior_i proporcional a prior_i * G_i(1.5)
    g_dom = dom.cdf_right(1.5).final_value
    g_intl = intl.cdf_right(1.5).final_value
    pe = 0.80 * g_dom + 0.20 * g_intl
    _assert_close(res.final_value, pe, TOL_STRICT, "P(X>1.5) = suma de priors*G_i(1.5)")
    _assert_close(posts["Internacional"], 0.20 * g_intl / pe, TOL_STRICT, "P(internacional | X>1.5)")
    print(f"  P(internacional | X>1.5) = {posts['Internacional']:.4f}")


# ---------------------------------------------------------------------
# 8. Bayes continuo — fosforos (misma Gamma, umbral por hipotesis)
# ---------------------------------------------------------------------

def test_bayes_continuo_fosforos():
    print("\n[8] Bayes continuo — fosforos (F(t_i) de UNA Gamma, 3 grupos)")

    # tiempo de quemado del fosforo ~ Gamma media=1.5min, varianza=0.06min^2
    # (se asume varianza en minutos^2 -- la consigna original mezcla "segundos" y
    #  "minutos"; con var en segundos^2 el CV resultaria < 1%, fisicamente
    #  irreal, por eso se interpreta como min^2 -- ver nota en informe al usuario)
    gm, _ = deriv.gamma_from_mean_variance(1.5, 0.06)
    g = Gamma(gm.r, gm.lam)

    labels = ["90s (1.5min)", "1.2min", "1.6min"]
    priors = [0.15, 0.25, 0.60]
    thresholds = [1.5, 1.2, 1.6]

    bayes, res = bayes_continuo_same_model_thresholds(
        labels, priors, g, thresholds, tail="left", evidence_label="se apaga antes",
    )
    posts = dict(bayes.posteriors())
    _assert_close(sum(posts.values()), 1.0, TOL_STRICT, "posteriores suman 1")

    f_vals = [g.cdf_left(t).final_value for t in thresholds]
    pe = sum(p * f for p, f in zip(priors, f_vals))
    _assert_close(res.final_value, pe, TOL_STRICT, "P(se apaga antes) = suma priors*F(t_i)")
    print(f"  P(se apague antes de usarlo) = {res.final_value:.4f}")
    print(f"  P(grupo=1.2min | se apago antes) = {posts['1.2min']:.4f}")


# ---------------------------------------------------------------------
# 9. Esperanza condicional — formulas cerradas (Pareto, Uniforme)
# ---------------------------------------------------------------------

def test_cond_expectation_closed_forms():
    print("\n[9] Esperanza condicional — formulas cerradas")

    p = Pareto(theta=20, b=5)
    cond_r = p.cond_expectation_right(25).final_value
    _assert_close(cond_r, 5.0 * 25.0 / 4.0, TOL_STRICT, "Pareto E[X|X>k] = b*k/(b-1)")

    u = Uniforme(1, 5)
    cond_u = u.cond_expectation_right(3).final_value
    _assert_close(cond_u, (3.0 + 5.0) / 2.0, TOL_STRICT, "Uniforme E[X|X>k] = (k+b)/2")

    cond_left_u = u.cond_expectation_left(3).final_value
    _assert_close(cond_left_u, (1.0 + 3.0) / 2.0, TOL_STRICT, "Uniforme E[X|X<a] = (a+a_dom)/2")


# ---------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_botellas_2025,
        test_fintech_2025,
        test_real_2024_combustible,
        test_real_2024_generador_poisson_process,
        test_real_2023_sierra_y_art,
        test_real_2023_muebles_gamma_tcl,
        test_bayes_continuo_transacciones,
        test_bayes_continuo_fosforos,
        test_cond_expectation_closed_forms,
    ]
    passed = 0
    failed = []
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            failed.append((t.__name__, repr(e)))
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\n{'=' * 60}")
    print(f"RESULTADO: {passed}/{len(tests)} OK")
    if failed:
        for name, err in failed:
            print(f"  FAIL {name}: {err}")
        sys.exit(1)
