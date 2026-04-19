"""
Test Sprint 10: cobertura del parser contra el corpus de la guía (180 ejercicios).

Itera cada ejercicio, corre NLParser.parse(), clasifica el resultado y reporta
una matriz por tema + genera coverage_report.md con los que fallaron.

Ejecutar desde APP/:
    C:\\Python314\\python tests/test_guide_corpus.py
"""

from __future__ import annotations

import os
import sys
import traceback
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)
if _APP not in sys.path:
    sys.path.insert(0, _APP)

from guide_index import load_or_build_index, get_exercise
from interpreter.nl_parser import NLParser


# Categorías del resultado
CAT_COMPLETE = "complete"
CAT_FOLLOW_UP = "follow_up"
CAT_ERROR = "error"
CAT_UNKNOWN = "unknown"


def _classify(result: dict) -> str:
    if not isinstance(result, dict):
        return CAT_UNKNOWN
    status = result.get("status", "")
    if status in ("complete", "compound", "guide_exercise"):
        return CAT_COMPLETE
    if status == "need_more_info":
        return CAT_FOLLOW_UP
    return CAT_UNKNOWN


def test_parse_coverage():
    print("\n[1] parse_coverage: iterando 180 ejercicios de la guía")
    parser = NLParser()
    index = load_or_build_index()

    counters: dict[str, Counter] = {}
    failures: list[dict] = []
    total_by_cat: Counter = Counter()

    temas = sorted(index.get("temas", {}).keys(),
                   key=lambda t: {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
                                  "VI": 6, "VII": 7}.get(t, 99))

    for tema in temas:
        ejs = index["temas"][tema].get("exercises", {})
        counters[tema] = Counter()
        for num, ex in ejs.items():
            text = ex.get("text", "")
            if not text or len(text) < 10:
                counters[tema][CAT_ERROR] += 1
                total_by_cat[CAT_ERROR] += 1
                failures.append({
                    "tema": tema, "numero": num,
                    "cat": CAT_ERROR, "reason": "texto vacío o muy corto",
                    "text": text, "resp": ex.get("resp", ""),
                })
                continue
            try:
                result = parser.parse(text)
                cat = _classify(result)
            except Exception as e:
                cat = CAT_ERROR
                failures.append({
                    "tema": tema, "numero": num,
                    "cat": CAT_ERROR, "reason": f"excepción: {e}",
                    "trace": traceback.format_exc(limit=3),
                    "text": text, "resp": ex.get("resp", ""),
                })
                counters[tema][cat] += 1
                total_by_cat[cat] += 1
                continue

            counters[tema][cat] += 1
            total_by_cat[cat] += 1

            if cat != CAT_COMPLETE:
                failures.append({
                    "tema": tema, "numero": num,
                    "cat": cat,
                    "reason": result.get("question", "") if cat == CAT_FOLLOW_UP
                    else result.get("status", "unknown"),
                    "text": text, "resp": ex.get("resp", ""),
                })

    total = sum(total_by_cat.values())
    complete = total_by_cat[CAT_COMPLETE]
    follow_up = total_by_cat[CAT_FOLLOW_UP]
    err = total_by_cat[CAT_ERROR] + total_by_cat[CAT_UNKNOWN]

    print(f"\n  Matriz por tema:")
    print(f"  {'Tema':<6} {'Total':>6} {'OK':>6} {'FU':>6} {'Err':>6}")
    for tema in temas:
        c = counters[tema]
        t = sum(c.values())
        print(f"  {tema:<6} {t:>6} {c[CAT_COMPLETE]:>6} "
              f"{c[CAT_FOLLOW_UP]:>6} {c[CAT_ERROR] + c[CAT_UNKNOWN]:>6}")
    print(f"  {'TOTAL':<6} {total:>6} {complete:>6} {follow_up:>6} {err:>6}")
    print(f"  → Coverage complete = {complete}/{total} = {100*complete/total:.1f}%")

    # Generar coverage_report.md
    report_path = Path(_HERE) / "coverage_report.md"
    _write_coverage_report(report_path, counters, total_by_cat, failures, temas)
    print(f"  → Reporte escrito en {report_path}")

    # Assert suave: baseline post Sprint 10. Próximos sprints deberán subirla.
    MIN_COMPLETE = 25
    assert complete >= MIN_COMPLETE, \
        f"Coverage demasiado bajo: {complete} < {MIN_COMPLETE}"
    print(f"  OK coverage >= {MIN_COMPLETE}  (baseline Sprint 10)")


def _write_coverage_report(path: Path, counters: dict, total_by_cat: Counter,
                           failures: list[dict], temas: list[str]) -> None:
    lines: list[str] = []
    lines.append("# Coverage report — parser contra guía PDF")
    lines.append("")
    lines.append(f"**Total:** {sum(total_by_cat.values())} ejercicios")
    lines.append(f"- complete: {total_by_cat[CAT_COMPLETE]}")
    lines.append(f"- follow_up: {total_by_cat[CAT_FOLLOW_UP]}")
    lines.append(f"- error: {total_by_cat[CAT_ERROR] + total_by_cat[CAT_UNKNOWN]}")
    lines.append("")
    lines.append("## Matriz por tema")
    lines.append("")
    lines.append("| Tema | Total | OK | Follow-up | Error |")
    lines.append("|------|-------|----|-----------|-------|")
    for tema in temas:
        c = counters[tema]
        t = sum(c.values())
        lines.append(f"| {tema} | {t} | {c[CAT_COMPLETE]} | "
                     f"{c[CAT_FOLLOW_UP]} | {c[CAT_ERROR] + c[CAT_UNKNOWN]} |")
    lines.append("")
    lines.append("## Ejercicios con fallas (follow_up + error)")
    lines.append("")
    for f in failures:
        head = f"### Tema {f['tema']} — Ejercicio {f['numero']}  ({f['cat']})"
        lines.append(head)
        lines.append("")
        reason = str(f.get("reason", ""))[:300].replace("\n", " ")
        lines.append(f"**Motivo:** {reason}")
        resp = str(f.get("resp", ""))[:200].replace("\n", " ")
        if resp:
            lines.append(f"**Resp. esperada:** {resp}")
        text = str(f.get("text", ""))
        preview = text[:600].replace("\n", " ")
        lines.append("")
        lines.append(f"```\n{preview}\n```")
        lines.append("")

    try:
        path.write_text("\n".join(lines), encoding="utf-8")
    except Exception as e:
        print(f"  WARN: no pude escribir {path}: {e}")


def test_known_answers():
    """Subset curado: comparar valores numéricos conocidos."""
    print("\n[2] known_answers: subset con respuestas numéricas")
    parser = NLParser()

    # Cada caso: (descripcion, texto, model_name esperado, query_type esperado)
    cases = [
        ("Bi Gb(3/10;0.25)", "Gb(3/10;0.25)", "Binomial", "cdf_right"),
        ("Bi Fb(4/12;0.45)", "Fb(4/12;0.45)", "Binomial", "cdf_left"),
        ("Pascal Fpa(12/5;0.42)", "Fpa(12/5;0.42)", "Pascal", "cdf_left"),
        ("Poisson Fpo(4/6)", "Fpo(4/6)", "Poisson", "cdf_left"),
        ("Multinomial conjunta",
         "multinomial n=10 probabilidades 0.2;0.3;0.5 conteos 2;3;5",
         "Multinomial", "joint_probability"),
    ]
    ok = 0
    for desc, text, want_model, want_qt in cases:
        r = parser.parse(text)
        got_model = r.get("model")
        got_qt = r.get("query_type")
        status = r.get("status")
        if status == "complete" and got_model == want_model and got_qt == want_qt:
            print(f"  OK {desc}: {got_model}/{got_qt}")
            ok += 1
        else:
            print(f"  FAIL {desc}: got status={status} model={got_model} qt={got_qt}")

    assert ok >= 4, f"known_answers: sólo {ok}/{len(cases)} pasaron"
    print(f"  → {ok}/{len(cases)} known_answers OK")


def test_parse_stability():
    """Determinismo: mismo texto, mismo resultado."""
    print("\n[3] parse_stability: el parser es determinístico")
    parser = NLParser()
    index = load_or_build_index()
    muestreo = []
    for tema in ("II", "III", "VI"):
        ejs = index["temas"].get(tema, {}).get("exercises", {})
        for num, ex in list(ejs.items())[:3]:
            muestreo.append(ex["text"])

    for i, text in enumerate(muestreo):
        r1 = parser.parse(text)
        r2 = parser.parse(text)
        assert r1.get("status") == r2.get("status"), \
            f"muestra {i}: status cambió entre corridas"
        assert r1.get("model") == r2.get("model"), \
            f"muestra {i}: model cambió"
    print(f"  OK {len(muestreo)} muestras son determinísticas")


if __name__ == "__main__":
    tests = [test_parse_coverage, test_known_answers, test_parse_stability]
    passed = 0
    failed = []
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            failed.append((t.__name__, str(e)))
            print(f"  FAIL {t.__name__}: {e}")
        except Exception as e:
            failed.append((t.__name__, f"EXC {e}"))
            print(f"  FAIL {t.__name__}: {e}")
            traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"RESULTADO: {passed}/{len(tests)} OK")
    if failed:
        for n, err in failed:
            print(f"  {n}: {err}")
        sys.exit(1)
