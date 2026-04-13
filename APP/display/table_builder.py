"""Construccion de tablas de distribucion."""

import pandas as pd
from typing import List, Dict


def build_dataframe(table_data: List[Dict]) -> pd.DataFrame:
    """Convierte la lista de dicts a un DataFrame formateado."""
    df = pd.DataFrame(table_data)
    # Redondear a 6 decimales
    numeric_cols = [c for c in df.columns if c != "r"]
    for col in numeric_cols:
        df[col] = df[col].round(6)
    return df
