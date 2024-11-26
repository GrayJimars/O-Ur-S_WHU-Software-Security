# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_client import *
import socket

class Client(Ui_ClientMainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fileManager.clicked.connect(self.fileManagerClicked)
        # self.regManager.clicked.connect(self.regManagerClicked)
        # self.openCamera.clicked.connect(self.openCameraClicked)
        # self.openMicrophone.clicked.connect(self.openMicrophoneClicked)
        # self.keylogger.clicked.connect(self.keyloggerClicked)
        
    def start_client(self, server_address):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建socket对象
        client.connect(server_address) # 连接服务器
        client.send("Hello, World!".encode()) # 发送数据
        response = client.recv(1024) # 接收数据
        self.textBrowser.append(response.decode('utf-8')) # 显示数据
        client.close() # 关闭连接
    
    def fileManagerClicked(self):
        server_host = socket.gethostname() # 获取本地主机名
        server_port = 25566 # 端口号
        server_address = (server_host, server_port)
        self.textBrowser.append(f"[*] Connecting to: {server_host}:{server_port}")
        # self.server_address = (self.ipInput.text(), int(self.portInput.text()))
        self.start_client(server_address)
    
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())