import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar  # pip install pyzbar

# 询问用户输入二维码图像的路径
image_path = input("请输入二维码图像的路径（例如：qrcode.png）：")

# 读取图像
frame = cv2.imread(image_path)

if frame is None:
    print("无法加载图像，请检查路径是否正确。")
else:
    decoded_objects = pyzbar.decode(frame)  # 解码二维码
    results = []

    for obj in decoded_objects:
        data = obj.data.decode('utf-8')  # 获取解码的数据
        results.append(data)  # 将结果添加到列表中
        print("Data:", data)

    if results:
        print("扫描结果如下：")
        for item in results:
            print(item)
    else:
        print("未检测到二维码。")
