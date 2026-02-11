# Google Chat Webhook Integration - Setup Guide

## Overview

Your GitHub Actions workflow now sends automated notifications to Google Chat whenever the AMFI TER daily analysis runs. This includes:
- ✅ Success notifications with analysis summary
- ❌ Failure notifications with error details
- 📊 Direct link to view the GitHub Action run

---

## Step 1: Create Google Chat Webhook

### 1.1 Open Google Chat
Go to [Google Chat](https://chat.google.com)

### 1.2 Create a New Space (or use existing)
- Click **"Create"** → **"Create a space"** or use an existing space
- Name it something like "AMFI TER Notifications"
- Click **"Create"**

### 1.3 Enable Webhooks
1. Open the space where you want notifications
2. Click the **space menu** (⋮) at the top
3. Select **"Apps & integrations"**
4. Click **"Create Webhook"**
5. Give it a name: `AMFI TER Analysis`
6. Click **"Create"**

### 1.4 Copy Webhook URL
- The webhook URL appears on screen
- Click **"Copy"** to copy it
- **Save this URL** - you'll need it in the next step

Example format:
```
https://chat.googleapis.com/v1/spaces/XXXXXX/messages?key=YYYYYY&token=ZZZZZZ
```

---

## Step 2: Add Secret to GitHub Repository

### 2.1 Go to Repository Settings
1. Go to your GitHub repository: `https://github.com/Rachitjainca/amfi-ter-analysis`
2. Click **Settings** (top right)
3. Click **Secrets and variables** → **Actions**

### 2.2 Create New Secret
1. Click **"New repository secret"** button
2. **Name:** `GOOGLE_CHAT_WEBHOOK_URL`
3. **Value:** Paste the webhook URL from Step 1.4
4. Click **"Add secret"**

✅ The secret is now saved and available to your workflow!

---

## Step 3: Verify Integration (Test)

### 3.1 Manual Trigger
1. Go to your repository
2. Click **"Actions"** tab
3. Click **"AMFI TER Daily Analysis"** workflow
4. Click **"Run workflow"** dropdown
5. Click **"Run workflow"** button
6. Wait for it to complete (~2 minutes)

### 3.2 Check Google Chat
After the workflow completes:
- Go to your Google Chat space
- You should see a notification message like:

```
✅ AMFI TER Analysis - Daily Update

Status: Success
Date: 2026-02-12
Repository: Rachitjainca/amfi-ter-analysis
Run: View in GitHub

Analysis Results:
• Regular Plan Changes: Analyzed and reported
• Direct Plan Changes: Analyzed and reported
• Comparison: Regular vs Direct plan changes tracked

Files Generated:
• Regular_Plan_TER_Changes_*.csv
• Direct_Plan_TER_Changes_*.csv
• Regular_vs_Direct_TER_Changes_*.csv

All results have been committed to the repository.
```

---

## Step 4: Automatic Daily Notifications

Once set up, your workflow will:

1. **Run Daily at 9:00 AM IST** (UTC 3:30)
2. **Analyze TER data** and generate reports
3. **Send Google Chat message** with results
4. **Auto-commit** changes to GitHub

No further action needed - it's fully automated!

---

## 📊 Notification Examples

### Success Notification
```
✅ AMFI TER Analysis - Daily Update

Status: Success
Date: 2026-02-12
Repository: Rachitjainca/amfi-ter-analysis
Run: View in GitHub

Analysis Results:
• Regular Plan Changes: Analyzed and reported
• Direct Plan Changes: Analyzed and reported
• Comparison: Regular vs Direct plan changes tracked

Files Generated:
• Regular_Plan_TER_Changes_*.csv
• Direct_Plan_TER_Changes_*.csv
• Regular_vs_Direct_TER_Changes_*.csv

All results have been committed to the repository.
```

### Failure Notification
```
❌ AMFI TER Analysis - Daily Update

Status: Failed
Date: 2026-02-12
Repository: Rachitjainca/amfi-ter-analysis
Run: View in GitHub

Error: The analysis workflow failed. Please check the logs for details.

Action Required: Review the GitHub Actions logs to identify the issue.
```

---

## 🔧 Troubleshooting

### Notification Not Received?

**Check 1: Secret Configuration**
1. Go to Repository Settings → Secrets and variables → Actions
2. Verify `GOOGLE_CHAT_WEBHOOK_URL` exists
3. Secret name must be exact (case-sensitive)

**Check 2: Webhook URL Validity**
1. Go back to Google Chat space settings
2. Verify webhook is still active
3. Copy the URL again and update the secret

**Check 3: Workflow Logs**
1. Go to Actions → AMFI TER Daily Analysis
2. Click the latest run
3. Scroll to "Notify Google Chat" step
4. Check for error messages

**Check 4: GitHub Actions Permissions**
1. Go to Settings → Actions → General
2. Verify "Allow all actions" is enabled
3. Check "Read and write permissions" is selected

---

## 📝 How It Works

### Workflow Steps:
1. **Analysis** - Python script analyzes TER data
2. **Summary** - Generates `analysis_summary.json`
3. **Commit** - Pushes changes to repository
4. **Notification** - Sends message to Google Chat webhook
   - Success message if analysis completed
   - Failure message if analysis failed

### Data Captured:
- Workflow status (success/failure)
- Repository name
- Execution date
- Link to GitHub Action run
- Analysis results summary

---

## 🔐 Security Notes

✅ **Webhook URL is secure:**
- Stored as GitHub Secret (encrypted)
- Not visible in workflow logs
- Only accessible to this repository

✅ **No sensitive data sent:**
- Only summary statistics sent
- No individual scheme details
- No authentication details

✅ **Google Chat permissions:**
- Webhook only posts messages
- Cannot read or delete messages
- Limited to the space it was created in

---

## 📌 Important Notes

### Secret Name Must Match
The workflow expects the secret to be named exactly:
```
GOOGLE_CHAT_WEBHOOK_URL
```

If you use a different name, update line in workflow:
```yaml
webhook-url: ${{ secrets.YOUR_SECRET_NAME }}
```

### Webhook URL Format
The URL should start with:
```
https://chat.googleapis.com/v1/spaces/
```

If it doesn't, you may have copied the wrong URL.

### Multiple Spaces
If you want notifications in multiple Google Chat spaces:
1. Create multiple webhooks (one per space)
2. Create multiple secrets (one per webhook)
3. Add separate notification steps in workflow

---

## 🎯 Next Steps

1. **Immediate:**
   - [ ] Create Google Chat webhook
   - [ ] Add secret to GitHub
   - [ ] Test with manual trigger

2. **Monitor:**
   - [ ] Check Google Chat for daily messages
   - [ ] Review workflow success/failure history
   - [ ] Keep webhook URL safe (don't share publicly)

3. **Optional:**
   - [ ] Customize notification message
   - [ ] Add more details to summary
   - [ ] Set up multiple notification channels

---

## 📚 Workflow Files Modified

### `.github/workflows/ter_analysis.yml`
- Added "Read analysis summary" step
- Added "Notify Google Chat - Success" step
- Added "Notify Google Chat - Failure" step

### `ter_github_actions.py`
- Added `generate_notification_data()` function
- Creates `analysis_summary.json` with analysis results

---

## 🔗 References

- [Google Chat Webhooks](https://developers.google.com/chat/how-tos/webhooks)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [google-github-actions/send-google-chat-webhook](https://github.com/google-github-actions/send-google-chat-webhook)

---

## ✅ Verification Checklist

After setup:
- [ ] Google Chat space created
- [ ] Webhook created and URL copied
- [ ] GitHub secret `GOOGLE_CHAT_WEBHOOK_URL` added
- [ ] Workflow manually triggered
- [ ] Success notification received in Google Chat
- [ ] Notification includes date and analysis results
- [ ] Click "View in GitHub" link works
- [ ] Files are listed in notification message

If all checks pass: ✅ **Integration Complete!**

---

## 💡 Tips

### Customize Message (Advanced)
Edit `.github/workflows/ter_analysis.yml` to modify:
- Message text
- Include additional data
- Change formatting/emojis
- Add more details from summary

### Increase Notification Detail
Update `generate_notification_data()` in `ter_github_actions.py` to:
- Count changes per plan
- Include top changed schemes
- Add more statistics
- Track trends

### Debug Webhook Issues
Run a test from Google Chat:
1. Go to space settings
2. Click webhook
3. Test the URL directly
4. See if message posts

---

**Setup Complete!** Your AMFI TER analysis now sends daily notifications to Google Chat. 🎉

