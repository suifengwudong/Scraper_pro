
# Scraper_pro

一个支持 requests 和 Selenium 的网页采集与可视化工具。

## 功能简介
- 支持静态页面采集（requests）
- 支持动态页面采集（Selenium，自动执行 JS）
- 可自定义浏览器驱动路径
- 单例模式管理 WebDriver，自动释放资源
- 图形化界面，支持：
  - HTML源码获取与预览
  - DOM树结构可视化与筛选
  - 元素选中与批量操作
  - 自动化爬虫参数设置与启动

## 快速使用
1. 安装依赖：
	```bash
	pip install selenium requests PyQt5 beautifulsoup4
	```
2. 启动界面：
	```bash
	python src/scrape/main_window.py
	```
3. 示例代码（命令行采集）：
	```python
	from src.scrape.get_html import get_html
	html = get_html('https://movie.douban.com', 'selenium')
	print(html)
	```

## 目录结构
- src/scrape/main_window.py      主界面入口
- src/scrape/ui/html_widget.py  HTML采集与预览界面
- src/scrape/ui/tree_widget.py  DOM树结构展示与筛选
- src/scrape/ui/output_view.py  输出/日志窗口
- src/scrape/ui/driver_dialog.py 浏览器驱动选择对话框
- src/scrape/web/driver.py      Selenium驱动管理
- src/scrape/web/fetch_html.py  网页采集主逻辑
- src/scrape/web/parse_html.py  HTML解析与清洗
- src/scrape/web/web_config.py  浏览器配置管理
- test/data/                    测试用HTML样例

## UI界面说明
- Tab1：HTML获取与预览，可选择采集方式（requests/selenium），支持驱动加载
- Tab2：DOMTree结构展示，支持标签/属性/值筛选与递归选中
- Tab3：自动化爬虫参数设置与启动，状态实时显示

## 注意事项
- Selenium 需下载对应浏览器驱动，并配置路径
- requests 采集部分网站需自定义 headers 规避反爬
- 建议使用 Python 3.8 及以上版本
