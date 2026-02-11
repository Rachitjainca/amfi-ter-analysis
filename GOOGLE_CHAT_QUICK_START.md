# Google Chat Integration - Quick Setup (5 Minutes)

## ⚡ Ultra-Quick Setup

### Step 1: Create Google Chat Webhook (2 min)
```
Google Chat → Space → ⋮ Menu → Apps & integrations → Create Webhook
Copy the URL that appears
```

### Step 2: Add Secret to GitHub (2 min)
```
Repository Settings → Secrets and variables → Actions
New secret name: GOOGLE_CHAT_WEBHOOK_URL
Paste webhook URL
```

### Step 3: Test (1 min)
```
Actions tab → Run workflow → Monitor Google Chat for message
```

**Done!** Your notifications are live. 🎉

---

## What You'll Get

Every day at 9:00 AM IST:
- ✅ Success notification OR ❌ Failure alert
- 📊 Analysis summary
- 🔗 Link to GitHub Action logs
- 📝 List of generated reports

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No message in Chat | Check secret name is exact: `GOOGLE_CHAT_WEBHOOK_URL` |
| "Permission denied" | Re-copy webhook URL, update secret |
| Action fails | Check Repository Settings → Actions → Permissions enabled |
| Still no message | Run manual test, check Actions logs |

---

## File References

- **Setup Guide:** `GOOGLE_CHAT_SETUP.md` (Complete)
- **Workflow:** `.github/workflows/ter_analysis.yml` (Updated)
- **Script:** `ter_github_actions.py` (Updated)

---

**Need help?** See `GOOGLE_CHAT_SETUP.md` for detailed steps.

