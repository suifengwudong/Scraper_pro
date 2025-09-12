from PyQt5.QtWidgets import (
    QApplication,
    QWidget, QVBoxLayout,
    QTextEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent

class OutputView(QWidget):
    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowFlags | Qt.WindowType = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)
        self.setWindowTitle("输出视图")

        layout = QVBoxLayout(self)
        self._font_size = 25
        self._base_style = """
            QTextEdit {{
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, 'Courier New', monospace;
                font-size: {}px;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
            }}
        """
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText(">>>")
        self._update_font_size()
        layout.addWidget(self.text_edit)

    def _update_font_size(self):
        self.text_edit.setStyleSheet(self._base_style.format(self._font_size))

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self._font_size = min(self._font_size + 1, 40)
            else:
                self._font_size = max(self._font_size - 1, 8)
            self._update_font_size()
            event.accept()
        else:
            super().wheelEvent(event)

    def print(self, text: str, append_mode: bool = True):
        if append_mode:
            self.text_edit.append(f">>> {text}")
        else:
            self.text_edit.setPlainText(f">>> {text}")

    def clear(self):
        self.text_edit.clear()


if __name__ == "__main__":
    app = QApplication([])
    window = OutputView()
    window.print("This is a test message.")
    window.show()
    app.exec_()