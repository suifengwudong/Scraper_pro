from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QWidget, QVBoxLayout, QStackedWidget,
    QLineEdit, QPushButton
)
from ui.tree_widget import DOMTreeWidget
from web.parse_html import parse_html
from bs4 import Tag

class MainWindow(QMainWindow):
    def __init__(self, soup: Tag):
        super().__init__()

        '''Setup central widget'''
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowTitle("DOM Tree Viewer")
        self.resize(900, 600)

        '''Build UI components'''
        self.tree_widget = DOMTreeWidget(soup)
        self.line_edit = QLineEdit()
        self.button = QPushButton("Fetch Selected")

        '''Layout setup'''
        v_box1 = QVBoxLayout(central_widget)
        v_box1.addWidget(self.line_edit)
        v_box1.addWidget(self.button)
        v_box1.addWidget(self.tree_widget)

        self.show()

if __name__ == "__main__":
    app = QApplication([])

    with open("src/test/data/output1.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = parse_html(html_content, remove_script=True, remove_style=True)

    mainWindow = MainWindow(soup)
    app.exec_()
