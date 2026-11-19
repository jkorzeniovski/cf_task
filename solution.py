import re

import pandas as pd


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:

    if not re.fullmatch(r"[A-Za-z_]+", new_column): #validation for new column name - only letters and _ 
        return pd.DataFrame([])

    if not re.fullmatch(r"\s*[A-Za-z_]+\s*[+\-*]\s*([A-Za-z_]+\s*)*", role): #validation for role - only letters, _+-* and spaces before, after and between
        return pd.DataFrame([])

    labels = re.findall(r"[A-Za-z_]+", role) #checking if labels are actual names of columns in df
    for label in labels:
        if label not in df.columns:
            return pd.DataFrame([])


    try:
        final = df.eval(role)
    except Exception:
        return pd.DataFrame([])

    output = df.copy()
    output[new_column] = final
    return output