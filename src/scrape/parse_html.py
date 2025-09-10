'''将html文件处理成层级化的结构，方便后续的解析'''
from bs4 import BeautifulSoup as BS
from typing import Optional

def parse_html(html: str, remove_script: bool = False, remove_style: bool = False, other_remove_tags: Optional[list[str]] = None) -> BS:
    soup = BS(html, "html.parser")
    # 这里可以添加更多的解析逻辑
    if remove_script:
        for script in soup(["script"]):
            script.decompose()
    if remove_style:
        for style in soup(["style"]):
            style.decompose()
    if other_remove_tags:
        for tag in other_remove_tags:
            for element in soup([tag]):
                element.decompose()
    return soup

if __name__ == "__main__":
    sample_html = "<html><head><title>Test Page</title></head><body><h1>Hello, World!</h1></body></html>"
    parsed = parse_html(sample_html)
    print(parsed.prettify())