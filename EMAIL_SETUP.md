# Email Setup Guide for Location Tracker

The app now sends location data via **email** instead of saving to a file! Perfect for Render's free tier.

## 📧 Gmail Setup (Recommended)

### Step 1: Create Gmail App Password

1. **Go to your Google Account**: https://myaccount.google.com
2. **Security** → **2-Step Verification** (enable if not already)
3. **Security** → **App passwords**
4. **Select app**: Choose "Mail"
5. **Select device**: Choose "Other" and name it "Location Tracker"
6. **Click Generate**
7. **Copy the 16-character password** (looks like: `xxxx xxxx xxxx xxxx`)

### Step 2: Set Environment Variables in Render

When deploying to Render, add these environment variables:

| Variable Name | Value | Example |
|--------------|-------|---------|
| `EMAIL_FROM` | Your Gmail address | `yourname@gmail.com` |
| `EMAIL_TO` | Email to receive locations | `yourname@gmail.com` (same or different) |
| `EMAIL_PASSWORD` | App password from Step 1 | `xxxxxxxxxxxxxx` (no spaces) |
| `SMTP_SERVER` | Gmail SMTP server | `smtp.gmail.com` |
| `SMTP_PORT` | Gmail SMTP port | `587` |

**In Render Dashboard:**
1. Go to your web service
2. Click **Environment** tab
3. Click **Add Environment Variable**
4. Add each variable above
5. Click **Save Changes**
6. Render will automatically redeploy

### Step 3: Test Locally (Optional)

Test on your computer before deploying:

**Windows PowerShell:**
```powershell
$env:EMAIL_FROM="yourname@gmail.com"
$env:EMAIL_TO="yourname@gmail.com"
$env:EMAIL_PASSWORD="your-app-password"
python server.py
```

Then open http://localhost:8080 and check if you receive an email!

---

## 📧 Other Email Providers

### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
EMAIL_FROM=yourname@outlook.com
EMAIL_PASSWORD=your-password
```

### Yahoo Mail
```
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
EMAIL_FROM=yourname@yahoo.com
EMAIL_PASSWORD=your-app-password
```
(Yahoo also requires app password: https://help.yahoo.com/kb/generate-app-password-sln15241.html)

### Custom SMTP Server
```
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
EMAIL_FROM=you@yourdomain.com
EMAIL_PASSWORD=your-password
```

---

## 📬 What You'll Receive

When someone opens the link, you'll receive a beautiful HTML email with:

✅ **Timestamp** - When location was captured  
✅ **Source** - GPS, WiFi, or IP-based  
✅ **Coordinates** - Latitude & Longitude  
✅ **Accuracy** - In meters  
✅ **Altitude, Speed, Heading** - If available  
✅ **Device Info** - User agent and IP address  
✅ **Google Maps Link** - Click to view location instantly  
✅ **Warnings** - If accuracy is low

---

## 🔍 Troubleshooting

### "Email not sent" error

**Check:**
1. ✅ All environment variables are set correctly in Render
2. ✅ App password (not regular password) is used for Gmail
3. ✅ 2-Step Verification is enabled for Gmail
4. ✅ No spaces in app password
5. ✅ Email addresses are valid

### "Authentication failed"

**Gmail users:**
- Make sure you're using **App Password**, not your regular password
- Check 2-Step Verification is enabled
- Try generating a new app password

### "Connection refused"

**Check:**
- SMTP_SERVER is correct
- SMTP_PORT is correct (usually 587)
- Your server/computer allows outbound SMTP connections

### Still not working?

**View Render logs:**
1. Go to Render dashboard
2. Select your service
3. Click **Logs** tab
4. Look for error messages

---

## 🎯 Benefits of Email Method

✅ **No file storage needed** - Perfect for Render's free tier  
✅ **Instant notifications** - Get alerted immediately  
✅ **Permanent record** - Emails stay in your inbox  
✅ **Easy to search** - Use email search to find locations  
✅ **No database needed** - Simpler deployment  
✅ **Works everywhere** - No disk space limitations  

---

## 🔒 Privacy & Security

⚠️ **Important:**
- Keep your app password secure
- Don't commit EMAIL_PASSWORD to Git
- Use environment variables only
- Consider who can access your email
- Emails contain precise location data

---

## 🚀 Quick Start Commands

```powershell
# Set environment variables (Windows)
$env:EMAIL_FROM="your@gmail.com"
$env:EMAIL_TO="your@gmail.com"
$env:EMAIL_PASSWORD="your-app-password"

# Run server
python server.py

# Test at http://localhost:8080
```

```bash
# Set environment variables (Linux/Mac)
export EMAIL_FROM="your@gmail.com"
export EMAIL_TO="your@gmail.com"
export EMAIL_PASSWORD="your-app-password"

# Run server
python server.py

# Test at http://localhost:8080
```

---

**Ready to deploy? Follow RENDER_DEPLOYMENT.md and add the email environment variables!**
