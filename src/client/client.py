# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_client import *
import socket
import asyncio
import qasync

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
        loop.create_task(self.start_client(server_address))

    async def start_client(self, server_address):
        try:
            reader, writer = await asyncio.open_connection(*server_address)
            self.append_log(f"[*] Connected to: {server_address[0]}:{server_address[1]}")

            # 发送数据
            message = "Hello, Server!"
            self.append_log(f"[*] Sending data: {message}")
            writer.write(message.encode())
            await writer.drain()

            # 等待服务器响应
            self.append_log("[*] Waiting for response...")
            response = await reader.read(1024)
            self.append_log(f"[*] Received response: {response.decode('utf-8')}")
        except OSError as e:
            self.append_log(f"[!] Network error: {e}")
        except Exception as e:
            self.append_log(f"[!] Unexpected error: {e}")
        finally:
            # 关闭连接
            writer.close()
            await writer.wait_closed()
            self.append_log("[*] Connection closed")

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
