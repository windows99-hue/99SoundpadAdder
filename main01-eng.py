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

print_good("Welcome to the 99 Kugou Music Downloader + Soundpad Importer Tool!")  
print_warning("This program is written by Windows99-hue and is prohibited for commercial use!")  
print_uquestion("This program will save your or other users' personal login information (cookies). The program will not store your personal information anywhere other than your computer. Please decide whether to use this program based on your personal needs.")  

print_status("Initializing the program....")  

self_path = os.path.abspath(__file__)  
self_dir = os.path.dirname(__file__) + '/'  
file_path = os.path.abspath(__file__)  
file_dir = os.path.dirname(file_path) + '/'  
media_pattern = re.compile(r'.*\.(m4a)$', re.IGNORECASE)  
# Set environment variables to disable all Chrome internal logs  
os.environ["GLOG_minloglevel"] = "3"  # FATAL level  
os.environ["GOOGLE_STRIP_LOG"] = "1"  # Strip all logs  

print_uquestion("Please select the music platform you want to download from")  
while True:  
    cmd = input('''  
    1) Kugou Music  
    2) NetEase Cloud Music  
    3) Exit the program  

''')  

    if cmd == "1":  
        version = "kugou"  
        break  
    elif cmd == "2":  
        version = "netcloud"  
        break  
    elif cmd == "3":  
        print_warning("Exiting the program")  
        os._exit(0)  
    else:  
        print_error("Unknown command, please re-enter")  

def contains_korean(text):
    for char in text:
        if ('\u1100' <= char <= '\u11FF' or
            '\u3130' <= char <= '\u318F' or
            '\uAC00' <= char <= '\uD7AF'):
            return True
    return False

##### Read the configuration and initialize them  
config = configparser.ConfigParser()  
config.read(self_dir + "configs.ini", encoding="utf-8")  
SavePath = config.get("settings", "SavePath")  
soundpad_path = config.get("settings", "SoundpadPath")  
addsoundpad = config.getboolean("settings", "AddSoundpad")  
cookies_path = config.get("settings", "CookiePath")  

if not os.path.isabs(cookies_path):  
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    cookies_path = os.path.join(script_dir, cookies_path)  

if contains_korean(SavePath):
    print_error("Detected that the save path contains Korean characters, please modify the save path in the configuration file.")
    sys.exit(1)

WAIT_TIME = 1  
songinfo = None  
target_url = config.get(version, "target_url")  

options = {  
    'disable_capture': False,  
}  

chrome_options = webdriver.ChromeOptions()  
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Disable logging  

driver = webdriver.Chrome(seleniumwire_options=options, options=chrome_options)  

def check_add_status(response: str) -> bool:  
    if response == "R-200":  
        return True  
    else:  
        return False  

def add_sound_to_soundpad(file_path: str) -> bool:  
    if not os.path.exists(file_path):  
        print_error(f"File does not exist: {file_path}")  
        return False  

    try:  
        # Connect to Soundpad's named pipe  
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

        # Send the DoAddSound command  
        command = f'DoAddSound("{os.path.abspath(file_path)}")'  
        print_status(command)  
        win32file.WriteFile(handle, str.encode(command, encoding="GBK"))  
        response = win32file.ReadFile(handle, 4096)[1].decode().strip('\x00')  
        print_status(f"Soundpad has responded")  
        if check_add_status(response):  
            print_good("Audio file added successfully")  
            return True  
        else:  
            print_error(f"Failed to add audio file: {response}")  
            return False  

    except pywintypes.error as e:  
        print_error(f"Failed to connect to the pipe: {e}")  
        return False  
    finally:  
        if 'handle' in locals():  
            win32file.CloseHandle(handle)  

def save_login_info():  
    print_status("Please log in to your platform account on the webpage as usual, then press Enter", end="")  
    input("")  
    time.sleep(WAIT_TIME)  
    print_status("Saving your login information locally:")  
    cookies = driver.get_cookies()  
    cookie_str = json.dumps(cookies)  
    with open(cookies_path, 'w') as f:  
        f.write(cookie_str)  
    print_good("Saved successfully!")  

def get_login_info():  
    with open(cookies_path, 'r') as f:  
        cookie_str = f.read()  
        cookies = json.loads(cookie_str)  
    for c in cookies:  
        driver.add_cookie(c)  
    time.sleep(WAIT_TIME)  
    driver.refresh()  
    print_good("Loading complete, please verify if the user is correct")  

def clean_filename(filename):  
    # Replace illegal characters with underscores  
    return re.sub(r'[\\/:*?"<>|]', '_', filename)  

def mp3_to_md5(file_path):
    """计算MP3文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_the_file(url):  
    response = requests.get(url)  
    data = json.loads(response.text)['data']  
    PlayUrl = data['play_url']  
    FileName = data['audio_name'] + ".mp3"  
    FileName = clean_filename(FileName)  
    print(file_dir + FileName)  
    download_the_file(PlayUrl, FileName, SavePath + "\\" + FileName)  

def get_the_file_netcloud(url):  
    # Damn...  
    song_title = driver.title[2:]  
    print_status(song_title)  

    download_the_file(url, song_title + ".m4a", SavePath + "\\" + song_title + ".m4a")  

def download_the_file(url, FileName, save_path):  

    if contains_korean(save_path):
        print_warning("检测到文件名包含韩国字符，即将使用md5修复，请注意")
        md5_hash = mp3_to_md5(save_path)
        save_path = save_path.replace(FileName, md5_hash + ".mp3")

    response = requests.get(url, stream=True)  
    response.raise_for_status()  

    total_size = int(response.headers.get('content-length', 0))  

    with open(save_path, 'wb') as file, tqdm(  
        desc=FileName,  # Progress bar description  
        total=total_size,  # Total size  
        unit='B',  # Unit  
        unit_scale=True,  # Auto-scale unit  
        unit_divisor=1024,  # Unit divisor  
    ) as bar:  
        for chunk in response.iter_content(chunk_size=8192):  
            file.write(chunk)  
            bar.update(len(chunk))  # Update progress bar  

    save_path = save_path.replace("/", "\\")  

    print_ok(f"File saved to: {save_path}")  

    if addsoundpad:  
        print_status("Adding the file to Soundpad...")  
        add_sound_to_soundpad(save_path)  

def be_start():  
    # Close all tabs  

    for handle in reversed(driver.window_handles):  
        if (len(driver.window_handles) == 1):  
            break  
        driver.switch_to.window(handle)  
        driver.close()  

    # Open a new tab  
    # driver.execute_script("window.open('about:blank')")  

    # Switch to the new tab  
    new_window_handle = driver.window_handles[0]  
    driver.switch_to.window(new_window_handle)  

    # Open a webpage in the new tab  
    driver.get(target_url)  

def on_esc_pressed():  
    print_status("ESC pressed, exiting the program")  
    print_status("Closing the browser...")  
    driver.quit()  
    os._exit(0)  

print_good("Initialization complete!")  
print_status("Starting the browser....")  

try:  
    driver.get(target_url)  
    print_good("Please do not close the browser. The program will close it automatically when finished.")  
    time.sleep(WAIT_TIME)  
    driver.refresh()  
    time.sleep(WAIT_TIME)  
    print_uquestion("Please select the operation you need")  
    while True:  
        print('''  
    1) Log in to account  
    2) Download songs  
    3) Exit the program  
    ''')  
        cmd = input("Please enter the command:")  
        if (cmd == '1'):  
            save_login_info()  
        elif (cmd == '2'):  
            get_login_info()  
            break  
        elif (cmd == '3'):  
            print_status("Exiting the program...")  
            sys.exit()  
        else:  
            print("Unknown command, please re-enter")  
    time.sleep(WAIT_TIME)  

    while True:  

        print_status("Please search for the song you want to download on the webpage and enter the music playback page. After the music starts playing, press F8 to continue or ESC to exit the program.")  
        keyboard.add_hotkey('esc', on_esc_pressed)  
        keyboard.wait("f8")  
        if version == "kugou":  
            for request in driver.requests:  
                if request.response:  
                    if ("songinfo" in request.url):  
                        songinfo = request.url  
            if songinfo == None:  
                print_error("Unable to find the file. Please confirm if the browser is functioning properly!")  
            else:  
                get_the_file(songinfo)  
        elif version == "netcloud":  
            recent_requests = list(driver.requests)[-20:]  # Slice to prevent memory overload  

            m4a_requests = [  
                req for req in driver.requests  
                if req.response and ".m4a?" in req.url  
            ]  # Find the latest .m4a  

            if not m4a_requests:  
                print_error("Unable to find the file. Please confirm if the browser is functioning properly!")  
                continue  

            latest_request = m4a_requests[-1]  # Get the latest request  

            if songinfo == latest_request.url:  
                print_status("Same URL, skipping...")  
                continue  

            print_good("Found the song file")  
            songinfo = latest_request.url  
            get_the_file_netcloud(songinfo)  

        be_start()  

finally:  
    print_status("Closing the browser...")  
    driver.quit()  