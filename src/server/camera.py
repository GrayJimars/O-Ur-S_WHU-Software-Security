import asyncio
import cv2
import pickle
import struct
import logging

# 发送视频流的函数
async def start_video_stream(writer,reader):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 强制使用 DirectShow 后端
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                raise Exception("Failed to read frame")

            # 序列化图像数据
            data = pickle.dumps(frame)
            size = struct.pack('L', len(data))  # 获取图像数据大小

            # 发送图像数据大小
            writer.write(size)
            await writer.drain()

            # 发送序列化的图像数据
            writer.write(data)
            await writer.drain()

            #print(f"Sent frame of size: {len(data)}")


            response = await reader.read(1024)
            response = response.decode()  # 解码成字符串
            print(response)
            # 如果按下 'q' 键，退出视频流传输
            if response == "stop":
                print("cxp")
                break
    except Exception as e:
        logging.error(f"[!] Error during video stream: {e}")
    finally:
        cap.release()
