# Manual regression checklist — Sprint v2

Recorrido manual de los 5 modos de la app. Marcá cada ítem verde después
de probarlo. El sprint cierra solo cuando están todos OK.

## Preparación

1. Desde `APP/`, correr `C:\Python314\python -m streamlit run app_streamlit.py`.
2. Abrir `http://localhost:8501`.

## Flujos

1. [ ] Modo **Modelos de Probabilidad** → Binomial `n=12, p=0.45, r=4` → `F(4) = 0.3044`.
2. [ ] Intérprete NL: escribir `Fb(4/12;0.45)` → auto-fill y resultado idéntico al #1.
3. [ ] Modo **Datos Agrupados** → cargar 5 intervalos → media y mediana calculadas.
4. [ ] Modo **Probabilidad** → Bayes con 3 hipótesis → posteriors suman 1.
5. [ ] Multinomial (`n=10, p=[0.2, 0.3, 0.5], r=[2, 3, 5]`) → `0.08505`.
6. [ ] TCL → 30 Bi(1, 0.5) con `count=30` → `E(S)=15`, `V(S)=7.5`, `P(S ≤ 10)` ≈ 0.0339.
7. [ ] NL: `tema III ejercicio 8` → muestra enunciado desde el PDF y resultado.
8. [ ] Tab "Aproximaciones" con `Bi(100, 0.6)` → Normal aparece con ✅.
9. [ ] Modo **Consultas Teóricas** → `"¿qué es la distribución binomial?"` → respuesta con LaTeX.
10. [ ] Consultas Teóricas follow-up: `"dame un ejemplo"` → usa memoria, respuesta coherente.
11. [ ] Modelo 2026 ej 4 (PMF custom): escribir `P(X=x) = (x+2)/k para x ∈ {0,1,2,3}. Hallar E(X)` → auto-fill CustomPMF.
12. [ ] Modelo 2026 ej 2b (grouped conditional): el parser pide tabla coherente.
13. [ ] PRACTICA ej 8 (3 mesas + 12 sillas): detecta TCL con counts `3` y `12`.
14. [ ] Consultas Teóricas con el servicio local caído → muestra literal `"Respuesta no disponible momentáneamente."` y nada más.
15. [ ] Modo Modelos de Probabilidad sigue funcionando si el servicio local está caído (regex-only).
16. [ ] Continuo Normal: `μ=10 σ=2`, `P(X < 12)` ≈ 0.8413.
17. [ ] Continuo Gamma: `r=2, λ=1`, `P(X < 2)` ≈ 0.5940.
18. [ ] Compound hiper+binomial (ejemplo de la guía): respuesta coincide con Resp.
19. [ ] Nivel de detalle 1/2/3: cambia el número de pasos renderizados en Binomial.
20. [ ] CSV download de `full_table()` funciona en Binomial y Poisson.

## Criterio de cierre

- 20/20 ítems OK.
- `python tests/test_regression_v2.py` → todas las suites OK o con SKIP coherente.
- No aparece ninguna mención visible al stack (Ollama, LLM, IA local, fuentes, PDFs, páginas) en ninguno de los 5 modos.
