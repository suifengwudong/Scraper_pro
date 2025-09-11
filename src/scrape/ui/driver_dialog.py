from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout, QGridLayout,
    QFileDialog, QDialog, QLabel, QPushButton, QComboBox, QTextEdit,
    QWidget
)
from web import web_configs, WebConfig

class DriverDialog(QDialog):
    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowFlags = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)

        self.label = QLabel("选择浏览器驱动路径:", self)
        self.select_btn = QPushButton("选择", self)
        self.ok_btn = QPushButton("确定", self)
        self.cancel_btn = QPushButton("取消", self)
        self.info = QTextEdit(self)
        self.info.setReadOnly(True)

        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.select_btn, 0, 1)
        layout.addWidget(self.info, 1, 0, 1, 2)
        layout.addWidget(self.ok_btn, 2, 0)
        layout.addWidget(self.cancel_btn, 2, 1)
        self.setLayout(layout)

        self.select_btn.clicked.connect(self.select_driver)

    def select_driver(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择浏览器驱动",
            "",
            "Executable Files (*.exe);;All Files (*)",
            options=options
        )
        if file_path:
            self.info.setText('>>>' + file_path)
        if 'edge' in file_path.lower():
            web_configs["DEFAULT_BROWSER"] = "edge"
            self.info.append('\n>>>' + "已选择Edge浏览器驱动")
        elif 'chrome' in file_path.lower():
            web_configs["DEFAULT_BROWSER"] = "chrome"
            self.info.append('\n>>>' + "已选择Chrome浏览器驱动")
        elif 'firefox' in file_path.lower():
            web_configs["DEFAULT_BROWSER"] = "firefox"
            self.info.append('\n>>>' + "已选择Firefox浏览器驱动")
        WebConfig.save()


if __name__ == "__main__":
    app = QApplication([])
    dlg = DriverDialog()
    dlg.show()
    app.exec_()