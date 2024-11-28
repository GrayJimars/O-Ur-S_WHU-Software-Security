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