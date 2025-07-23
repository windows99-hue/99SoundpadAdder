# 99 Music Downloader & Soundpad Importer Tool

> What a peculiar name
>
> Hard work makes people lazy~

Welcome to the 99 Music Downloader & Soundpad Importer Tool!

This program can automatically download music from music platforms and import it into Soundpad.

## Installation

This program is written in **Python 3**. We recommend using `Python 3.9` or higher to run this program.

#### 1. Download [Python 3](https://www.python.org/downloads/)

#### 2. After installing [Python 3](https://www.python.org/downloads/), download the program and install the required libraries

shell

```
pip install -r requirements.txt
```

#### 3. Download and install [Google Chrome](https://www.google.cn/intl/zh-CN_ALL/chrome/fallback/)/[Official Google Chrome](https://www.google.com/intl/zh_cn/chrome/)

#### 4. Configure the program

Please open `configs.ini` in the program folder. You should see a structure similar to the following:

ini

```
[settings]
SoundpadPath = D:\SteamLibrary\steamapps\common\Soundpad\Soundpad.exe
SavePath = D:\Temp
AddSoundPad = True

[kugou]
target_url = https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord=

[netcloud]
target_url = https://music.163.com
```

Please set `SoundpadPath` under the `[Settings]` section to the path where Soundpad is located (including Soundpad.exe). If you installed Soundpad via Steam, you can follow these steps:

1. Open the Soundpad page in your Steam library and click the gear icon.

   https://raw.githubusercontent.com/windows99-hue/99SoundpadAdder/refs/heads/main/images/document/ca3376ff8e0d74d7b81acbb73affcfd9.png

2. Hover over the `Manage` tab and click `Browse local files`.

https://raw.githubusercontent.com/windows99-hue/99SoundpadAdder/refs/heads/main/images/document/75a1ba4413af1daf54eaafea15acae31.png

1. Copy the absolute file path of `Soundpad.exe`.

Set `SavePath` to the path where you want to **store the music files**.

`AddSoundPad` is a boolean switch. When set to `True`, the program will automatically import downloaded audio into Soundpad. If set to `False`, the program will prepare for the next download after completing the current one.

`target_url` is the default setting.

## Usage

**Open a terminal** and execute:

shell

```
python main01.py
```

This will start the program. Follow the prompts to select your preferred music platform.

**On first launch**, choose the `Log in to account` option and follow the instructions to log in before starting downloads.

On subsequent launches, simply select the `Download songs` option.

**Ensure that Soundpad is turned on during use!**

## Final Notes

This program uses the `GNU General Public License v2.0`license. If you have suggestions or bug reports, feel free to fork my repository or submit an `Issue`.

refer to:[Mass1milian0/soundpad-python-youtube-adder](https://github.com/Mass1milian0/soundpad-python-youtube-adder)

Have fun! =)