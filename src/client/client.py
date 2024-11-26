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
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ����socket����
        client.connect(server_address) # ���ӷ�����
        client.send("Hello, World!".encode()) # ��������
        response = client.recv(1024) # ��������
        self.textBrowser.append(response.decode('utf-8')) # ��ʾ����
        client.close() # �ر�����
    
    def fileManagerClicked(self):
        server_host = socket.gethostname() # ��ȡ����������
        server_port = 25566 # �˿ں�
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