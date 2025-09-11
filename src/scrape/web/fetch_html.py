from .web_config import WebConfig
from typing import Optional

config = WebConfig.configs
driver = None  # save the driver instance here

def fetch_html(url: str, option: str, arg: Optional[str] = None) -> str:
    '''Get HTML content from a webpage using the specified method.
    Args:
        url (str): The URL of the webpage to fetch.
        option (str): The method to use for fetching the HTML (requests or selenium).
        arg (Optional[str]): Additional argument for selenium to specify browser type.
    Returns:
        str: The HTML content of the webpage.
    Raises:
        ValueError: If an unsupported option is provided.
    '''
    html = ""
    global driver
    match option.lower():
        case "requests":
            import requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            html = requests.get(url, headers=headers).text
        case "selenium":
            from driver import Driver
            if isinstance(arg, str) and (arg in config["BROWSER_LIST"]):
                driver_name = arg
            else:
                driver_name = config["DEFAULT_BROWSER"]

            if driver is None:
                driver = Driver(driver_name, config["BROWSER_PATH_DICT"][driver_name])  # or "firefox", "edge"
                if driver is None:
                    raise RuntimeError("WebDriver failed to initialize.")
            html = driver.get_html(url)
        case _:
            raise ValueError(f"Unsupported option: {option}")
    
    if html == "":
        raise RuntimeError("Failed to retrieve HTML content.")
    return html


if __name__ == "__main__":
    url = "https://movie.douban.com/"
    option = "selenium"
    path = "src/test/data"
    html = fetch_html(url, option)
    # from parse_html import parse_html
    # parsed = parse_html(html, remove_script=True, remove_style=True)
    # print(parsed.prettify())
    import os
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "output1.html"), "w", encoding="utf-8") as f:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        f.write(str(soup))