'''将html文件处理成层级化的结构，方便后续的解析'''
from bs4 import BeautifulSoup as BS
from typing import Optional

def parse_html(html: str, remove_script: bool = False, remove_style: bool = False, other_remove_tags: Optional[list[str]] = None) -> BS:
    '''Parse HTML content into a BeautifulSoup object.
    Args:
        html (str): The HTML content to parse.
        remove_script (bool): Whether to remove "script" tags. Default is False.
        remove_style (bool): Whether to remove "style" tags. Default is False.
        other_remove_tags (Optional[list[str]]): List of other tags to remove. Default is None.
    Returns:
        BS: The BeautifulSoup object representing the parsed HTML.
    '''
    soup = BS(html, "html.parser")
    tags: list[str] = []
    if remove_script:
        tags.append("script")
    if remove_style:
        tags.append("style")
    if other_remove_tags:
        tags.extend(other_remove_tags)
    
    for element in soup(tags):  # 直接传入列表
        element.decompose()
    
    # 这里可以添加更多的解析逻辑
    return soup

if __name__ == "__main__":
    with open("src/test/data/output1.html", "r", encoding="utf-8") as f:
        sample_html = f.read()
    parsed = parse_html(sample_html, remove_style=True, remove_script=True, other_remove_tags=["head"])
    with open("temp.html", "w", encoding="utf-8") as f:
        f.write(str(parsed))
    # print(parsed.prettify())