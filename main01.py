from playwright.sync_api import sync_playwright
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
from urllib.parse import quote

initsystem()

print_good("欢迎使用99酷狗音乐下载+Soundpad导入神器!")
print_warning("本程序由Windows99-hue编写")
print_uquestion("本程序会保存您或其他用户的个人登录信息(cookie)，本程序不会将您的个人信息放在除了您计算机以外的任何地方，请按照个人需求决定是否使用本程序。")

print_status("初始化程序。。。。")

self_path = os.path.abspath(__file__)
self_dir = os.path.dirname(__file__) + '/'
file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path) + '/'
media_pattern = re.compile(r'.*\.(m4a)$', re.IGNORECASE)

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

# 读取配置
config = configparser.ConfigParser()
config.read(self_dir+"configs.ini", encoding="utf-8")
SavePath = config.get("settings", "SavePath")
soundpad_path = config.get("settings", "SoundpadPath")
addsoundpad = config.getboolean("settings", "AddSoundpad")

WAIT_TIME = 1
songinfo = None
target_url = config.get(version, "target_url")

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
        
        command = f'DoAddSound("{os.path.abspath(file_path)}")'
        print_status(command)
        win32file.WriteFile(handle, str.encode(command, encoding="GBK"))
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

def save_login_info(page):
    print_status("请在网页中按照正常流程登录您的平台账号，完成后按下回车", end="")
    input("")
    time.sleep(WAIT_TIME)
    print_status("正在保存你的登录信息到本地:")
    cookies = page.context.cookies()
    with open(file_dir+'cookies.json', 'w') as f:
        json.dump(cookies, f)
    print_good("保存成功!")

def load_login_info(page):
    if not os.path.exists(file_dir+'cookies.json'):
        print_error("未找到cookie文件，请先登录")
        return False
    
    with open(file_dir+'cookies.json', 'r') as f:
        cookies = json.load(f)
    
    page.context.add_cookies(cookies)
    page.reload()
    print_good("加载完成，请查看用户是否正确")
    return True

def clean_filename(filename):
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

def download_the_file(url, FileName, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))

    with open(save_path, 'wb') as file, tqdm(
        desc=FileName,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            bar.update(len(chunk))

    save_path = save_path.replace("/", "\\")
    print_ok(f"文件已保存到: {save_path}")

    if addsoundpad:
        print_status("正在将文件添加到Soundpad...")
        add_sound_to_soundpad(save_path)

def handle_kugou(page):
    # 存储监听器引用以便后续移除
    def on_response(response):
        global songinfo
        if "songinfo" in response.url:
            songinfo = response.url
    
    # 添加监听器并保存引用
    response_listener = lambda response: on_response(response)
    page.on("response", response_listener)
    
    print_status("请在网页中搜索您想下载的歌曲并进入音乐播放页, 在音乐播放后按F8继续, 按ESC结束程序")
    keyboard.wait("f8")
    
    # 移除监听器
    page.remove_listener("response", response_listener)
    
    if not songinfo:
        print_error("无法找到文件，请确认浏览器是否运行正常!")
        return
    
    get_the_file(songinfo)

def handle_netcloud(page):
    # 存储监听器引用以便后续移除
    def on_response(response):
        global songinfo
        if ".m4a?" in response.url:
            songinfo = response.url
    
    # 添加监听器并保存引用
    response_listener = lambda response: on_response(response)
    page.on("response", response_listener)
    
    print_status("请在网页中搜索您想下载的歌曲并进入音乐播放页, 在音乐播放后按F8继续, 按ESC结束程序")
    keyboard.wait("f8")
    
    # 移除监听器
    page.remove_listener("response", response_listener)
    
    if not songinfo:
        print_error("无法找到文件，请确认浏览器是否运行正常!")
        return
    
    song_title = page.title()[2:]
    print_status(song_title)
    download_the_file(songinfo, song_title + ".m4a", SavePath + "\\" + song_title + ".m4a")

def get_the_file(url):
    response = requests.get(url)
    data = json.loads(response.text)['data']
    PlayUrl = data['play_url']
    FileName = data['audio_name'] + ".mp3"
    FileName = clean_filename(FileName)
    download_the_file(PlayUrl, FileName, SavePath + "\\" + FileName)

def on_esc_pressed(page):
    print_status("ESC被按下, 程序退出")
    print_status("正在关闭浏览器...")
    page.close()
    os._exit(0)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print_good("初始化完成！")
        print_status("正在启动浏览器....")
        
        try:
            page.goto(target_url)
            print_good("请不要关闭浏览器，完成后程序会自动将其关闭")
            time.sleep(WAIT_TIME)
            page.reload()
            time.sleep(WAIT_TIME)
            
            print_uquestion("请选择您需要的操作")
            while True:
                print('''
            1)登录账号
            2)下载歌曲
            3)退出程序
            ''')
                cmd = input("请输入指令:")
                if cmd == '1':
                    save_login_info(page)
                elif cmd == '2':
                    if not load_login_info(page):
                        continue
                    break
                elif cmd == '3':
                    print_status("正在退出程序...")
                    sys.exit()
                else:
                    print("未知的指令，请重新输入")
            
            time.sleep(WAIT_TIME)
            
            while True:
                keyboard.add_hotkey('esc', lambda: on_esc_pressed(page))
                
                if version == "kugou":
                    handle_kugou(page)
                elif version == "netcloud":
                    handle_netcloud(page)
                
                # 重置页面
                page.close()
                page = context.new_page()
                page.goto(target_url)
                if load_login_info(page):
                    continue
        
        finally:
            print_status("正在关闭浏览器...")
            browser.close()

if __name__ == "__main__":
    main()