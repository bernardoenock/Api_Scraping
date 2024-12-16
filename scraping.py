from selenium.common.exceptions import TimeoutException


def get_page_source(driver, logger):
  try:
      logger.info("Return HTML Success.")
      return driver.page_source
  except TimeoutException:
      logger.info("Error during scraping. get_page_source")