"""Build the notification text for TER changes."""

from __future__ import annotations

import datetime as dt

import pandas as pd

from .amfi import KEY

MAX_ROWS = 15
MAX_CHARS = 3800  # Google Chat rejects messages near 4096 characters


def build_message(changes: dict[str, pd.DataFrame], added: pd.DataFrame, today: dt.date) -> str:
    lines = [f"AMFI TER changes for {today:%d %b %Y}"]
    total = sum(len(frame) for frame in changes.values())
    if total == 0 and added.empty:
        lines.append("No base TER changes since the previous run.")
        return "\n".join(lines)

    for plan, frame in changes.items():
        lines.append("")
        lines.append(f"{plan} plan: {len(frame)} scheme(s) changed")
        old_col, new_col = f"Old {plan} Plan - Base TER (%)", f"New {plan} Plan - Base TER (%)"
        for _, row in frame.head(MAX_ROWS).iterrows():
            lines.append(
                f"- {row['Scheme Name']}: {row[old_col]:.2f}% -> {row[new_col]:.2f}% ({-row['TER Reduction (%)']:+.2f})"
            )
        if len(frame) > MAX_ROWS:
            lines.append(f"... and {len(frame) - MAX_ROWS} more (see the CSV in data/output)")

    if not added.empty:
        lines.append("")
        lines.append(f"{len(added)} new scheme(s) listed, for example: " + "; ".join(added["Scheme Name"].head(5)))

    message = "\n".join(lines)
    return message if len(message) <= MAX_CHARS else message[: MAX_CHARS - 20] + "\n... (truncated)"


def summary(changes: dict[str, pd.DataFrame], added: pd.DataFrame, today: dt.date) -> dict:
    return {
        "date": today.isoformat(),
        "regular_changes": len(changes.get("Regular", [])),
        "direct_changes": len(changes.get("Direct", [])),
        "new_schemes": len(added),
        "key": KEY,
    }
