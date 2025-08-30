from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from typing import Optional

class Driver:
    _instance = None
    _driver = None

    def __new__(cls, browser_name: str, driver_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._driver = cls._create_driver(browser_name, driver_path)
        return cls._instance

    @classmethod
    def _create_driver(cls, browser_name: str, driver_path: Optional[str] = None):
        match browser_name.lower():
            case 'chrome':
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                if driver_path:
                    service = ChromeService(driver_path)
                    return webdriver.Chrome(options=options, service=service)
                else:
                    return webdriver.Chrome(options=options)
            case 'firefox':
                options = webdriver.FirefoxOptions()
                options.add_argument('--headless')
                if driver_path:
                    service = FirefoxService(driver_path)
                    return webdriver.Firefox(options=options, service=service)
                else:
                    return webdriver.Firefox(options=options)
            case 'edge':
                options = webdriver.EdgeOptions()
                options.add_argument('--headless')
                if driver_path:
                    service = EdgeService(driver_path)
                    return webdriver.Edge(options=options, service=service)
                else:
                    return webdriver.Edge(options=options)
            case _:
                raise ValueError(f"Unsupported browser: {browser_name}")

    def acquire(self):
        '''Get the WebDriver instance.
        Returns:
            webdriver: The WebDriver instance.
        '''
        return self._driver

    @classmethod
    def quit(cls):
        """Quit the WebDriver instance and reset singleton."""
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
            cls._instance = None