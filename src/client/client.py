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

    def append_log(self, message):
        QtCore.QMetaObject.invokeMethod(self.textBrowser, "append", QtCore.Q_ARG(str, message))

    def fileManagerClicked(self):
        loop = asyncio.get_event_loop()
        loop.create_task(fileManager(self))


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
