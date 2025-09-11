from PyQt5.QtWidgets import (
    QApplication,
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTreeWidget, QTreeWidgetItem, QHeaderView,
    QComboBox, QLineEdit, QCheckBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from bs4 import Tag

class InvalidHtmlError(Exception):
    pass


class DOMTreeWidget(QWidget):
    '''DOM Tree Widget with filtering and execution mode'''
    def __init__(self, soup: Tag):
        super().__init__()

        self.soup = soup
        self.tag_set = set()
        self.attr_set = set()
        self._collect_tags_attrs(soup)

        # 筛选区控件
        self.tag_combo = QComboBox()
        self.tag_combo.setEditable(True)
        self.tag_combo.addItem("全部")
        self.tag_combo.addItems(sorted(self.tag_set))
        self.tag_combo.setCurrentIndex(0)

        self.attr_combo = QComboBox()
        self.attr_combo.setEditable(True)
        self.attr_combo.addItem("全部")
        self.attr_combo.addItems(sorted(self.attr_set))
        self.attr_combo.setCurrentIndex(0)

        self.value_edit = QLineEdit()
        self.value_edit.setPlaceholderText("属性值/模糊检索")

        # 模式控件
        self.recursive_checkbox = QCheckBox("递归修改模式")
        self.recursive_checkbox.setChecked(True)

        # 筛选区布局
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("标签:"))
        filter_layout.addWidget(self.tag_combo)
        filter_layout.addWidget(QLabel("属性:"))
        filter_layout.addWidget(self.attr_combo)
        filter_layout.addWidget(QLabel("值:"))
        filter_layout.addWidget(self.value_edit)

        # 模式控件布局
        mode_layout = QGridLayout()
        mode_layout.addWidget(self.recursive_checkbox)

        # 树控件
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["标签", "属性", "选择"])
        self.tree.resize(900, 600)
        self.tree.setStyleSheet("""
            QTreeWidget::item {
                border-bottom: 1px solid #eee;
            }
            QTreeWidget::item:selected {
                background: #124197;
            }
        """)
        self.tree.setFont(QFont("Consolas"))
        header = self.tree.header()
        if header is None:
            raise RuntimeError("Tree header is not available.")
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.tree.setColumnWidth(2, 80)
        header.setStretchLastSection(False)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(filter_layout)
        main_layout.addLayout(mode_layout)
        main_layout.addWidget(self.tree)
        self.setLayout(main_layout)
        self.resize(900, 600)

        # 初始化树
        self._populate_tree()

        # 信号连接
        self.tag_combo.currentTextChanged.connect(self._on_filter_changed)
        self.attr_combo.currentTextChanged.connect(self._on_filter_changed)
        self.value_edit.textChanged.connect(self._on_filter_changed)
        self.tree.itemChanged.connect(self.onCheckStateChanged)

    def _collect_tags_attrs(self, soup: Tag):
        '''收集所有tag和attribute种类'''
        def walk(node):
            if isinstance(node, Tag):
                self.tag_set.add(node.name)
                for attr in node.attrs:
                    self.attr_set.add(attr)
                for child in node.children:
                    walk(child)
        walk(soup)

    def _populate_tree(self):
        self.tree.clear()
        html_tag = self.soup.find('html')
        if isinstance(html_tag, Tag):
            root_item = QTreeWidgetItem([html_tag.name, str(html_tag.attrs), ""])
            root_item.setCheckState(2, Qt.CheckState.Unchecked)
            self.tree.addTopLevelItem(root_item)
            self._add_dom_to_tree(html_tag, root_item)
        else:
            raise InvalidHtmlError("The provided soup does not contain an <html> tag.")

    def _add_dom_to_tree(self, soup: Tag, parent_item: QTreeWidgetItem):
        for element in soup.children:
            if isinstance(element, Tag) and element.name:
                attr_str = str(element.attrs) if element.attrs else ""
                item = QTreeWidgetItem([element.name, attr_str, ""])
                item.setCheckState(2, Qt.CheckState.Unchecked)
                parent_item.addChild(item)
                self._add_dom_to_tree(element, item)

    def _on_filter_changed(self):
        tag = self.tag_combo.currentText()
        attr = self.attr_combo.currentText()
        value = self.value_edit.text().strip()
        self._filter_tree(tag, attr, value)

    def _filter_tree(self, tag, attr, value):
        '''根据筛选条件显示/隐藏节点'''
        def match(item):
            # tag
            if tag != "全部" and item.text(0) != tag:
                return False
            # attribute
            attrs = eval(item.text(1)) if item.text(1) else {}
            if attr != "全部" and attr not in attrs:
                return False
            # value
            if value:
                if attr != "全部":
                    v = str(attrs.get(attr, ""))
                    if value not in v:
                        return False
                else:
                    # 任意属性值模糊匹配
                    if not any(value in str(v) for v in attrs.values()):
                        return False
            return True

        def walk(item):
            visible = match(item)
            for i in range(item.childCount()):
                child = item.child(i)
                child_visible = walk(child)
                visible = visible or child_visible
            item.setHidden(not visible)
            return visible

        for i in range(self.tree.topLevelItemCount()):
            walk(self.tree.topLevelItem(i))

    def onCheckStateChanged(self, item, column):
        if column != 2:
            return
        if not self.recursive_checkbox.isChecked():
            return
        # 递归修改所有当前筛选下的子节点
        state = item.checkState(2)
        def walk(item):
            if not item.isHidden():
                item.setCheckState(2, state)
                for i in range(item.childCount()):
                    walk(item.child(i))
        walk(item)

    def update(self):
        self.tree.update()

if __name__ == "__main__":
    app = QApplication([])

    with open("src/test/data/output1.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    from parse_html import parse_html
    soup = parse_html(html_content, remove_script=True, remove_style=True)

    tree_widget = DOMTreeWidget(soup)
    tree_widget.show()
    app.exec_()