import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_website(website):
    print("Launching Chrome browser...")

    # Path to the ChromeDriver (ensure the correct path here)
    chrome_driver_path = "./chromedriver"

    # Configure Chrome options
    options = Options()
    options.headless = True  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Recommended for headless environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--remote-debugging-port=9222")  # Enable DevTools debugging

    # Add binary location if using Chromium instead of Chrome
    options.binary_location = '/usr/bin/chromium-browser'  # Uncomment if using Chromium

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source
        time.sleep(5)  # Wait for the page to fully load

        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Clean and extract text
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
