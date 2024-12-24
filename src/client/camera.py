from PyQt5 import QtWidgets, QtGui
import cv2
import pickle
import struct
import time


async def receive_video_stream(GUI):
    """ 接收视频流并显示 """
    print("Waiting for video stream...")
    video_label = QtWidgets.QLabel()
    video_label.show()
    last_frame_time = 0

    while True:
        try:
            current_time = time.time()
            if current_time - last_frame_time * 1.0 < 0.033:  # 控制到约30帧/秒
                continue

            last_frame_time = current_time
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
                    raise Exception(
                        "[!] Data was truncated or connection was closed.")
                data += more_data

            frame = pickle.loads(data)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to QImage
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QtGui.QImage(frame.data, width, height,
                                 bytes_per_line, QtGui.QImage.Format_RGB888)
            # Display the QImage in the QLabel
            video_label.setPixmap(QtGui.QPixmap.fromImage(q_img))
            video_label.resize(width, height)

            if GUI.camera_check == False:
                operation = "stop"
                GUI.connections["openCamera"]["writer"].write(
                    operation.encode())
                await GUI.connections["openCamera"]["writer"].drain()
                break
            else:
                operation = "go on"
                GUI.connections["openCamera"]["writer"].write(
                    operation.encode())
                await GUI.connections["openCamera"]["writer"].drain()

        except Exception as e:
            GUI.append_log(f"[!] Error during receiving video stream: {e}")
