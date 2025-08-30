import time

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
    match option.lower():
        case "requests":
            import requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            return requests.get(url, headers=headers).text
        case "selenium":
            from driver import Driver
            driver_manager = Driver("edge", "E:/PYTHON/Scripts/msedgedriver.exe")
            instance = driver_manager.acquire()
            if instance is None:
                raise RuntimeError("WebDriver failed to initialize.")
            try:
                instance.get(url)
                time.sleep(3)
                return instance.page_source
            finally:
                Driver.quit()  # TODO: quit太草率了，应添加更多的逻辑（或许异步？）
        case _:
            raise ValueError(f"Unsupported option: {option}")


if __name__ == "__main__":
    url = "https://movie.douban.com/"
    option = "requests"
    html = get_html(url, option)
    with open("output2.html", "w", encoding="utf-8") as f:
        f.write(html)