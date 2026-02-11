# Deploy Google Chat Integration - Step by Step

## 📋 Deployment Checklist

This guide walks you through deploying the Google Chat notification integration to your GitHub repository.

---

## Step 1: Verify Local Changes

### 1.1 Check Updated Files
Ensure these files have been updated in your local AMFI folder:

```bash
✓ .github/workflows/ter_analysis.yml
✓ ter_github_actions.py
✓ GOOGLE_CHAT_SETUP.md (new)
✓ GOOGLE_CHAT_QUICK_START.md (new)
✓ GOOGLE_CHAT_CHANGES.md (new)
✓ GOOGLE_CHAT_INTEGRATION.md (this file)
```

### 1.2 Verify Changes Locally
```bash
cd c:\Users\rachit.jain\Desktop\AMFI
git status
```

You should see the modified/new files listed.

---

## Step 2: Create Google Chat Webhook

### 2.1 Create Space or Use Existing
Go to [Google Chat](https://chat.google.com)
- Create new space (optional): Click "Create" → "Create a space"
- Or use existing space

### 2.2 Create Webhook
In your Google Chat space:
1. Click **space menu** (⋮ three dots)
2. Select **"Apps & integrations"**
3. Click **"Create Webhook"**
4. Name: `AMFI TER Analysis`
5. Click **"Create"**

### 2.3 Copy Webhook URL
- The webhook URL appears
- Click **"Copy"**
- **Save this URL** (you'll need it in Step 3)

Example URL format:
```
https://chat.googleapis.com/v1/spaces/SPACE_ID/messages?key=API_KEY&token=TOKEN
```

---

## Step 3: Add Secret to GitHub

### 3.1 Go to Repository Settings
1. Open GitHub: `https://github.com/Rachitjainca/amfi-ter-analysis`
2. Click **"Settings"** (top right)
3. Click **"Secrets and variables"** → **"Actions"**

### 3.2 Create New Secret
1. Click **"New repository secret"** button
2. **Name field:** `GOOGLE_CHAT_WEBHOOK_URL` (exactly as shown)
3. **Value field:** Paste the webhook URL from Step 2.3
4. Click **"Add secret"**

✅ Secret is now stored and encrypted in GitHub!

---

## Step 4: Commit and Push Changes

### 4.1 Stage Changes
```bash
cd c:\Users\rachit.jain\Desktop\AMFI
git add .
```

### 4.2 Commit
```bash
git commit -m "Feature: Add Google Chat webhook notifications for daily TER analysis"
```

### 4.3 Push to GitHub
```bash
git push -u origin main
```

Expected output:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Delta compression using up to X threads
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), X bytes
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ Changes pushed to GitHub!

---

## Step 5: Verify Changes in GitHub

### 5.1 Check Repository
1. Go to `https://github.com/Rachitjainca/amfi-ter-analysis`
2. Verify files are there:
   - `.github/workflows/ter_analysis.yml` (updated)
   - `ter_github_actions.py` (updated)
   - `GOOGLE_CHAT_*.md` (new guides)

### 5.2 Check Secrets
1. Go to Settings → Secrets and variables → Actions
2. Verify `GOOGLE_CHAT_WEBHOOK_URL` is listed
3. You should NOT see the actual URL (it's encrypted)

---

## Step 6: Test the Integration

### 6.1 Manual Test Run
1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. Click **"AMFI TER Daily Analysis"** workflow
4. Click **"Run workflow"** dropdown
5. Click **"Run workflow"** button
6. Wait for the run to complete (~2 minutes)

### 6.2 Monitor Progress
- Workflow status shows in the Actions tab
- Green checkmark = Success
- Red X = Failed (check logs)

### 6.3 Check Google Chat
Go to your Google Chat space. You should see a message like:

```
✅ AMFI TER Analysis - Daily Update

Status: Success
Date: 2026-02-12
Repository: Rachitjainca/amfi-ter-analysis
Run: View in GitHub
...
```

✅ **Integration Successful!**

---

## Step 7: Troubleshoot (If Needed)

### No Message in Google Chat?

**Check 1: Secret Configuration**
```
Repository Settings → Secrets and variables → Actions
Verify GOOGLE_CHAT_WEBHOOK_URL exists (exact name)
```

**Check 2: GitHub Actions Permissions**
```
Settings → Actions → General
Verify "Allow all actions" is enabled
Verify "Read and write permissions" selected
```

**Check 3: Workflow Logs**
1. Go to Actions tab
2. Click the failed/latest run
3. Click "ter-analysis" job
4. Scroll to "Notify Google Chat" step
5. Check for error messages
6. Expand each step to see output

**Check 4: Webhook URL**
- Make sure you copied the FULL webhook URL
- Should start with `https://chat.googleapis.com/`
- Should include `key=` and `token=` parameters

---

## Step 8: Verify Daily Execution

### 8.1 First Automatic Run
- Scheduled for: **9:00 AM IST (UTC 3:30)** tomorrow
- Will automatically send Google Chat notification
- No action required from you

### 8.2 Monitor Future Runs
1. Each day at 9:00 AM IST, the workflow runs
2. Check Google Chat space for notification
3. Check Actions tab for run status and logs

---

## Complete File Changes Summary

### Modified Files (2)
1. **`.github/workflows/ter_analysis.yml`**
   - Added: Read analysis summary step
   - Added: Google Chat success notification step
   - Added: Google Chat failure notification step

2. **`ter_github_actions.py`**
   - Added: `generate_notification_data()` function
   - Modified: `__main__` block to call notification function

### New Files (4)
1. `GOOGLE_CHAT_SETUP.md` - Complete setup guide
2. `GOOGLE_CHAT_QUICK_START.md` - Quick reference
3. `GOOGLE_CHAT_CHANGES.md` - What changed
4. `GOOGLE_CHAT_INTEGRATION.md` - This deployment guide

---

## Expected Behavior After Deployment

### Daily Schedule
| Time | Action |
|------|--------|
| 9:00 AM IST | GitHub Actions triggers |
| 9:01 AM IST | Python analysis runs |
| 9:02 AM IST | Google Chat notification sent |

### Notification Examples

**Success (9:00 AM-9:02 AM):**
```
✅ AMFI TER Analysis - Daily Update
Status: Success
Date: 2026-02-12
[... analysis results ...]
All results have been committed to the repository.
```

**Failure (if any step fails):**
```
❌ AMFI TER Analysis - Daily Update
Status: Failed
Date: 2026-02-12
Error: The analysis workflow failed...
```

---

## 🔐 Security Reminders

✅ **Do:**
- Keep webhook URL secret (stored in GitHub Secrets)
- Use only official Google Chat spaces
- Monitor Google Chat for daily updates
- Review logs if notifications fail

❌ **Don't:**
- Share webhook URL publicly
- Commit webhook URL to repository
- You can't, it's encrypted anyway! 

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| "repository not found" | Check secret name: `GOOGLE_CHAT_WEBHOOK_URL` |
| "Permission denied to fintechchamp" | Make sure you're using Rachitjainca username |
| No notification received | Check secret is added to GitHub Settings |
| Workflow fails with 403 | Verify webhook URL is valid and active |
| Message appears late | GitHub Actions can have 1-5 min delay (normal) |
| Wrong webhook URL | Delete and re-create webhook, update secret |
| Multiple messages | Check if workflow runs manually + scheduled |

---

## Next Steps After Deployment

1. **Immediate (Today):**
   - [ ] Follow steps 1-6 above
   - [ ] Verify notification in Google Chat

2. **Monitor (Next 24 hours):**
   - [ ] Check if automatic run happens tomorrow at 9:00 AM IST
   - [ ] Verify notification appears in Google Chat
   - [ ] Review notification content

3. **Optional Enhancements:**
   - [ ] Customize notification message format
   - [ ] Add more metrics to summary
   - [ ] Set up multiple notification channels

---

## Command Reference

### Quick Commands (Copy & Paste)

**Check git status:**
```bash
cd c:\Users\rachit.jain\Desktop\AMFI
git status
```

**Stage all changes:**
```bash
git add .
```

**Commit changes:**
```bash
git commit -m "Feature: Add Google Chat webhook notifications for daily TER analysis"
```

**Push to GitHub:**
```bash
git push -u origin main
```

**Check GitHub Actions:**
```
Open: https://github.com/Rachitjainca/amfi-ter-analysis/actions
```

---

## Files to Review

Before deploying, you may want to review:
- **Setup Details**: `GOOGLE_CHAT_SETUP.md`
- **Quick Start**: `GOOGLE_CHAT_QUICK_START.md`
- **Changes Made**: `GOOGLE_CHAT_CHANGES.md`
- **Workflow**: `.github/workflows/ter_analysis.yml`
- **Script**: `ter_github_actions.py`

---

## Success Indicators

✅ **You're successful when:**
1. Files committed to GitHub
2. Secret added to repository
3. Manual workflow run succeeds
4. Google Chat shows notification
5. Notification includes today's date
6. "View in GitHub" link works
7. Files section lists CSV names
8. Next day automatic run occurs

---

## 📞 Support

- **Quick Help**: Read `GOOGLE_CHAT_QUICK_START.md`
- **Full Guide**: Read `GOOGLE_CHAT_SETUP.md`
- **Troubleshooting**: See section above or `GOOGLE_CHAT_SETUP.md`
- **Technical Details**: See `GOOGLE_CHAT_CHANGES.md`

---

**Ready to Deploy?** Follow steps 1-8 above! 🚀

