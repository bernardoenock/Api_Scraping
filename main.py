import logging
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from scraping import get_page_source

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def home():
    return { 'message': 'To START Go to /colect-html' }

@app.get("/colect-html")
def iniciar_bot():
    selenium_host = "http://selenium:4444/wd/hub"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(command_executor=selenium_host, options=chrome_options)
    
    try:
        html_source = get_page_source(driver, logger)
        time.sleep(2)

        logger.info("Full HTML captured successfully")

    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        html_source = "Error during scraping"

    finally:
        driver.quit()
        logger.info("Browser closed")

    return {"html": html_source}
