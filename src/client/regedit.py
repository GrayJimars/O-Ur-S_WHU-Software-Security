import socket
import json
import asyncio

async def send_registry_request(GUI,writer, reader,action,hive, key_path, key_name='', value=None):
    request = {
        'action': action,         #注册表操作类型，包括：add、delete、modify、find
        'hive': hive,             #注册表根键，包括：HKEY_CLASSES_ROOT、HKEY_CURRENT_USER、HKEY_LOCAL_MACHINE、HKEY_USERS、HKEY_CURRENT_CONFIG            
        'key_path': key_path,     #注册表路径：，需使用\\分隔目录
        'key_name': key_name,     #键名
        'value': value            #键值
    }
    
    request_data = json.dumps(request)
    

    # 发送请求数据到服务端
    writer.write(request_data.encode())
    await writer.drain() 

    # 接收服务端的响应
    response = await reader.read(1024)
    if response:
        response_message = response.decode('utf-8')
        GUI.append_log(f"[*] Response from server: {response_message}")

