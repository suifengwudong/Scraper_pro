from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLineEdit, QPushButton, QTextEdit, QLabel, QComboBox, QFileDialog, QDialog, QMessageBox
)
from ui import *
from web import *
from bs4 import Tag

class MainWindow(QMainWindow):
    def __init__(self, soup: Tag):
        super().__init__()
        self.setWindowTitle("Scraper Pro")
        self.resize(900, 600)
        self.is_driver_loaded = False

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)
        
        # Tab1: 获取初始HTML
        tab1 = QWidget()
        vbox1 = QVBoxLayout(tab1)
        title_label = QLabel("HTML源获取")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        vbox1.addWidget(title_label)

        hbox_url = QHBoxLayout()
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("输入网址")
        hbox_url.addWidget(self.url_edit)
        vbox1.addLayout(hbox_url)

        hbox_opts = QHBoxLayout()
        self.option_combo = QComboBox()
        self.option_combo.addItems(["requests", "selenium"])
        self.option_combo.setCurrentIndex(0)
        self.option_combo.setToolTip("选择HTML获取方式")
        self.load_driver_btn = QPushButton("加载驱动")
        self.load_driver_btn.setEnabled(False)
        self.load_html_btn = QPushButton("加载HTML")
        hbox_opts.addWidget(self.option_combo)
        hbox_opts.addWidget(self.load_driver_btn)
        hbox_opts.addWidget(self.load_html_btn)
        vbox1.addLayout(hbox_opts)

        self.html_view = QTextEdit()
        self.html_view.setReadOnly(True)
        self.html_view.setPlaceholderText(">>>")
        vbox1.addWidget(self.html_view)

        self.option_combo.currentTextChanged.connect(self.on_option_changed)
        self.load_driver_btn.clicked.connect(self.load_driver)
        self.load_html_btn.clicked.connect(self.load_html)

        # Tab2: DOMTree展示与选中
        tab2 = QWidget()
        grid2 = QGridLayout(tab2)
        self.tree_widget = DOMTreeWidget(soup)
        grid2.addWidget(QLabel("DOM结构与元素选中"))
        grid2.addWidget(self.tree_widget)

        # Tab3: 自动化爬虫控制（优化布局）
        tab3 = QWidget()
        vbox3 = QVBoxLayout(tab3)
        title_label3 = QLabel("自动化爬虫")
        title_label3.setStyleSheet("font-weight: bold; font-size: 16px;")
        vbox3.addWidget(title_label3)

        hbox_params = QHBoxLayout()
        self.crawl_param_edit = QLineEdit()
        self.crawl_param_edit.setPlaceholderText("爬虫参数设置（如起始页、深度等）")
        hbox_params.addWidget(QLabel("参数:"))
        hbox_params.addWidget(self.crawl_param_edit)
        vbox3.addLayout(hbox_params)

        hbox_btn = QHBoxLayout()
        self.crawl_btn = QPushButton("启动自动化爬虫")
        hbox_btn.addStretch(1)
        hbox_btn.addWidget(self.crawl_btn)
        hbox_btn.addStretch(1)
        vbox3.addLayout(hbox_btn)

        self.crawl_status = QLabel("爬虫未启动")
        self.crawl_status.setStyleSheet("color: #124197; font-weight: bold;")
        vbox3.addWidget(self.crawl_status)

        tab_widget.addTab(tab1, "HTML获取")
        tab_widget.addTab(tab2, "DOMTree")
        tab_widget.addTab(tab3, "自动化爬虫")

        self.show()

    def on_option_changed(self, text: str):
        if text.lower() == "selenium":
            self.load_driver_btn.setEnabled(True)
        else:
            self.load_driver_btn.setEnabled(False)

    def load_driver(self):
        self.is_driver_loaded = True
        if web_configs["DEFAULT_BROWSER"] == "":
            dlg = DriverDialog(self)
            dlg.exec_()
            return
        
    def load_html(self):
        if not self.is_driver_loaded:
            QMessageBox.warning(self, "警告", "!!浏览器驱动未加载!!")
            return

if __name__ == "__main__":
    app = QApplication([])
    with open("src/test/data/output1.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = parse_html(html_content, remove_script=True, remove_style=True)

    mainWindow = MainWindow(soup)
    app.exec_()
