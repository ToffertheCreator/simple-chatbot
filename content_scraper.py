from selenium import webdriver  # Importing Selenium WebDriver for browser automation
from selenium.webdriver.chrome.service import Service  # To provide the path to the ChromeDriver
from selenium.webdriver.chrome.options import Options  # For configuring Chrome browser options
from bs4 import BeautifulSoup  # Importing BeautifulSoup for parsing HTML content
import os  # To work with file paths

def setup_browser():
    """Set up the Chrome WebDriver."""
    # Specify the path to the ChromeDriver executable
    chrome_driver_path = os.path.abspath("C:\\chromedriver.exe")  # Ensure the chromedriver.exe is installed and in the path
    chrome_options = Options()  # Set options for the Chrome browser

    # Add options to run Chrome in headless mode (no UI), disable GPU, and no sandbox (for headless environments)
    chrome_options.add_argument("--headless")  # Run browser in headless mode (without UI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (needed for headless mode)
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox for more compatibility in some environments

    # Return the Chrome WebDriver with the specified options and service
    return webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)


def scrape_content(url: str, browser: webdriver.Chrome) -> str:
    """Scrape the main content of a webpage."""
    try:
        # Open the given URL using the provided browser instance
        browser.get(url)

        # Get the HTML source code of the page
        html_source = browser.page_source

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_source, "html5lib")

        # Find all <p> tags (typically containing the main text content of the page)
        paragraphs = soup.find_all("p")

        # Extract the text from each <p> tag and join them into a single string
        content = "\n".join([p.get_text() for p in paragraphs])

        # Return the scraped content as a string
        return content
    except Exception as e:
        # Return an error message if something goes wrong during scraping
        return f"Error scraping {url}: {e}"
