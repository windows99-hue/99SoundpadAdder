from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from clc99 import *
import os
import sys
import requests
from tqdm import tqdm
import re
import keyboard
import configparser
import win32file
import pywintypes
import win32api
from urllib.parse import quote
import hashlib

initsystem()

print_good("欢迎使用99酷狗音乐下载+Soundpad导入神器!")
print_warning("本程序由Windows99-hue编写，禁止商用!")
print_uquestion("本程序会保存您或其他用户的个人登录信息(cookie)，本程序不会将您的个人信息放在除了您计算机以外的任何地方，请按照个人需求决定是否使用本程序。")

print_status("初始化程序。。。。")

self_path = os.path.abspath(__file__)
self_dir = os.path.dirname(__file__) + '/'
file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path) + '/'
media_pattern = re.compile(r'.*\.(m4a)$', re.IGNORECASE)
# 设置环境变量禁用所有 Chrome 内部日志
os.environ["GLOG_minloglevel"] = "3"  # FATAL 级别
os.environ["GOOGLE_STRIP_LOG"] = "1"  # 剥离所有日志

print_uquestion("请选择您想下载的音乐平台")
while True:
    cmd = input('''
    1)酷狗音乐
    2)网易云音乐
    3)退出程序
    
''')

    if cmd == "1":
        version = "kugou"
        break
    elif cmd == "2":
        version = "netcloud"
        break
    elif cmd == "3":
        print_warning("程序退出")
        os._exit(0)
    else:
        print_error("未知的指令，请重新输入")

    
def contains_korean(text):
    for char in text:
        if ('\u1100' <= char <= '\u11FF' or
            '\u3130' <= char <= '\u318F' or
            '\uAC00' <= char <= '\uD7AF'):
            return True
    return False

#####读取配置并初始化他们
config = configparser.ConfigParser()
config.read(self_dir+"configs.ini",encoding="utf-8")
SavePath = config.get("settings", "SavePath")
soundpad_path = config.get("settings", "SoundpadPath")
addsoundpad = config.getboolean("settings", "AddSoundpad")
cookies_path = config.get("settings", "CookiePath")

if contains_korean(SavePath):
    print_error("检测到保存路径包含韩国字符，请修改配置文件中的保存路径")
    sys.exit(1)

if not os.path.isabs(cookies_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookies_path = os.path.join(script_dir, cookies_path)

WAIT_TIME = 1
songinfo = None
target_url = config.get(version, "target_url")

options = {
    'disable_capture': False,
}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 禁用日志

driver = webdriver.Chrome(seleniumwire_options=options,options=chrome_options)


    
def check_add_status(response: str) -> bool:
    if response == "R-200":
        return True
    else:
        return False

def add_sound_to_soundpad(file_path: str) -> bool:
    if not os.path.exists(file_path):
        print_error(f"文件不存在: {file_path}")
        return False

    try:
        # 连接 Soundpad 的命名管道
        pipe_name = r'\\.\pipe\sp_remote_control'
        handle = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )

        #发送 DoAddSound 命令
        command = f'DoAddSound("{os.path.abspath(file_path)}")'

        win32file.WriteFile(handle, str.encode(command,encoding="GBK"))
        response = win32file.ReadFile(handle, 4096)[1].decode().strip('\x00')
        print_status(f"Soundpad 已响应")
        if check_add_status(response):
            print_good("音频文件添加成功")
            return True
        else:
            print_error(f"音频文件添加失败: {response}")
            return False
        

    except pywintypes.error as e:
        print_error(f"管道连接失败: {e}")
        return False
    finally:
        if 'handle' in locals():
            win32file.CloseHandle(handle)

def save_login_info():
    print_status("请在网页中按照正常流程登录您的平台账号，完成后按下回车",end="")
    input("")
    time.sleep(WAIT_TIME)
    print_status("正在保存你的登录信息到本地:")
    cookies = driver.get_cookies()
    cookie_str = json.dumps(cookies)
    with open(cookies_path, 'w') as f:
        f.write(cookie_str)
    print_good("保存成功!")
    

def get_login_info():
    with open(cookies_path, 'r') as f:
        cookie_str = f.read()
        cookies = json.loads(cookie_str)
    for c in cookies:
        driver.add_cookie(c)
    time.sleep(WAIT_TIME)
    driver.refresh()
    print_good("加载完成，请查看用户是否正确")

def clean_filename(filename):
    # 替换非法字符为下划线
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

def get_the_file(url):
    response = requests.get(url)
    data = json.loads(response.text)['data']
    PlayUrl = data['play_url']
    FileName = data['audio_name'] + ".mp3"
    FileName = clean_filename(FileName)
    download_the_file(PlayUrl,FileName , SavePath + "\\" + FileName)

def get_the_file_netcloud(url):
    #fuck...
    song_title = driver.title[2:]
    download_the_file(url, song_title + ".m4a", SavePath + "\\" + song_title + ".m4a")
    
def mp3_to_md5(file_path):
    """计算MP3文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def download_the_file(url,FileName, save_path):

    if contains_korean(save_path):
        print_warning("检测到文件名包含韩国字符，即将使用md5修复，请注意")
        md5_hash = mp3_to_md5(save_path)
        save_path = save_path.replace(FileName, md5_hash + ".mp3")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))

    with open(save_path, 'wb') as file, tqdm(
        desc=FileName,  # 进度条描述
        total=total_size,  # 总大小
        unit='B',  # 单位
        unit_scale=True,  # 自动缩放单位
        unit_divisor=1024,  # 单位除数
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            bar.update(len(chunk))  # 更新进度条

    save_path = save_path.replace("/", "\\")

    print_ok(f"文件已保存到: {save_path}")

    if addsoundpad:
        print_status("正在将文件添加到Soundpad...")
        add_sound_to_soundpad(save_path)

def be_start():
    # 关闭所有标签页

    for handle in reversed(driver.window_handles):
        if(len(driver.window_handles) == 1):
            break
        driver.switch_to.window(handle)
        driver.close()

    # 打开一个新标签页
    #driver.execute_script("window.open('about:blank')")

    # 切换到新标签页
    new_window_handle = driver.window_handles[0]
    driver.switch_to.window(new_window_handle)

    # 在新标签页中打开一个网页
    driver.get(target_url)

def on_esc_pressed():
    print_status("ESC被按下, 程序退出")
    print_status("正在关闭浏览器...")
    driver.quit()
    os._exit(0)

print_good("初始化完成！")
print_status("正在启动浏览器....")

try:
    driver.get(target_url)
    print_good("请不要关闭浏览器，完成后程序会自动将其关闭")
    time.sleep(WAIT_TIME)
    driver.refresh()
    time.sleep(WAIT_TIME)
    print_uquestion("请选择您需要的操作")
    while True:
        print('''
    1)登录账号
    2)下载歌曲
    3)退出程序
    ''')
        cmd = input("请输入指令:")
        if(cmd == '1'):
            save_login_info()
        elif (cmd == '2'):
            get_login_info()
            break
        elif (cmd == '3'):
            print_status("正在退出程序...")
            sys.exit()
        else:
            print("未知的指令，请重新输入")
    time.sleep(WAIT_TIME)

    while True:

        print_status("请在网页中搜索您想下载的歌曲并进入音乐播放页, 在音乐播放后按F8继续, 按ESC结束程序")
        keyboard.add_hotkey('esc', on_esc_pressed)
        keyboard.wait("f8")
        if version == "kugou":
            for request in driver.requests:
                if request.response:
                    if("songinfo" in request.url):
                        songinfo = request.url
            if songinfo == None:
                print_error("无法找到文件，请确认浏览器是否运行正常!")
            else:
                get_the_file(songinfo)
        elif version == "netcloud":
            recent_requests = list(driver.requests)[-20:] #切片防止炸内存
            
            m4a_requests = [
                req for req in driver.requests 
                if req.response and ".m4a?" in req.url
            ] #查找最新的m4a
            
            if not m4a_requests:
                print_error("无法找到文件，请确认浏览器是否运行正常!")
                continue
            
            latest_request = m4a_requests[-1]  # 获取最新的请求
            
            if songinfo == latest_request.url:
                print_status("same url, skipping...")
                continue
                
            print_good("找到歌曲文件")
            songinfo = latest_request.url
            get_the_file_netcloud(songinfo)

        be_start()
        
finally:
    print_status("正在关闭浏览器...")
    driver.quit()