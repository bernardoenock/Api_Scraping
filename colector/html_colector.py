from __future__ import annotations

from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


class HTMLColector:
    """ classe contexto para coletar HTML"""
    def __init__(self, strategy: HTMLColectorStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> HTMLColectorStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: HTMLColectorStrategy) -> None:
        self._strategy = strategy

    def collect_html(self):
        return self._strategy.collect_html()


class HTMLColectorStrategy(ABC):
    """
    Classe abstrata para estratégias de coleta de HTML
    """
    @abstractmethod
    def collect_html(self, *args, **kwargs):
        pass


class SeleniumStrategy(HTMLColectorStrategy):
    """
    Classe concreta para coleta de HTML usando Selenium
    """
    def __init__(self, driver):
        self._engine = driver
    
    def navigate_to_url(self, url, logger):
        """
        Navegar a uma página específica
        """
        try:
            logger.info(f"Navigating to {url}")
            self._engine.get(url)
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            raise

    def get_page_source(self, logger):
        try:
            logger.info("Capturing page's HTML...")
            return self._engine.page_source
        
        except TimeoutException:
            logger.error(f"Error during scraping: {e}")
    
    def quit_driver(self, logger):
        """
        Fecha o navegador
        """
        try:
            logger.info("Closing browser...")
            self._engine.quit()
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            raise
    
    def collect_html(self, url: str, logger) -> str:
        """
        Realiza a coleta do HTML de uma página específica.
        Navega para a URL, captura o HTML e fecha o navegador

        :param url: URL da página a ser coletada
        :param logger: objeto logger para realizar log
        :return: HTML da página
        """

        try:
            self.navigate_to_url(url, logger)
            html = self.get_page_source(logger)
            return html
        finally:
            self.quit_driver(logger)

class BS4Strategy(HTMLColectorStrategy):

    def collect_html(self, url: str, logger) -> str:
        try:
            logger.info(f"Collecting HTML from {url} with BS4")
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            html = soup.prettify()
            logger.info("Successfully captured HTML with BS4")
            return html
        except requests.RequestException as e:
            logger.error(f"Error during BS4 scraping: {e}")
            raise

class HTMLColectorFactory:
    """
    Fábrica para instanciar estratégias do HTMLColector
    """

    #TODO: melhorar a implementação da Factory. ainda está bem incompleta e inflexível
    @staticmethod
    def create_strategy(strategy: str, logger) ->HTMLColectorStrategy:
        if strategy == "selenium":
            selenium_host = "http://selenium:4444/wd/hub"
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Remote(command_executor=selenium_host, options=chrome_options)
            return SeleniumStrategy(driver)

        elif strategy == "bs4":
            return BS4Strategy()
        else:
            raise ValueError(f"Invalid strategy: {strategy}")