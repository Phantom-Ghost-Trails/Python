import os
import time
import random
import string
from colorama import Fore, Style, init

# 初始化colorama
init(autoreset=True)

def generate_random_string(length=10):
    """生成指定长度的随机字符串"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def get_random_color():
    """随机选择一个颜色"""
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

def random_delete_part_of_path(path):
    """随机删除路径的一部分"""
    parts = path.split('/')
    if len(parts) > 2:  # 至少保留首尾两部分
        start = random.randint(1, len(parts) - 2)
        end = random.randint(start, len(parts) - 2)
        del parts[start:end+1]
    return '/'.join(parts)

def print_random_colored_text(text):
    """以随机颜色输出每个字符，并在随机间隔后添加空格"""
    colored_text = ""
    interval = random.randint(1, 5)  # 随机间隔，范围为1到5
    count = 0  # 计数器，用于跟踪当前字符位置

    for char in text:
        random_color = get_random_color()
        colored_text += random_color + char
        count += 1
        if count == interval and char != text[-1]:
            colored_text += " "
            interval = random.randint(1, 5)  # 重新生成随机间隔
            count = 0  # 重置计数器

    print(colored_text)

def scan_files(directory, display_probability=0.5):
    # 检查指定的路径是否存在
    if not os.path.exists(directory):
        print(Fore.RED + f"指定的目录 {directory} 不存在")
        return
    
    # 打印开始扫描的消息
    print_random_colored_text("MatrixScanner 开始扫描文件系统...")
    time.sleep(1)  # 模拟启动延迟

    # 遍历指定目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if random.random() < display_probability:  # 根据概率决定是否显示
                file_path = os.path.join(root, file)
                random_code = generate_random_string(10)  # 生成10个字符的乱码
                masked_path = random_delete_part_of_path(file_path)
                a = random.randint(1,6)
                if a == 1:
                    print_random_colored_text(f"MatrixScanner 现文件: {masked_path} [{random_code} ：{random_code}]")
                    time.sleep(random.random())  # 模拟文件加载时间
                elif a == 2:
                    print_random_colored_text(f"MatrixScanner 发文件: {masked_path} [{random_code} ：{random_code}]")
                    time.sleep(random.random())  # 模拟文件加载时间
                elif a == 3:
                    print_random_colored_text(f"MatrixScanner 发件: {masked_path} [{random_code} ：{random_code}]")
                    time.sleep(random.random())  # 模拟文件加载时间
                elif a == 4:
                    print_random_colored_text(f"MatrixScanner 发文: {masked_path} [{random_code} ：{random_code}]")
                    time.sleep(random.random())  # 模拟文件加载时间
                elif a == 5:
                    print_random_colored_text(f"MatrixScanner 现件: {masked_path} [{random_code} ：{random_code}]")
                    time.sleep(random.random())  # 模拟文件加载时间
                else:
                    print_random_colored_text(f"MatrixScanner 文: {masked_path} [{random_code} ：{random_code}]")
                    time.sleep(random.random())  # 模拟文件加载时间


    print_random_colored_text("MatrixScanner 扫描完成！")

# 指定要扫描的目录
directory_to_scan = input("请输入要扫描的目录路径: ")
scan_files(directory_to_scan, display_probability=0.5)