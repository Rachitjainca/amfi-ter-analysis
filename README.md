# amfi-ter-analysis

Tracks changes in mutual fund Total Expense Ratios (TER) published by AMFI. Each run downloads the current TER workbook, compares base TER with the previous run for Regular and Direct plans, writes the changes to CSV and posts a summary to Google Chat.

## How it works

1. Download `https://www.amfiindia.com/api/populate-te-rdata-revised`.
2. Compare with `data/baseline_ter.csv.gz` on `NSDL Scheme Code`. The first run only creates the baseline.
3. Write `data/output/{Regular,Direct}_Plan_TER_Changes_<date>.csv`, `latest_message.txt` and `latest_summary.json`.
4. Replace the baseline and, if anything changed, post to Google Chat.

A positive `TER Reduction (%)` means the TER fell; a negative value means it rose.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```powershell
amfi-ter                 # run, write reports, notify if GOOGLE_CHAT_WEBHOOK_URL is set
amfi-ter --no-notify     # reports only
```

## GitHub Actions

`.github/workflows/amfi_ter_analysis.yml` runs daily at 08:10 IST and commits the updated `data/` folder.

1. In Google Chat, add a webhook to your space and copy its URL.
2. In the repository go to Settings > Secrets and variables > Actions and add `GOOGLE_CHAT_WEBHOOK_URL`.
3. Trigger the workflow once from the Actions tab to create the baseline. Notifications start from the next day with changes.

The webhook URL contains a key and token. Keep it in the secret only, never in the code or the repository.

## Development

```powershell
pytest
ruff check .
```

Licensed under MIT, see LICENSE.
