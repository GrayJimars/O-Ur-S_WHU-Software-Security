import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

# 定义Keylogger窗口
class KeyloggerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keylogger Data")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建滚动文本框显示按键信息
        self.text_box = QTextEdit(self)
        self.text_box.setReadOnly(True)  # 设置为只读模式
        
        # 创建关闭按钮
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.text_box)
        layout.addWidget(self.close_button)
        
        # 设置一个主窗口的 widget 来承载布局
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_display(self, key_buffer):
        """ 更新按键信息的显示 """
        # 将 key_buffer 数据更新到文本框
        self.text_box.append(" ".join(key_buffer))
        
        # 获取滚动条，并将其设置到最底部
        scrollbar = self.text_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())  # 滚动条滚动到最大值（即底部）


# 管理键盘窗口和根窗口
class KeyloggerManager:
    def __init__(self):
        # 创建主应用程序实例
        self.app = QApplication(sys.argv)
        self.keylogger_window = None  # 存储keylogger窗口实例

    def open_keylogger_window(self):
        """ 打开 Keylogger 窗口 """
        if self.keylogger_window is None:  # 如果窗口已被关闭
            self.keylogger_window = KeyloggerWindow()
            self.keylogger_window.show()

    def close_keylogger_window(self):
        """ 关闭 Keylogger 窗口 """
        if self.keylogger_window:
            self.keylogger_window.close()  # 关闭窗口
            self.keylogger_window = None  # 将窗口实例设为 None，表示窗口已被关闭

    def start(self):
        """ 启动Qt应用程序的事件循环 """
        sys.exit(self.app.exec_())

