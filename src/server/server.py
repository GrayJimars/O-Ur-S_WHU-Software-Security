# -*- coding: utf-8 -*-
import socket
import asyncio
import threading
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
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
        self.textBrowser.append(f"[*] Starting server on {client_address[0]}:{client_address[1]}")
        self.serverState.setText("Listening")
        try:
            server = await asyncio.start_server(self.handle_client, *client_address)
            self.textBrowser.append(f"[*] Server is running on {client_address[0]}:{client_address[1]}")
            async with server:
                self.server_task = server
                await server.serve_forever()
        except ConnectionResetError as e:
            self.textBrowser.append(f"[!] Connection reset error: {e}")
            self.serverState.setText("Not Listening")
        except Exception as e:
            self.textBrowser.append(f"[!] An error occurred: {e}")
            self.serverState.setText("Not Listening")

    def stopServerClicked(self):
        self.startServer.setEnabled(True)
        self.stopServer.setEnabled(False)
        if self.server_task:
            self.server_task.close()
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.serverState.setText("Stopped")
            self.textBrowser.append("[*] Server stopped")

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        self.textBrowser.append(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # 发送一条消息
        writer.write(b"Hello, you are connected!\n")
        await writer.drain()

        # 关闭连接
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = Server()
    window.show()
    sys.exit(app.exec_())