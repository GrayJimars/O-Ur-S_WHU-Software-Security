async def handle_operation(GUI, operation, writer, reader):
    operation = operation.decode()
    print(f"[*] Received operation: {operation}")
    
    if operation == "Hello, Server!":
        GUI.textBrowser.append("[*] Received data: Hello, Server!")
        response = "Hello, Client!"
        
        GUI.textBrowser.append(f"[*] Sending response: {response}")
        writer.write(response.encode())
        await writer.drain()
        writer.close()
        return
    # elif operation == "fileManager":
    #     fileManager()
    else:
        GUI.textBrowser.append("[!] Invalid operation: {operation}")
        writer.write("Invalid operation".encode())
        await writer.drain()
        writer.close()
        return
    
async def open_file_manager(GUI,writer,reader):
    # 这里放具体的操作
    while(1):
        response = await reader.read(1024)
        if(response):
            operation = "Im file manager!"
            writer.write(operation.encode())
            await writer.drain()
        else:
            writer.close()
            return


async def open_reg_manager(GUI,writer,reader):
    # 这里放具体的操作
    while(1):
        response = await reader.read(1024)
        if(response):
            operation = "Im reg manager!"
            writer.write(operation.encode())
            await writer.drain()
        else:
            writer.close()
            return

async def open_camera(GUI,writer,reader):
    # 这里放具体的操作
    while(1):
        response = await reader.read(1024)
        if(response):
            operation = "Im camera opener!"
            writer.write(operation.encode())
            await writer.drain()
        else:
            writer.close()
            return

async def open_microphone(GUI,writer,reader):
    # 这里放具体的操作
    while(1):
        response = await reader.read(1024)
        if(response):
            operation = "Im microphone opener!"
            writer.write(operation.encode())
            await writer.drain()
        else:
            writer.close()
            return

async def start_keylogger(GUI,writer,reader):
    # 这里放具体的操作
    while(1):
        response = await reader.read(1024)
        if(response):
            operation = "Im keylogger!"
            writer.write(operation.encode())
            await writer.drain()
        else:
            writer.close()
            return
