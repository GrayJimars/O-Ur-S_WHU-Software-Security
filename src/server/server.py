# -*- coding: utf-8 -*-
import asyncio
import threading
import ctypes
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtWidgets
from Ui_server import *
from operation_modules import *
import random
import socket



class Server(Ui_ServerMainWindow, QtWidgets.QMainWindow):
    connection_request_signal = QtCore.pyqtSignal(
        str, int, object, name='connectionRequestSignal')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "myappid")

        self.serverState.setText("停止监听")
        self.server_task = None
        self.loop = asyncio.new_event_loop()
        self.startServer.clicked.connect(self.startServerClicked)
        self.stopServer.clicked.connect(self.stopServerClicked)
        self.connection_request_signal.connect(self.show_connection_request)
        self.whiteList = {}

    def get_random_available_port(self):
        while True:
            # 生成一个随机端口号，范围在1024到65535之间
            port = random.randint(1024, 65535)
            # 尝试创建一个socket并绑定到该端口，检查端口是否可用
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(('localhost', port))
                # connect_ex() 返回 0 表示端口可用
                if result != 0:
                    return port  # 如果端口可用，返回该端口

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
        client_host = self.ipInput.text()
        client_port = self.portInput.text()
        client_address = (client_host, client_port)

        asyncio.run_coroutine_threadsafe(
            self.start_server(client_address), self.loop)
        threading.Thread(target=self.run_event_loop, daemon=True).start()

    def run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def get_local_ip(self):
        # 获取本地机器的主机名
        hostname = socket.gethostname()
        
        # 获取本地机器的 IP 地址
        local_ip = socket.gethostbyname(hostname)
        
        return local_ip

    async def send_receive_for_client(self, target_address, data):
        try:
            data = f"{data[0]}:{data[1]}"
            reader, writer = await asyncio.open_connection(target_address[0], target_address[1])
            writer.write(data.encode())
            await writer.drain()
            self.log_message(f"已向 {target_address[0]}:{target_address[1]} 发送数据: {data}")
            try:
                # 使用 asyncio.wait_for 设置 5 秒超时时间
                response = await asyncio.wait_for(reader.read(1024), timeout=5)  # 假设最大响应长度为1024字节
                self.log_message(f"收到客户端 {target_address[0]}:{target_address[1]} 的回复: {response.decode()}")
                writer.close()
                await writer.wait_closed()
                return response.decode()
            except asyncio.TimeoutError:
                self.log_message("[!] 接收数据超时（5 秒），未收到客户端回复。")
                writer.close()
                await writer.wait_closed()
                return None
        except Exception as e:
            self.log_message(f"发送数据失败！{e}")
            try:
                writer.close()
                await writer.wait_closed()
                return None
            except:
                return None

    async def wait_for_client_reply(self, target_address, client_address):
        try:
            while True:
                try:
                    self.log_message(f"正在向 {target_address[0]}:{target_address[1]} 发送 IP 和端口信息...")
                    # 等待客户端回复，并设置超时时间为5秒
                    reply = await self.send_receive_for_client(target_address,client_address)
                    if(reply != None):
                        # 如果接收到客户端的回复，退出循环
                        self.log_message("客户端已回复，停止发送数据。")
                        break  # 收到回复，跳出循环
                    elif(self.startServer.isEnabled()):
                        self.log_message("正在停止服务")
                        break
                except asyncio.TimeoutError:
                    # 如果超时没有收到回复，继续发送数据并等待
                    self.log_message("[!] 超时，继续等待客户端回复...")
        except Exception as e:
            self.log_message(f"[!] 等待客户端回复失败: {e}")

        except Exception as e:
            # 处理其他错误
            self.log_message(f"[!] 发生错误: {e}")

    async def start_server(self, client_address):
        random_port = str(self.get_random_available_port())
        self.portInput.setText(random_port)
        self.ipInput.setText("0.0.0.0")
        client_host, client_port = client_address
        client_address = ("0.0.0.0", random_port)
        self.log_message(
            f"[*] 正在启动服务器，监听地址为 {client_address[0]}:{client_address[1]}")
        self.serverState.setText("监听中")
        try:
            self.log_message(
                f"正在连接到客户端......")
            #每隔5秒向指定ip和端口发送client_address，直到客户端回复receive
            localip = str(self.get_local_ip())
            target_address = (localip, '25577')
            await self.wait_for_client_reply(target_address,(localip,random_port))
            server = await asyncio.start_server(self.handle_client, *client_address)
            self.log_message(
                f"[*] 服务器已启动，正在监听 {client_address[0]}:{client_address[1]}")
            async with server:
                self.server_task = server
                await server.serve_forever()
        except Exception as e:
            self.log_message(f"[!] 错误: {e}")
            self.serverState.setText("停止监听")

    def stopServerClicked(self):
        self.startServer.setEnabled(True)
        self.stopServer.setEnabled(False)
        if self.server_task:
            self.server_task.close()
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.serverState.setText("停止监听")
            self.log_message("[*] 服务器已停止监听")

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')

        if addr[0] not in self.whiteList.values():
            confirm = await self.ask_connection_permission(addr[0], addr[1])
        else:
            confirm = QMessageBox.Yes

        if confirm == QMessageBox.No:
            self.log_message(
                f"[*] 来自 {addr[0]}:{addr[1]} 的连接请求被拒绝")
            writer.close()
            await writer.wait_closed()
            return
        else:
            if addr[0] not in self.whiteList.values():
                self.log_message(f"[*] 地址 {addr[0]} 被加入白名单")
            self.whiteList[addr[1]] = addr[0]

        self.log_message(f"[*] 来自 {addr[0]}:{addr[1]} 的连接请求已接受")

        operation = await reader.read(1024)
        if not operation:
            self.log_message(
                f"[*] 空白操作请求来自 {addr[0]}:{addr[1]}，连接将关闭")
            writer.close()
            await writer.wait_closed()
            return

        # 解码操作内容
        operation_str = operation.decode('utf-8').strip()

        # 根据操作类型调用不同的处理函数
        if operation_str == "fileManager":
            operation = "File manager opened"
            self.log_message(f"[*] 文件管理器已被 {addr[0]}:{addr[1]} 打开")
            writer.write(operation.encode())
            await writer.drain()
            # self.log_message(f"[*] 文件管理器确认")
            await open_file_manager(self, writer, reader)
        elif operation_str == "regManager":
            operation = "Register manager opened"
            self.log_message(
                f"[*] 注册表管理器已被 {addr[0]}:{addr[1]} 打开")
            writer.write(operation.encode())
            await writer.drain()
            await open_reg_manager(self, writer, reader)
        elif operation_str == "openCamera":
            operation = "Camera opened"
            self.log_message(f"[*] 摄像头已被 {addr[0]}:{addr[1]} 打开")
            writer.write(operation.encode())
            await writer.drain()
            await open_camera(self, writer, reader)
        elif operation_str == "openMicrophone":
            operation = "Microphone opened"
            self.log_message(f"[*] 麦克风已被 {addr[0]}:{addr[1]} 打开")
            writer.write(operation.encode())
            await writer.drain()
            await open_microphone(self, writer, reader)
        elif operation_str == "keylogger":
            operation = "Keylogger started"
            self.log_message(f"[*] 键盘记录器已被 {addr[0]}:{addr[1]} 打开")
            writer.write(operation.encode())
            await writer.drain()
            await start_keylogger(self, writer, reader)
        else:
            self.log_message(f"[*] 未知操作请求来自 {addr[0]}:{addr[1]}，连接将关闭")
            writer.close()
            await writer.wait_closed()
            return

        self.log_message(f"[*] 来自 {addr[0]}:{addr[1]} 的连接已关闭")
        self.whiteList.pop(addr[1])
        if addr[0] not in self.whiteList.values():
            self.log_message(f"[*] 地址 {addr[0]} 已从白名单中移除")

    async def ask_connection_permission(self, host, port):
        future = asyncio.Future()
        self.connection_request_signal.emit(host, port, future)
        self.log_message(
            f"[*] 为来自 {host}:{port} 的连接请求确认")
        return await future

    @QtCore.pyqtSlot(str, int, object)
    def show_connection_request(self, host, port, future):
        confirm = QMessageBox.question(
            self,
            "连接请求",
            f"来自 {host}:{port} 的连接请求，是否接受？",
            QMessageBox.Yes | QMessageBox.No
        )
        self.loop.call_soon_threadsafe(future.set_result, confirm)

    def closeEvent(self, event):
        self.loop.call_soon_threadsafe(self.loop.stop)
        event.accept()

if __name__ == "__main__":
    import sys
    from qasync import QEventLoop
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    server = Server()
    server.show()
    with loop:
        sys.exit(loop.run_forever())
