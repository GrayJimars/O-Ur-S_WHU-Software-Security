# -*- coding: utf-8 -*-
import socket
import asyncio
import threading
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtWidgets
from Ui_server import *

class Server(Ui_ServerMainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serverState.setText("Not Listening")
        self.server_task = None
        self.loop = asyncio.new_event_loop()
        self.startServer.clicked.connect(self.startServerClicked)
        self.stopServer.clicked.connect(self.stopServerClicked)

    def log_message(self, message):
        QtCore.QMetaObject.invokeMethod(
            self.textBrowser,
            "append",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, message),
        )

    def startServerClicked(self):
        self.startServer.setEnabled(False)
        self.stopServer.setEnabled(True)
        client_host = socket.gethostname()
        client_port = 25566
        client_address = (client_host, client_port)

        # 创建一个事件循环运行服务器
        asyncio.run_coroutine_threadsafe(self.start_server(client_address), self.loop)
        threading.Thread(target=self.run_event_loop, daemon=True).start()

    def run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def start_server(self, client_address):
        self.log_message(f"[*] Starting server on {client_address[0]}:{client_address[1]}")
        self.serverState.setText("Listening")
        try:
            server = await asyncio.start_server(self.handle_client, *client_address)
            self.server_task = server
            async with server:
                self.log_message(f"[*] Server is running on {client_address[0]}:{client_address[1]}")
                await server.serve_forever()
        except Exception as e:
            self.log_message(f"[!] An error occurred: {e}")
            self.serverState.setText("Not Listening")

    def stopServerClicked(self):
        self.startServer.setEnabled(True)
        self.stopServer.setEnabled(False)
        if self.server_task:
            self.server_task.close()
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.log_message("[*] Server stopped")
            self.serverState.setText("Stopped")

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        self.log_message(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        try:
            # 读取客户端发送的数据
            self.log_message(f"[*] Waiting for data from {addr[0]}:{addr[1]}...")
            data = await reader.read(1024)
            message = data.decode()
            self.log_message(f"[*] Received: {message}")

            # 发送响应数据
            response = "Hello, Client!"
            writer.write(response.encode())
            await writer.drain()
            self.log_message(f"[*] Response sent: {response}")
        except Exception as e:
            self.log_message(f"[!] Error handling client {addr}: {str(e)}")
        finally:
            # 关闭连接
            writer.close()
            await writer.wait_closed()
            self.log_message(f"[*] Connection with {addr[0]}:{addr[1]} closed")

    def closeEvent(self, event):
        self.loop.call_soon_threadsafe(self.loop.stop)
        event.accept()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = Server()
    window.show()
    sys.exit(app.exec_())
