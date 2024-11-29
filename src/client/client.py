# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from Ui_client import *
import asyncio
import qasync
from operation_modules import *


class Client(Ui_ClientMainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fileManager.clicked.connect(self.fileManagerClicked)
        self.keylogger.clicked.connect(self.keyloggerClicked)
        self.regManager.clicked.connect(self.regManagerClicked)
        self.openMicrophone.clicked.connect(self.openMicrophoneClicked)
        self.openCamera.clicked.connect(self.openCameraClicked)
        self.Connect.clicked.connect(self.connect)
        self.disConnect.clicked.connect(self.disconnect)
        self.connections = {
            'fileManager': {'reader': None, 'writer': None},
            'regManager': {'reader': None, 'writer': None},
            'openCamera': {'reader': None, 'writer': None},
            'openMicrophone': {'reader': None, 'writer': None},
            'keylogger': {'reader': None, 'writer': None}
        }

    def append_log(self, message):
        QtCore.QMetaObject.invokeMethod(
            self.textBrowser, "append", QtCore.Q_ARG(str, message))

    def connect(self):
        loop = asyncio.get_event_loop()
        loop.create_task(connected(self))

    def disconnect(self):
        loop = asyncio.get_event_loop()
        loop.create_task(disconnected(self))

    def fileManagerClicked(self):
        loop = asyncio.get_event_loop()
        loop.create_task(fileManager(self))

    def regManagerClicked(self):
        loop = asyncio.get_event_loop()
        loop.create_task(regmanager(self))

    def keyloggerClicked(self):
        loop = asyncio.get_event_loop()
        loop.create_task(keylogger(self))

    def openCameraClicked(self):
        loop = asyncio.get_event_loop()
        loop.create_task(opencamera(self))

    def openMicrophoneClicked(self):
        loop = asyncio.get_event_loop()
        loop.create_task(openmicrophone(self))


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
