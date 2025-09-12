from web import *
from .driver_dialog import DriverDialog
from .output_view import OutputView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget, QVBoxLayout, QHBoxLayout, QDialog, QMessageBox,
    QTextEdit, QLineEdit, QPushButton, QComboBox
)

class HTMLWidget(QWidget):
    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowFlags = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)

        self.driver = None
        self.is_driver_loaded = False
        self.option = 0  # 0: requests, 1: selenium
        vbox1 = QVBoxLayout(self)

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

        self.html_view = OutputView()
        vbox1.addWidget(self.html_view)

        self.option_combo.currentTextChanged.connect(self.on_option_changed)
        self.load_driver_btn.clicked.connect(self.load_driver)
        self.load_html_btn.clicked.connect(self.load_html)

    def on_option_changed(self, text: str):
        if text.lower() == "selenium":
            self.option = 1
            self.load_driver_btn.setEnabled(True)
        else:
            self.option = 0
            self.load_driver_btn.setEnabled(False)

    def load_driver(self):
        self.is_driver_loaded = True
        if web_configs["DEFAULT_BROWSER"] == "":
            dlg = DriverDialog(self)
            dlg.exec_()
            if dlg.result() == QDialog.DialogCode.Accepted:
                self.html_view.print(f"浏览器驱动已设置为: {dlg.selected_driver}")
            else:
                self.html_view.print("浏览器驱动加载取消")
                self.is_driver_loaded = False
        self.driver = Driver(web_configs["DEFAULT_BROWSER"], web_configs["BROWSER_PATH_DICT"][web_configs["DEFAULT_BROWSER"]])

    def load_html(self):
        if self.option and not self.is_driver_loaded:
            QMessageBox.warning(self, "警告", "!!浏览器驱动未加载!!")
            return
        if not self.url_edit.text().strip():
            QMessageBox.warning(self, "警告", "请输入有效的网址！")
            return
        html = fetch_html(self.url_edit.text(), self.option_combo.currentText(), 
                         driver=self.driver if self.option else None)
        self.soup = parse_html(html, remove_script=True, remove_style=True)
        self.html_view.print(str(self.soup.prettify()), append_mode=False)