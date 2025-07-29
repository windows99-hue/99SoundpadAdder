# 99 Music Downloader and Soundpad Importer Tool

> What a peculiar name
>
> Hard work makes people lazy~

Welcome to the 99 Music Downloader and Soundpad Importer Tool!

This program can fully automate the process of downloading music from music platforms and automatically importing it into Soundpad.

## Installation

This program is written in **Python 3**. It is recommended to use `Python 3.9` or higher to run this program.

#### 1. Download [Python 3](https://www.python.org/downloads/)

#### 2. After installing [Python 3](https://www.python.org/downloads/), download the program and install the required libraries.

```shell
pip install -r requirements.txt
```

#### 3. Download and install [Google Chrome](https://www.google.cn/intl/zh-CN_ALL/chrome/fallback/)/[Official Google Chrome](https://www.google.com/intl/zh_cn/chrome/)

#### 4. Configure the Program

Open the `configs.ini` file in the program folder. You should see a structure similar to the following:

```ini
[settings]
SoundpadPath = D:\SteamLibrary\steamapps\common\Soundpad\Soundpad.exe
SavePath = D:\Temp
AddSoundPad = True
CookiePath = D:\99SoundPadAdder\cookies.json

[kugou]
target_url = https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord=

[netcloud]
target_url = https://music.163.com
```

Set the `SoundpadPath` under the `[Settings]` section to the path where Soundpad is located (including `Soundpad.exe`). If you installed Soundpad via Steam, follow these steps:

1. Open the Soundpad page in your Steam library and click the gear icon.

   https://raw.githubusercontent.com/windows99-hue/99SoundpadAdder/refs/heads/main/images/document/ca3376ff8e0d74d7b81acbb73affcfd9.png

2. Hover over the `Manage` tab and click `Browse local files`.

https://raw.githubusercontent.com/windows99-hue/99SoundpadAdder/refs/heads/main/images/document/75a1ba4413af1daf54eaafea15acae31.png

1. Copy the absolute path of the `Soundpad.exe` file.

Set `SavePath` to the path where you want **the music files to be stored. Don't have Korean charactors**.

`AddSoundPad` is a boolean switch. When set to `True`, the program will automatically import downloaded audio into Soundpad. If set to `False`, the program will prepare for the next download after completing the current one.

`CookiePath` is where the program stores your login information.

**Please use absolute paths for all settings.**

`target_url` is the default setting.

## Usage

**Open the terminal** and execute:

```shell
python main01.py
```

This will start the program. Follow the prompts to select the music platform you want to use.

**For the first run**, choose the `Log in to account` option and follow the instructions to log in before starting downloads.

For subsequent runs, directly select the `Download songs` option.

**While using the program, ensure Soundpad is running!**

## Final Notes

This program is licensed under the `GNU General Public License v2.0`. If you have suggestions or bug reports, feel free to fork my repository or submit an `Issue`.

Reference: [Mass1milian0/soundpad-python-youtube-adder](https://github.com/Mass1milian0/soundpad-python-youtube-adder)

Have fun! =)