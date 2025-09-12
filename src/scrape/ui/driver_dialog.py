from web import web_configs, WebConfig
from .output_view import OutputView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QFileDialog, QDialog, QLabel, QPushButton,
    QWidget
)

class DriverDialog(QDialog):
    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowFlags = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)

        self.label = QLabel("选择浏览器驱动路径:", self)
        self.select_btn = QPushButton("选择", self)
        self.ok_btn = QPushButton("确定", self)
        self.cancel_btn = QPushButton("取消", self)
        self.info = OutputView()

        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.select_btn, 0, 1)
        layout.addWidget(self.info, 1, 0, 1, 2)
        layout.addWidget(self.ok_btn, 2, 0)
        layout.addWidget(self.cancel_btn, 2, 1)
        self.setLayout(layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.select_btn.clicked.connect(self.select_driver)

    def select_driver(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择浏览器驱动",
            "",
            "Executable Files (*.exe);;All Files (*)",
            options=options
        )
        if file_path:
            self.info.print(file_path)

        for browser in ("chrome", "edge", "firefox"):
            if browser in file_path.lower():
                self.selected_driver = browser
                web_configs["DEFAULT_BROWSER"] = browser
                self.info.print(f"已选择{browser}浏览器驱动")
                break
        else:
            self.selected_driver = ""
            self.info.print('警告: 未识别的浏览器驱动，请确保驱动与浏览器匹配！')
        WebConfig.save()


if __name__ == "__main__":
    app = QApplication([])
    dlg = DriverDialog()
    dlg.show()
    app.exec_()