
# Chrome + ChromeDriver Setup Guide for JobAssistantAgent

This document describes how to set up Google Chrome and ChromeDriver to enable JD extraction via Selenium in the JobAssistantAgent project.

## ✅ Step 1: Install Google Chrome

Download and install Chrome from the official site:
https://www.google.com/chrome/

Ensure it's properly installed and accessible from the system PATH.

## ✅ Step 2: Install undetected-chromedriver

JobAssistantAgent uses `undetected-chromedriver` to bypass anti-bot protections.

Run the following command:
```
pip install undetected-chromedriver
```

## ✅ Step 3: Verify ChromeDriver Works

Test the setup using Python:
```
python -c "import undetected_chromedriver as uc; driver = uc.Chrome(); driver.quit(); print('✅ ChromeDriver works!')"
```

If successful, you’ll see:
```
✅ ChromeDriver works!
```

## 🛑 Troubleshooting

If Chrome is not installed or incompatible:
- JD extraction from URL will fail silently or throw errors.

### 💡 Error Handling Suggestion

Inside `jd_extraction.py`, enhance error visibility:

```
try:
    driver = uc.Chrome(options=options)
    driver.get(url)
    ...
except Exception as e:
    print('❌ Chrome or ChromeDriver error:', e)
```

This prints helpful messages such as:
```
❌ Chrome or ChromeDriver error: cannot find Chrome binary
```

---
This setup ensures your project works consistently across machines and reviewers’ systems.
