# -*- coding: utf-8 -*-
async def clientFileManager(GUI, writer, reader, operation):
    if operation == "fileList":
        serverPath = GUI.serverFilePath.text()
        GUI.fileManagerOutput.append(f"浏览文件夹")
        writer.write(f"fileList".encode())
        await writer.drain()
        await reader.read(1024)
        GUI.fileManagerOutput.append(f"路径: {serverPath}")
        writer.write(serverPath.encode())
        await writer.drain()
        fileList = await reader.read(1024)
        GUI.fileManagerOutput.append(fileList.decode())

    elif operation == "fileDownload":
        clientPath = GUI.clientFilePath.text()
        serverPath = GUI.serverFilePath.text()
        GUI.fileManagerOutput.append(f"下载文件")
        writer.write(f"fileDownload".encode())
        await writer.drain()
        await reader.read(1024)
        GUI.fileManagerOutput.append(f"将{serverPath}")
        writer.write(serverPath.encode())
        await writer.drain()
        await reader.read(1024)
        GUI.fileManagerOutput.append(f"下载到{clientPath}")
        writer.write(clientPath.encode())
        await writer.drain()
        # 拆分接收
        with open(clientPath, "wb") as file:
            while True:
                data = await reader.read(1024)
                if data.endswith(b"EOFGrayJimars"):
                    # 去掉结尾的EOF并写入文件
                    file.write(data[:-13])
                    break
                file.write(data)
        GUI.fileManagerOutput.append(f"下载完成")

    elif operation == "fileUpload":
        clientPath = GUI.clientFilePath.text()
        serverPath = GUI.serverFilePath.text()
        GUI.fileManagerOutput.append(f"上传文件")
        writer.write(f"fileUpload".encode())
        await writer.drain()
        await reader.read(1024)
        GUI.fileManagerOutput.append(f"将{clientPath}")
        writer.write(clientPath.encode())
        await writer.drain()
        await reader.read(1024)
        GUI.fileManagerOutput.append(f"上传到{serverPath}")
        writer.write(serverPath.encode())
        await writer.drain()
        await reader.read(1024)
        # 拆分发送
        with open(clientPath, "rb") as file:
            while True:
                data = file.read(1024)
                if not data:
                    writer.write(b"EOFGrayJimars")
                    await writer.drain()
                    break
                writer.write(data)
                await writer.drain()
        GUI.fileManagerOutput.append(f"上传完成")

    elif operation == "fileExcute":
        serverPath = GUI.serverFilePath.text()
        GUI.fileManagerOutput.append(f"执行文件")
        writer.write(f"fileExcute".encode())
        await writer.drain()
        await reader.read(1024)
        GUI.fileManagerOutput.append(f"目标: {serverPath}")
        writer.write(serverPath.encode())
        await writer.drain()
        result = await reader.read(1024)
        GUI.fileManagerOutput.append(f"结果")
        GUI.fileManagerOutput.append(result.decode())

    return
