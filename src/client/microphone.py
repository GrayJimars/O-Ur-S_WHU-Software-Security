import asyncio
import pyaudio
import struct
import logging


async def receive_voice_stream(GUI):
    """ 接收音频流并播放 """
    print("Waiting for voice stream...")
    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()
    # 打开音频输出流
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True,
                    frames_per_buffer=8192)
    while True:
        try:
            # 读取 1024 字节数据
            data = await asyncio.wait_for(
                GUI.connections["openMicrophone"]["reader"].read(4096),
                timeout=5  # 设置超时时间（5秒）
            )
            if not data:
                print("[*] No data received, stream closed.")
                break  # 如果没有数据，退出循环
            # 播放音频数据
            stream.write(data)
            print(f"Length of data: {len(data)}")  # 打印字符串长度
            if GUI.microphone_check == False:
                microphone_stop = "stop"
                GUI.connections["openMicrophone"]["writer"].write(
                    microphone_stop.encode())
                await GUI.connections["openMicrophone"]["writer"].drain()
                break

            else:
                microphone_stop = "go on--"
                GUI.connections["openMicrophone"]["writer"].write(
                    microphone_stop.encode())
                await GUI.connections["openMicrophone"]["writer"].drain()

        except Exception as e:
            # 捕获其他异常
            print(f"[!] Error while receiving audio stream: {e}")
            break

        # 关闭音频流和 PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("[*] Audio stream stopped and resources released.")
