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

        # ����һ���¼�ѭ�����з�����
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

        # �첽�������߳�ȷ���Ƿ��������
        confirm = await self.ask_connection_permission(addr[0], addr[1])
        if confirm == QMessageBox.No:
            self.log_message(f"[*] Connection from {addr[0]}:{addr[1]} rejected")
            writer.close()
            await writer.wait_closed()
            return

        self.log_message(f"[*] Connection from {addr[0]}:{addr[1]} accepted")

        # ��ȡ�ͻ��˷��͵�����
        self.log_message(f"[*] Waiting for operation from {addr[0]}:{addr[1]}...")
        operation = await reader.read(1024)
        if not operation:
            self.log_message(f"[*] Blank operation received from {addr[0]}:{addr[1]}")
            writer.close()
            await writer.wait_closed()
            return

        # 解码操作内容
        operation_str = operation.decode('utf-8').strip()
        
        # 根据操作类型调用不同的处理函数
        if operation_str == "fileManager":
            operation = "File manager opened"
            writer.write(operation.encode())
            await writer.drain()
            await open_file_manager(self,writer,reader)
        elif operation_str == "regManager":
            operation = "Register manager opened"
            writer.write(operation.encode())
            await writer.drain()
            await open_reg_manager(self,writer,reader)
        elif operation_str == "openCamera":
            operation = "Camera opened"
            writer.write(operation.encode())
            await writer.drain()
            await open_camera(self,writer,reader)
        elif operation_str == "openMicrophone":
            operation = "Microphone opened"
            writer.write(operation.encode())
            await writer.drain()
            await open_microphone(self,writer,reader)
        elif operation_str == "keylogger":
            operation = "Keylogger started"
            writer.write(operation.encode())
            await writer.drain()
            await start_keylogger(self,writer,reader)
        else:
            self.log_message(f"[*] Unknown operation: {operation_str}")
            writer.close()
            await writer.wait_closed()
            return

        self.log_message(f"[*] Connection with {addr[0]}:{addr[1]} closed")

    async def ask_connection_permission(self, host, port):
        future = asyncio.Future()
        self.connection_request_signal.emit(host, port, future)
        self.log_message(f"[*] Signal emitted for connection from {host}:{port}")
        return await future

    @QtCore.pyqtSlot(str, int, object)
    def show_connection_request(self, host, port, future):
        # ʹ�� Qt ���¼����Ʊ�������
        confirm = QMessageBox.question(
            self,
            "Connection Request",
            f"Accept connection from {host}:{port}?",
            QMessageBox.Yes | QMessageBox.No
        )
        # ʹ�� call_soon_threadsafe ȷ���̰߳�ȫ������ future �Ľ��
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
