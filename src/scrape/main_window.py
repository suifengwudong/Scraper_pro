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
        label_style = "font-weight: bold; font-size: 32px;"
        
        # Tab1: 获取初始HTML
        tab1 = QWidget()
        grid1 = QGridLayout(tab1)
        self.html_widget = HTMLWidget()
        self.html_widget.load_html_btn.clicked.connect(self.load_soup)
        label1 = QLabel("HTML内容获取与展示")
        label1.setStyleSheet(label_style)
        grid1.addWidget(label1)
        grid1.addWidget(self.html_widget)

        # Tab2: DOMTree展示与选中
        tab2 = QWidget()
        grid2 = QGridLayout(tab2)
        self.tree_widget = DOMTreeWidget(soup)
        label2 = QLabel("DOM结构与元素选中")
        label2.setStyleSheet(label_style)
        grid2.addWidget(label2)
        grid2.addWidget(self.tree_widget)

        # Tab3: 自动化爬虫控制（优化布局）
        tab3 = QWidget()
        vbox3 = QVBoxLayout(tab3)
        label3 = QLabel("自动化爬虫")
        label3.setStyleSheet(label_style)
        vbox3.addWidget(label3)

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

        # 将Tab添加到TabWidget
        tab_style = """
            QTabWidget::pane {
                border: 2px solid #bdbdbd;
                background: #f5f5f5;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                color: #333;
                padding: 10px 24px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
                font-size: 15px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #1976d2;
                font-weight: bold;
                border-bottom: 2px solid #1976d2;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
            QTabBar::tab:hover {
                background: #eeeeee;
                color: #1565c0;
            }
        """
        tab_widget.addTab(tab1, "HTML获取")
        tab_widget.addTab(tab2, "DOMTree")
        tab_widget.addTab(tab3, "自动化爬虫")
        tab_widget.setStyleSheet(tab_style)

        self.show()

    def load_soup(self):
        if self.html_widget.soup:
            self.tree_widget.load_soup(self.html_widget.soup)
            self.html_widget.html_view.print("DOMTree已更新")
        else:
            QMessageBox.warning(self, "警告", "请先加载HTML内容！")
   

if __name__ == "__main__":
    app = QApplication([])
    with open("src/test/data/output1.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = parse_html(html_content, remove_script=True, remove_style=True)

    mainWindow = MainWindow(soup)
    app.exec_()
