# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_client import *
import socket
import asyncio
import qasync
from operation_modules import *

class Client(Ui_ClientMainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fileManager.clicked.connect(self.fileManagerClicked)

    def append_log(self, message):
        QtCore.QMetaObject.invokeMethod(self.textBrowser, "append", QtCore.Q_ARG(str, message))

    def fileManagerClicked(self):
        server_host = socket.gethostname()
        server_port = 25566
        server_address = (server_host, server_port)
        self.append_log(f"[*] Connecting to: {server_host}:{server_port}")

        loop = asyncio.get_event_loop()
        loop.create_task(fileManager(self, server_address))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    client = Client()
    client.show()

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_forever()
