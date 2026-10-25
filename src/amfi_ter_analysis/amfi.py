"""Download and read the AMFI TER workbook."""

from __future__ import annotations

import datetime as dt
import io

import pandas as pd
import requests

API_URL = "https://www.amfiindia.com/api/populate-te-rdata-revised"
KEY = "NSDL Scheme Code"
REQUIRED = [
    KEY,
    "Scheme Name",
    "TER Date",
    "Regular Plan - Base TER (%)",
    "Direct Plan - Base TER (%)",
]


def download(month: dt.date | None = None, session: requests.Session | None = None, timeout: int = 60) -> bytes:
    """Download the TER workbook for `month` (default: the current month)."""
    month = month or dt.date.today()
    session = session or requests.Session()
    params = {"MF_ID": "All", "Month": f"{month:%m-%Y}", "strCat": "-1", "strType": "-1", "excel": "true"}
    response = session.get(API_URL, params=params, headers={"User-Agent": "Mozilla/5.0 Chrome/120.0"}, timeout=timeout)
    response.raise_for_status()
    if not response.content.startswith(b"PK"):
        raise ValueError("AMFI did not return an xlsx workbook")
    return response.content


def parse_workbook(content: bytes) -> pd.DataFrame:
    return validate(pd.read_excel(io.BytesIO(content)))


def _canonical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """AMFI has called the base column both 'Base TER (%)' and 'Base Expense Ratio (BER) (%)'."""
    rename = {}
    for plan in ("Regular", "Direct"):
        target = f"{plan} Plan - Base TER (%)"
        if target in df.columns:
            continue
        for column in df.columns:
            name = str(column).lower()
            if name.startswith(plan.lower()) and "base" in name:
                rename[column] = target
                break
    return df.rename(columns=rename)


def validate(df: pd.DataFrame) -> pd.DataFrame:
    df = _canonical_columns(df)
    missing = [column for column in REQUIRED if column not in df.columns]
    if missing:
        raise ValueError(f"TER data is missing columns: {missing}")
    df = df.copy()
    df["TER Date"] = pd.to_datetime(df["TER Date"], errors="coerce")
    # The workbook holds one row per scheme per day; the latest row is the current TER.
    df = df.sort_values("TER Date", kind="stable", na_position="first").drop_duplicates(subset=[KEY], keep="last")
    for column in df.columns:
        if column.endswith("(%)"):
            df[column] = pd.to_numeric(df[column], errors="coerce")
    return df.sort_values(KEY).reset_index(drop=True)
