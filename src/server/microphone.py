import asyncio
import pyaudio
import logging


# 发送音频流的函数
# 发送音频流的函数
async def start_voice_stream(writer, reader):
    """ 发送麦克风音频流到指定的writer """
    print("Starting voice stream...")

    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()

    # 打开麦克风输入流
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=8192)

    try:
        # 循环读取麦克风输入并发送数据
        while True:
            try:
                # 读取音频数据
                data = stream.read(2048, exception_on_overflow=False)
                # print(f"Length of data: {len(data)}")  # 打印字符串长度
                # 发送音频数据到连接
                writer.write(data)
                await writer.drain()  # 确保数据被传输

                microphone_stop = await reader.read(1024)
                microphone_stop = microphone_stop.decode()  # 解码成字符串
                print(f"Length of data2: {len(data)}")  # 打印字符串长度

                if microphone_stop == "stop":
                    print("Stopping voice stream...")
                    break
            except asyncio.CancelledError:
                # 当任务被取消时，正常退出循环
                print("[*] Voice stream transmission was cancelled.")
                break

            except Exception as e:
                # 捕获其他异常并打印
                print(f"[!] Error during audio stream transmission: {e}")
                break

    except Exception as e:
        print(f"[!] Error initializing the audio stream: {e}")

    finally:
        # 关闭麦克风输入流和 PyAudio
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        p.terminate()
        print("[*] Audio stream stopped and resources released.")
