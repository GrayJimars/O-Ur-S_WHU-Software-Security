import socket
import winreg
import json

def handle_registry_request(data):
    try:

        request = json.loads(data)
        action = request['action']
        hive = request['hive']
        key_path = request['key_path']
        key_name = request.get('key_name', '')
        value = request.get('value', None)
        
        #将注册表根键转换为可以被OpenKey函数接受的参数形式
        hive = getattr(winreg, hive.upper(), None)
        
        if not hive:
            return "Invalid registry hive"
           
        if action == 'add':
            # 添加注册表键值
            try:
                # 打开当前路径
                key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                # 当前路径不存在,创建该路径
                key = winreg.CreateKey(hive, key_path)
            
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(key)  
            return "Key added successfully."
        

        elif action == 'delete':
            # 删除注册表键值
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_ALL_ACCESS)  
            winreg.DeleteValue(key, key_name)
            return "Key deleted successfully."
        
        elif action == 'modify':
            # 修改注册表键值
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_ALL_ACCESS)  
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, value)
            return "Key modified successfully."
        
        elif action == 'find':
            # 查找注册表键值
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)  
            try:
                value, regtype = winreg.QueryValueEx(key, key_name)
                
                return f"Found value: {value}"
            except FileNotFoundError:
                return "Key not found"
        else:
            return "Unknown action"
        
    except Exception as e:
        return f"Error processing request: {e}"

