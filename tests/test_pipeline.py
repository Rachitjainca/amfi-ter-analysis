import datetime as dt

import pandas as pd
import pytest

from amfi_ter_analysis import cli, compare, notify, report
from amfi_ter_analysis.amfi import KEY, validate


def snapshot(rows):
    return validate(
        pd.DataFrame(
            [
                {
                    KEY: code,
                    "Scheme Name": name,
                    "TER Date": "2026-02-01",
                    "Regular Plan - Base TER (%)": regular,
                    "Direct Plan - Base TER (%)": direct,
                }
                for code, name, regular, direct in rows
            ]
        )
    )


OLD = snapshot([("A", "Alpha Fund", 1.84, 0.50), ("B", "Beta Fund", 1.20, 0.40), ("C", "Gamma Fund", 2.0, 1.0)])
NEW = snapshot([("A", "Alpha Fund", 1.80, 0.50), ("B", "Beta Fund", 1.20, 0.35), ("D", "Delta Fund", 1.0, 0.3)])


def test_compare_plan_reports_only_changes_with_positive_reduction_for_cuts():
    regular = compare.compare_plan(OLD, NEW, "Regular")
    assert list(regular["Scheme Name"]) == ["Alpha Fund"]
    assert regular.loc[0, "TER Reduction (%)"] == pytest.approx(0.04)
    assert regular.loc[0, "Old Regular Plan - Base TER (%)"] == 1.84
    assert list(compare.compare_plan(OLD, NEW, "Direct")["Scheme Name"]) == ["Beta Fund"]


def test_compare_plan_flags_increases_as_negative_reduction():
    increased = compare.compare_plan(NEW, OLD, "Regular")
    assert increased.loc[0, "TER Reduction (%)"] == pytest.approx(-0.04)


def test_new_schemes_lists_codes_absent_from_baseline():
    assert list(compare.new_schemes(OLD, NEW)[KEY]) == ["D"]


def test_message_lists_changes_and_stays_short():
    changes = compare.compare_all(OLD, NEW)
    message = report.build_message(changes, compare.new_schemes(OLD, NEW), dt.date(2026, 10, 25))
    assert "Alpha Fund: 1.84% -> 1.80%" in message
    assert "Delta Fund" in message
    assert len(message) < report.MAX_CHARS


def test_message_when_nothing_changed():
    empty = compare.compare_all(OLD, OLD)
    assert "No base TER changes" in report.build_message(empty, compare.new_schemes(OLD, OLD), dt.date(2026, 10, 25))


def test_first_run_creates_baseline_then_second_run_reports(tmp_path):
    today = dt.date(2026, 10, 25)
    first = cli.run(tmp_path, today, send_notification=False, current=OLD)
    assert first["baseline_created"]
    second = cli.run(tmp_path, today, send_notification=False, current=NEW)
    assert (second["regular_changes"], second["direct_changes"], second["new_schemes"]) == (1, 1, 1)
    assert (tmp_path / "output" / f"Regular_Plan_TER_Changes_{today}.csv").exists()
    assert (tmp_path / "output" / "latest_message.txt").exists()


def test_notify_skips_without_webhook_and_rejects_foreign_hosts(monkeypatch):
    monkeypatch.delenv(notify.ENV_VAR, raising=False)
    assert notify.send("hi") is False
    assert notify.send("hi", webhook_url="https://example.com/hook") is False


def test_validate_rejects_missing_columns():
    with pytest.raises(ValueError):
        validate(pd.DataFrame({"Scheme Name": ["x"]}))


def test_validate_maps_renamed_base_columns_and_keeps_latest_daily_row():
    raw = pd.DataFrame(
        {
            KEY: ["A", "A", "A", "B"],
            "Scheme Name": ["Alpha"] * 3 + ["Beta"],
            "TER Date": ["2026-10-01", "2026-10-03", "2026-10-02", "2026-10-01"],
            "Regular Plan - Base Expense Ratio (BER) (%)": [1.0, 0.9, 1.0, 2.0],
            "Direct Plan - Base Expense Ratio (BER) (%)": [0.5, 0.4, 0.5, 1.0],
            "Regular Plan - Total TER (%)": [9, 9, 9, 9],
        }
    )
    out = validate(raw)
    assert list(out[KEY]) == ["A", "B"]
    assert out.loc[0, "Regular Plan - Base TER (%)"] == 0.9
    assert out.loc[0, "Direct Plan - Base TER (%)"] == 0.4
