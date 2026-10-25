"""Daily run: download, compare with the stored baseline, write reports, notify."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
from pathlib import Path

import pandas as pd

from . import amfi, compare, notify, report

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
BASELINE_NAME = "baseline_ter.csv.gz"
log = logging.getLogger(__name__)


def run(data_dir: Path, today: dt.date, send_notification: bool = True, current: pd.DataFrame | None = None) -> dict:
    """Execute one daily run and return its summary. `current` lets tests skip the download."""
    if current is None:
        current = amfi.parse_workbook(amfi.download(today))
    baseline_path = data_dir / BASELINE_NAME
    output_dir = data_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not baseline_path.exists():
        current.to_csv(baseline_path, index=False)
        log.info("no baseline yet; saved %d schemes as the baseline", len(current))
        return {"date": today.isoformat(), "baseline_created": True, "schemes": len(current)}

    previous = amfi.validate(pd.read_csv(baseline_path))
    changes = compare.compare_all(previous, current)
    added = compare.new_schemes(previous, current)

    for plan, frame in changes.items():
        if not frame.empty:
            frame.to_csv(output_dir / f"{plan}_Plan_TER_Changes_{today}.csv", index=False)

    message = report.build_message(changes, added, today)
    result = report.summary(changes, added, today)
    (output_dir / "latest_message.txt").write_text(message, encoding="utf-8")
    (output_dir / "latest_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    current.to_csv(baseline_path, index=False)

    has_changes = bool(result["regular_changes"] or result["direct_changes"] or result["new_schemes"])
    if send_notification and has_changes:
        result["notified"] = notify.send(message)
    log.info("summary: %s", result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="amfi-ter", description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--no-notify", action="store_true", help="write reports but do not post to Google Chat")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        run(args.data_dir, dt.date.today(), send_notification=not args.no_notify)
    except (OSError, ValueError) as exc:
        log.error("run failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
