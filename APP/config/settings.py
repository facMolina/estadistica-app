"""Constantes globales y configuracion."""

import math

# Constante de Euler-Mascheroni
EULER_MASCHERONI = 0.5772156649015329

# Pi
PI = math.pi

# Niveles de detalle
DETAIL_MAX = 3        # Maximo detalle: cada sub-calculo
DETAIL_INTERMEDIATE = 2  # Intermedio: formulas con valores reemplazados
DETAIL_BASIC = 1      # Basico: solo formula y resultado

DETAIL_LABELS = {
    DETAIL_MAX: "Maximo detalle",
    DETAIL_INTERMEDIATE: "Detalle intermedio",
    DETAIL_BASIC: "Formula y resultado",
}

# Tolerancia para comparaciones numericas
EPSILON = 1e-10

# Maximo de terminos para sumatorias infinitas (Poisson, Pascal)
MAX_SUMMATION_TERMS = 1000

# Ruta base del proyecto
import os
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEORIA_DIR = os.path.join(os.path.dirname(APP_DIR), "TEORIA")
GUIA_PATH = os.path.join(os.path.dirname(APP_DIR),
    "Guia Problemas Estadística General - Probabilidad y Estadística - UADE (1).pdf")
SESSION_CONFIG_PATH = os.path.join(APP_DIR, ".session_config.json")
