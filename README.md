# Scraper_pro

一个支持 requests 和 Selenium 的网页采集工具。

## 功能简介
- 支持静态页面采集（requests）
- 支持动态页面采集（Selenium，自动执行 JS）
- 可自定义浏览器驱动路径
- 单例模式管理 WebDriver，自动释放资源

## 快速使用
1. 安装依赖：
	```bash
	pip install selenium requests
	```
2. 示例代码：
	```python
	from src.scrape.get_html import get_html
	html = get_html('https://movie.douban.com', 'selenium')
	print(html)
	```

## 目录结构
- src/scrape/driver.py  Selenium 驱动管理
- src/scrape/get_html.py  网页采集主逻辑

## 注意事项
- Selenium 需下载对应浏览器驱动，并配置路径
- requests 采集部分网站需自定义 headers 规避反爬
