from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

def setup_browser():
    """Set up the Chrome WebDriver."""
    chrome_driver_path = os.path.abspath("C:\\chromedriver.exe")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)


def scrape_content(url: str, browser: webdriver.Chrome) -> str:
    """Scrape the main content of a webpage."""
    try:
        browser.get(url)
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, "html5lib")
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text() for p in paragraphs])
        return content
    except Exception as e:
        return f"Error scraping {url}: {e}"
