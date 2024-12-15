import qrcode

# 创建一个二维码对象
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# 添加要编码的数据到二维码
data = input("请输入要编码的数据: ")
qr.add_data(data)

# 生成二维码                        
qr.make(fit=True)

# 从二维码生成图像                        
img = qr.make_image(fill_color="black", back_color="white")

# 保存二维码为图像文件
filename = input("请输入二维码图像的文件名: ")
img.save(filename + ".png")