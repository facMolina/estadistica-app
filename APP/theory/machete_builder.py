"""Generador del archivo MACHETE.md (resumen teórico indexable).

Estrategia simple: copia el contenido editable de `theory/machete_seed.md`
(fuente única, sin escaping de Python) a `TEORIA/MACHETE.md`. El usuario puede
editar `MACHETE.md` libremente después; el RAG lo indexa como cualquier otra
fuente. `force=True` (usado por los tests) sincroniza desde el seed — por eso
el seed, no este módulo, es la fuente de verdad del contenido.
"""

from __future__ import annotations

import os

from config.settings import MACHETE_PATH

_SEED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "machete_seed.md")


def build_machete(force: bool = False) -> str:
    """Escribe MACHETE.md si no existe (o si force=True). Devuelve la ruta."""
    if os.path.exists(MACHETE_PATH) and not force:
        return MACHETE_PATH
    os.makedirs(os.path.dirname(MACHETE_PATH), exist_ok=True)
    with open(_SEED_PATH, encoding="utf-8") as f:
        seed = f.read()
    with open(MACHETE_PATH, "w", encoding="utf-8") as f:
        f.write(seed)
    return MACHETE_PATH


if __name__ == "__main__":
    p = build_machete(force=True)
    print(f"Machete escrito en: {p}")
