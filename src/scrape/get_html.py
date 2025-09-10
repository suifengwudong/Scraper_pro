import time
import config

driver = None  # save the driver instance here

def get_driver_instance(browser_name: str = config.driver_used, driver_path: str = config.BROWSER_PATH_DICT[config.driver_used]):

    global driver
    if driver is None:
        from driver import Driver
        driver_manager = Driver(browser_name, driver_path)
        driver = driver_manager.acquire()
    return driver

def get_html(url: str, option: str) -> str:
    '''Get HTML content from a webpage using the specified method.
    Args:
        url (str): The URL of the webpage to fetch.
        option (str): The method to use for fetching the HTML (requests or selenium).
    Returns:
        str: The HTML content of the webpage.
    Raises:
        ValueError: If an unsupported option is provided.
    '''
    html = ""
    match option.lower():
        case "requests":
            import requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            html = requests.get(url, headers=headers).text
        case "selenium":
            driver_name = config.driver_used
            instance = get_driver_instance(driver_name, config.BROWSER_PATH_DICT[driver_name])  # or "firefox", "edge"
            if instance is None:
                raise RuntimeError("WebDriver failed to initialize.")
            instance.get(url)
            time.sleep(3)
            html = instance.page_source
        case _:
            raise ValueError(f"Unsupported option: {option}")
    
    if (html == ""):
        raise RuntimeError("Failed to retrieve HTML content.")
    return html


if __name__ == "__main__":
    url = "https://movie.douban.com/"
    option = "requests"
    html = get_html(url, option)
    with open("src/test/data/output2.html", "w", encoding="utf-8") as f:
        f.write(html)