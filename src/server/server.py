# -*- coding: utf-8 -*-
import socket
import asyncio
import threading
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtWidgets
from Ui_server import *
from operation_modules import *

class Server(Ui_ServerMainWindow, QtWidgets.QMainWindow):
    connection_request_signal = QtCore.pyqtSignal(str, int, object, name='connectionRequestSignal')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serverState.setText("Not Listening")
        self.server_task = None
        self.loop = asyncio.new_event_loop()
        self.startServer.clicked.connect(self.startServerClicked)
        self.stopServer.clicked.connect(self.stopServerClicked)
        self.connection_request_signal.connect(self.show_connection_request)

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
            self.log_message(f"[*] Server is running on {client_address[0]}:{client_address[1]}")
            async with server:
                self.server_task = server
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
            self.serverState.setText("Stopped")
            self.log_message("[*] Server stopped")

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')

        # 异步请求主线程确认是否接受连接
        confirm = await self.ask_connection_permission(addr[0], addr[1])
        if confirm == QMessageBox.No:
            self.log_message(f"[*] Connection from {addr[0]}:{addr[1]} rejected")
            writer.close()
            await writer.wait_closed()
            return

        self.log_message(f"[*] Connection from {addr[0]}:{addr[1]} accepted")

        # 读取客户端发送的数据
        self.log_message(f"[*] Waiting for operation from {addr[0]}:{addr[1]}...")
        operation = await reader.read(1024)
        if not operation:
            self.log_message(f"[*] Blank operation \"{operation}\" received from {addr[0]}:{addr[1]}")
            writer.close()
            await writer.wait_closed()
            return

        # 处理操作
        await handle_operation(self, operation, writer, reader)
        self.log_message(f"[*] Connection with {addr[0]}:{addr[1]} closed")

    async def ask_connection_permission(self, host, port):
        future = asyncio.Future()
        self.connection_request_signal.emit(host, port, future)
        self.log_message(f"[*] Signal emitted for connection from {host}:{port}")
        return await future

    @QtCore.pyqtSlot(str, int, object)
    def show_connection_request(self, host, port, future):
        # 使用 Qt 的事件机制避免阻塞
        confirm = QMessageBox.question(
            self,
            "Connection Request",
            f"Accept connection from {host}:{port}?",
            QMessageBox.Yes | QMessageBox.No
        )
        # 使用 call_soon_threadsafe 确保线程安全地设置 future 的结果
        self.loop.call_soon_threadsafe(future.set_result, confirm)

    def closeEvent(self, event):
        self.loop.call_soon_threadsafe(self.loop.stop)
        event.accept()


if __name__ == "__main__":
    import sys
    from qasync import QEventLoop
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    server = Server()
    server.show()
    with loop:
        sys.exit(loop.run_forever())
