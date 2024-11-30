import asyncio
import cv2
import pickle
import struct
import logging

async def receive_video_stream(GUI):
    """ 接收视频流并显示 """
    print("Waiting for video stream...")
    while True:
        try:
            # 读取图像数据大小（一个32位的无符号长整型）
            size_data = await GUI.connections["openCamera"]["reader"].read(struct.calcsize('L'))
            if not size_data:
                GUI.append_log("[!] No data received. Connection closed.")
                break

            size = struct.unpack('L', size_data)[0]
            data = b''  # 用于存储完整的图像数据
            while len(data) < size:
                more_data = await GUI.connections["openCamera"]["reader"].read(size - len(data))
                if not more_data:
                    raise Exception("[!] Data was truncated or connection was closed.")
                data += more_data

            frame = pickle.loads(data)

            cv2.imshow('Camera Stream', frame)

            if GUI.camera_check == False:
                operation = "stop"
                GUI.connections["openCamera"]["writer"].write(operation.encode())
                await GUI.connections["openCamera"]["writer"].drain()
                break
            else:
                operation = "go on"
                GUI.connections["openCamera"]["writer"].write(operation.encode())
                await GUI.connections["openCamera"]["writer"].drain()

        except Exception as e:
            GUI.append_log(f"[!] Error during receiving video stream: {e}")
            cv2.destroyAllWindows()

    cv2.destroyAllWindows()  # 关闭 OpenCV 窗口


