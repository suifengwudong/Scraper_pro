from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from typing import Optional
import config

class Driver:
    _instance = None
    _driver = None

    def __new__(cls, browser_name: str, path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if path is None:
                if config.BROWSER_PATH_DICT.get(browser_name) is None:
                    raise ValueError(f"No driver path specified for browser: {browser_name}")
                else:
                    path = config.BROWSER_PATH_DICT[browser_name]
            else:
                if config.BROWSER_PATH_DICT.get(browser_name) is None:
                    config.BROWSER_PATH_DICT[browser_name] = path

            cls._driver = cls._create_driver(browser_name, path)
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

    @classmethod
    def quit(cls):
        """Quit the WebDriver instance and reset singleton."""
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
            cls._instance = None
    
    @classmethod
    def instance(cls):
        '''Get the Class Driver instance.
        Returns:
            Driver: The Class Driver instance.
        '''
        return cls._instance
    
    def acquire(self):
        '''Get the WebDriver instance.
        Returns:
            webdriver: The WebDriver instance.
        '''
        return self._driver
    
    def get_html(self, url: str) -> str:
        '''Navigate to the specified URL and return the page source.
        Args:
            url (str): The URL to navigate to.
        Returns:
            str: The HTML content of the page.
        Raises:
            RuntimeError: If the WebDriver is not initialized.
        '''
        if self._driver is None:
            raise RuntimeError("WebDriver is not initialized.")
        self._driver.get(url)
        self._driver.implicitly_wait(10) 
        return self._driver.page_source