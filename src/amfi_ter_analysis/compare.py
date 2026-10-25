"""Compare two TER snapshots."""

from __future__ import annotations

import pandas as pd

from .amfi import KEY

PLANS = ("Regular", "Direct")
EPSILON = 1e-9


def compare_plan(old: pd.DataFrame, new: pd.DataFrame, plan: str) -> pd.DataFrame:
    """Schemes whose base TER changed for `plan`. A positive reduction means the TER fell."""
    column = f"{plan} Plan - Base TER (%)"
    merged = old[[KEY, column]].merge(
        new[[KEY, "Scheme Name", "TER Date", column]], on=KEY, suffixes=("_old", "_new")
    )
    reduction = merged[f"{column}_old"] - merged[f"{column}_new"]
    changed = merged[reduction.abs() > EPSILON].copy()
    changed["TER Reduction (%)"] = (reduction[changed.index]).round(4)
    out = changed.rename(
        columns={
            f"{column}_old": f"Old {column}",
            f"{column}_new": f"New {column}",
            "TER Date": "TER Date (Change)",
        }
    )
    out["TER Date (Change)"] = out["TER Date (Change)"].dt.strftime("%Y-%m-%d")
    ordered = [KEY, "Scheme Name", f"Old {column}", f"New {column}", "TER Date (Change)", "TER Reduction (%)"]
    return out[ordered].sort_values("TER Reduction (%)", key=lambda s: s.abs(), ascending=False).reset_index(drop=True)


def compare_all(old: pd.DataFrame, new: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {plan: compare_plan(old, new, plan) for plan in PLANS}


def new_schemes(old: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    return new[~new[KEY].isin(old[KEY])][[KEY, "Scheme Name"]].reset_index(drop=True)
