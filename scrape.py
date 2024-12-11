import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Function to scrape a website using Selenium
def scrape_website(website):
    print("Launching chrome browser...")
    chrome_driver_path = "./chromedriver.exe"  # Path to ChromeDriver
    options = webdriver.ChromeOptions()  # Configure Selenium options
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)  # Load the website
        print("Page loaded...")
        html = driver.page_source  # Get the page's HTML content
        return html
    finally:
        driver.quit()  # Ensure the browser closes after scraping

# Extracts only the <body> content of the page
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

# Removes scripts, styles, and unnecessary whitespace
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):  # Remove <script> and <style> tags
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")  # Extract plain text
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )  # Remove extra whitespace
    return cleaned_content

# Splits large content into manageable chunks for AI processing
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
