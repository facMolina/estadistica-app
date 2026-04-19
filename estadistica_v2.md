# Sprint v2 — análisis, decisiones y backlog

**Fecha de cierre:** 2026-04-18.
**Versión de la app:** cubre Temas I–VII de la cátedra Dopazo (UADE) + el corpus
hard de los PDFs de final 2026.

## Objetivo del sprint

Al arrancar v2 había dos gaps operativos:

1. El parser regex se pegaba en enunciados tipo final (PMF casera con
   normalizador `k`, Bayes + Pascal encadenado, suma de normales con
   coeficientes). Coverage de la guía estaba en 31/180 `complete`.
2. No había un flujo de preguntas teóricas. El usuario tenía que buscar en los
   PDFs manualmente.

Requisitos fuertes del usuario:

- **Invisibilidad total**: nada del stack de razonamiento local (modelos
  Ollama, LLM, RAG, embeddings, citas de fuentes) puede filtrar a la UI.
- **Offline garantizado**: todo corre contra `127.0.0.1`; la app sigue
  funcionando aunque el servicio local no esté arriba.
- **Zero regresión**: los 4 modos ya existentes deben seguir funcionando
  exactamente como antes.

## Gap analysis — corpus

### Coverage regex Sprint 10

Matriz por tema del parser regex, baseline:

| Tema | Total | OK | Follow-up | Error |
|------|------:|---:|----------:|------:|
| I    |     5 |  5 |         0 |     0 |
| II   |    31 |  2 |        29 |     0 |
| III  |    33 | 17 |        16 |     0 |
| IV   |    27 |  1 |        26 |     0 |
| V    |    27 |  1 |        26 |     0 |
| VI   |    40 |  2 |        38 |     0 |
| VII  |    17 |  3 |        14 |     0 |
| **TOTAL** | **180** | **31** | **149** | **0** |

Los `follow_up` son mayormente "falta tabla de datos agrupados" o "falta
especificar la consulta" — situaciones donde el parser detecta contexto pero
necesita más info. No son errores.

### Corpus hard — 11 ejercicios de final

Los dos PDFs nuevos (`PRACTICA PARA FINAL -ESTA GENERAL.pdf` y
`Estadística General 1 MODELO 2026.pdf`) traen 11 ejercicios clasificados así:

| Ejercicio | Tipo | Resolución |
|-----------|------|------------|
| Modelo 2026 #4 | PMF casera `P(X=x) = (x+2)/k` | **Resoluble v2** — CustomPMF + parser regex. |
| Modelo 2026 #2b | P(rango \| condición) sobre datos agrupados | **Resoluble v2** — fallback LLM identifica `grouped_conditional`. |
| Modelo 2026 #5 | Bayes + Pascal inverso encadenado | **Backlog v3** — requiere nuevo `compound_type=bayes_then_pascal`. |
| Modelo 2026 #1, #3 | Casos ya cubiertos | Ya funcionaba. |
| PRACTICA #8 | `3 X + 12 Y`, ambas normales | **Resoluble v2** — `_parse_tcl` con count multiplicador. |
| PRACTICA #5 | 2 Paretos en el mismo enunciado | **Backlog v3** — `compound_type=multi_distribution`. |
| PRACTICA #1,#2,#3,#4,#6,#7 | Mix binomial/poisson con giros | Parte resoluble, parte depende del fallback LLM. |

## Decisiones de arquitectura

### Regex primero, LLM solo como red de seguridad

El flujo queda:

1. `NLParser.parse(text)` corre el pipeline regex de siempre.
2. Si el resultado es `complete` → se devuelve (regex ganó, `_source: regex`).
3. Si es `need_more_info | error | unknown` → se llama al LLM local con el
   prompt `parser_fallback.txt` en JSON-mode.
4. El LLM devuelve un dict con `status/model/params/query_type/query_params/confidence`.
5. `_validate_llm_output()` chequea: status en
   {`complete`, `need_more_info`}, confidence ≥ 0.6 (solo si complete), modelo
   en `IMPLEMENTED_MODELS` (salvo modos especiales). Si no pasa → se devuelve
   el resultado regex original. **Cero regresión garantizada.**

### Invisibilidad como gate de cierre

Tres capas de defensa:

- **Prompt**: `llm/prompts/theory_answer.txt` tiene reglas absolutas de
  "prohibido mencionar fuentes/PDFs/páginas/stack".
- **Fallback silencioso**: si el servicio cae, la app responde con el texto
  genérico `"Respuesta no disponible momentáneamente."` — sin banner, sin
  explicación técnica, sin botón especial.
- **Test**: `tests/test_ui_invisibility.py` escanea los 14 archivos de UI y
  los prompts buscando las strings prohibidas (`ollama`, `llm`, `ia local`,
  `📚`, `fuente:`, etc.). Cierra el sprint solo si pasa.

### RAG — minimal y local

- PDFs de `TEORIA/` + `MACHETE.md` partidos en chunks de ~400 palabras con
  overlap de 80.
- Embeddings via `nomic-embed-text` (Ollama). Fallback BM25-lite si el servicio
  no está.
- Persistencia en `theory/_cache/rag_index.pkl` con invalidación por hash de
  mtime+size de los PDFs.
- No se usa `faiss` — la cantidad de chunks (~230) no lo justifica; coseno en
  Python puro es suficiente.

### CustomPMF sin LLM

El ejercicio de PMF casera no requiere razonamiento — solo álgebra de
normalización. Se resuelve con `eval()` sobre una expresión string en un
namespace restringido:

```python
_SAFE_FUNCS = {
    "abs": abs, "min": min, "max": max, "round": round,
    "sqrt": math.sqrt, "exp": math.exp, "log": math.log,
    "factorial": math.factorial, "pi": math.pi, "e": math.e,
}
```

Se calcula `k = Σ f(x) con k=1` (asumiendo que `k` aparece como divisor o
factor lineal) y se normaliza el PMF. Luego `mean`, `variance`, `probability`
salen directo.

## Riesgos identificados + mitigación

| Riesgo | Mitigación |
|---|---|
| Servicio local caído el día del examen | Todo lo que anda hoy sigue andando. Fallback del parser y texto genérico en Consultas Teóricas. |
| `qwen2.5:14b` no entra en RAM | Fallback automático a `qwen2.5:7b` si el primary no está pulled. |
| RAG devuelve pasajes irrelevantes → alucinaciones | Prompt obliga "si no sabés, decí que no tenés info suficiente". |
| Cobertura regex cae | Suite de regresión v2 falla si `coverage_corpus < 31/180`. |
| LLM filtra menciones a sí mismo a la UI | Prompt de sistema + gate de invisibilidad en los archivos de UI. Defensa en 2 capas. |

## Resultados finales

- **Tests**: 8 suites corridas por el orquestador `test_regression_v2.py`.
  Con servicio local arriba: 8/8 OK. Sin servicio: 6/8 OK + 2 skipped
  (ollama_client, theory_flow — skipean correctamente).
- **Coverage corpus**: ≥ 31/180 mantenido (baseline Sprint 10). El fallback LLM
  no se mide en el test porque es no-determinístico; se valida con el
  checklist manual.
- **UI invisibility gate**: 4/4 OK — ningún archivo de UI menciona el stack.
- **Nuevos modelos**: CustomPMF registrado en `model_catalog.py`.
- **Nuevo modo**: `Consultas Teóricas` disponible en el radio del sidebar.

## Backlog post-v2 (Sprint v3 candidato)

| Feature | Prioridad | Notas |
|---------|-----------|-------|
| `compound_type=bayes_then_pascal` | Alta | Modelo 2026 #5 — encadenar solver. |
| `compound_type=multi_distribution` (2 Paretos, 2 Normales, etc.) | Alta | PRACTICA #5. |
| UI para CustomPMF (`st.text_input` + `st.data_editor`) | Media | Hoy solo se expone via NL parser. |
| Exportar el machete desde la UI | Baja | Más que nada para edición del usuario. |
| Evaluación de fallback LLM en test automatizado | Media | Requiere snapshots para determinismo. |
| Ampliar corpus a los 8 PDFs de TEORIA completos | Media | Hoy el RAG sí los cubre; falta validar recall. |
| Aproximaciones nuevas (Pascal→Normal, Hiper→Normal) | Baja | Pedir de la cátedra si las usan. |

## Archivos que toca v2

**Nuevos**

- `APP/llm/__init__.py`, `APP/llm/ollama_client.py`
- `APP/llm/prompts/parser_fallback.txt`, `APP/llm/prompts/theory_answer.txt`
- `APP/theory/__init__.py`, `APP/theory/machete_builder.py`,
  `APP/theory/rag_index.py`, `APP/theory/answerer.py`
- `APP/ui/components/theory_ui.py`
- `APP/models/discrete/custom_pmf.py`
- `APP/scripts/bootstrap.bat`
- `APP/tests/test_ollama_client.py`, `APP/tests/test_parser_llm_fallback.py`,
  `APP/tests/test_theory_flow.py`, `APP/tests/test_ui_invisibility.py`,
  `APP/tests/test_regression_v2.py`,
  `APP/tests/MANUAL_REGRESSION_CHECKLIST.md`
- `TEORIA/MACHETE.md`
- `estadistica_v2.md` (este archivo)

**Modificados**

- `APP/interpreter/nl_parser.py` — fallback LLM + CustomPMF + TCL coeficientes.
- `APP/app_streamlit.py` — modo nuevo `Consultas Teóricas`.
- `APP/config/settings.py` — flags del servicio local.
- `APP/config/model_catalog.py` — `CustomPMF`.
- `APP/requirements.txt` — `requests`.
- `APP/CLAUDE.md`, `CLAUDE.md` raíz.

## Pendientes explícitos (no son errores, son scope decisions)

- No se creó una UI dedicada para `CustomPMF`. Hoy se opera solo desde el
  text-area del intérprete NL. Queda en backlog.
- No se integraron los compound types `bayes_then_pascal` y
  `multi_distribution`. Están en backlog v3.
- El test del corpus hard (11 ejercicios de los PDFs nuevos) no se agregó como
  suite automática porque depende del fallback LLM y ese camino es
  no-determinístico. La validación de esos 11 queda en el checklist manual.
