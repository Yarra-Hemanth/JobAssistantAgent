import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from readability import Document
from newspaper import Article
from goose3 import Goose

# ----------------------------------------
# 🔧 Selenium-based extractor (e.g., Indeed, Naukri, Foundit)
# ----------------------------------------
def selenium_extract(url, wait_by, wait_value):
    options = uc.ChromeOptions()
    # Disable headless for anti-bot sites
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        driver = uc.Chrome(options=options)
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((wait_by, wait_value)))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup
    except Exception as e:
        print("❌ Selenium error:", e)
        try:
            driver.quit()
        except:
            pass
        return None

# ----------------------------------------
# 🌐 Site-specific handlers
# ----------------------------------------
def extract_indeed(url):
    soup = selenium_extract(url, By.ID, "jobDescriptionText")
    if soup:
        block = soup.find("div", id="jobDescriptionText")
        if block:
            return block.get_text(separator="\n").strip()
    return None

def extract_naukri(url):
    soup = selenium_extract(url, By.CLASS_NAME, "jd-wrapper")
    if soup:
        block = soup.find("div", class_="jd-wrapper")
        if block:
            return block.get_text(separator="\n").strip()
    return None

def extract_foundit(url):
    soup = selenium_extract(url, By.ID, "JobDescription")
    if soup:
        block = soup.find("div", id="JobDescription")
        if block:
            return block.get_text(separator="\n").strip()
    return None

def extract_linkedin_with_goose(url):
    try:
        g = Goose()
        article = g.extract(url=url)
        if article.cleaned_text and len(article.cleaned_text.strip()) > 200:
            return article.cleaned_text.strip()
    except:
        pass
    return None

# ----------------------------------------
# 📚 Generic fallback extractors
# ----------------------------------------
def extract_with_tools(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        if len(article.text.strip()) > 200:
            return article.text.strip()
    except:
        pass

    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        doc = Document(res.text)
        soup = BeautifulSoup(doc.summary(), 'html.parser')
        text = soup.get_text(separator='\n').strip()
        if len(text) > 200:
            return text
    except:
        pass

    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.content, 'html.parser')
        for tag in ['div', 'section', 'article']:
            for block in soup.find_all(tag):
                text = block.get_text()
                if 'job' in text.lower() and len(text) > 300:
                    return text.strip()
    except:
        pass

    return None

# ----------------------------------------
# 🚀 Main Controller
# ----------------------------------------
def extract_job_description(url):
    hostname = urlparse(url).hostname or ""
    extractors = {
        "linkedin.com": extract_linkedin_with_goose,
        "indeed.com": extract_indeed,
        "naukri.com": extract_naukri,
        "foundit": extract_foundit,
        "monsterindia": extract_foundit,
    }
    for key, func in extractors.items():
        if key in hostname:
            result = func(url)
            return result if result else "JD extraction failed or unsupported URL."

    result = extract_with_tools(url)
    return result if result else "JD extraction failed or unsupported URL."


# ----------------------------------------
# 🧪 Run Script
# ----------------------------------------
if __name__ == "__main__":
    url = input("🔗 Enter job description URL: ").strip()
    jd = extract_job_description(url)
    if jd:
        print("\n📄 Extracted Job Description:\n")
        print(jd[:2000])
        with open("extracted_jd.txt", "w", encoding="utf-8") as f:
            f.write(jd)
        print("\n💾 Saved to 'extracted_jd.txt'")
    else:
        print("\n⚠️ Unable to extract JD from this site.")
