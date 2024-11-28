import asyncio


async def fileManager(GUI):
    try:
        # ���ı����ȡ�ַ���
        server_address = (GUI.ipInput.text(), GUI.portInput.text())
        GUI.append_log(
            f"[*] Connecting to: {server_address[0]}:{server_address[1]}")
        reader, writer = await asyncio.open_connection(*server_address)
        while (1):
            break
        GUI.append_log(
            f"[*] Connected to: {server_address[0]}:{server_address[1]}")

        operation = "Hello, Server!"
        writer.write(operation.encode())
        await writer.drain()
        GUI.append_log(f"[*] Sent operation: {operation}")

        # �ȴ���������Ӧ
        GUI.append_log("[*] Waiting for response...")
        response = await reader.read(1024)
        GUI.append_log(f"[*] Received response: {response.decode('utf-8')}")
    except OSError as e:
        GUI.append_log(f"[!] Network error: {e}")
    except Exception as e:
        GUI.append_log(f"[!] Unexpected error: {e}")
    finally:
        # �ر�����
        writer.close()
        await writer.wait_closed()
        GUI.append_log("[*] Connection closed")
