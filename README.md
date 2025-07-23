# 99音乐下载并添加到Soundpad神器

> 这什么稀奇名字
>
> 勤劳使人懒惰~

欢迎使用99音乐下载并添加到Soundpad神器！

本程序可以全自动化将音乐平台上的音乐下载并自动导入到soundpad中

## 安装

本程序使用**python3**编写，建议您使用`python3.9`及以上版本运行本程序

#### 1. 下载[python3](https://www.python.org/downloads/)

#### 2. 安装好[python3](https://www.python.org/downloads/)后，下载程序并安装本程序所需的库

~~~shell
pip install -r requirements.txt
~~~

#### 3. 下载并安装[Google Chrome](https://www.google.cn/intl/zh-CN_ALL/chrome/fallback/)/[Google Chrome官网版](https://www.google.com/intl/zh_cn/chrome/)

#### 4. 设置程序

请打开程序文件夹中的`configs.ini`，您应看到类似下方的构造

~~~ini
[settings]
SoundpadPath = D:\SteamLibrary\steamapps\common\Soundpad\Soundpad.exe
SavePath = D:\Temp
AddSoundPad = True

[kugou]
target_url = https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord=

[netcloud]
target_url = https://music.163.com
~~~

请将`[Settings]`部分的`SoundpadPath`设置为您Soundpad所在的路径（包含Soundpad.exe），若您使用steam安装的soundpad，可以遵循如下步骤

1. 在steam库中打开soundpad页面并点击齿轮图标

   ![1](https://raw.githubusercontent.com/windows99-hue/99SoundpadAdder/refs/heads/main/images/document/ca3376ff8e0d74d7b81acbb73affcfd9.png)

2. 将鼠标悬停在`管理`选项卡中，点击`浏览本地文件`

![2](https://raw.githubusercontent.com/windows99-hue/99SoundpadAdder/refs/heads/main/images/document/75a1ba4413af1daf54eaafea15acae31.png)

3. 复制`Soundpad.exe`的文件绝对路径即可

请将`SavePath`设置为您想**将音乐文件存储的路径**

`AddSoundPad`是一个布尔开关，当值为`True`时，程序会在下载完音频后自动导入soundpad，如果为`False`，那么程序会在下载完音频后自动准备下一轮下载

`target_url`为默认设置

## 使用

**打开终端**，执行

~~~shell
python main01.py
~~~

这将启动程序，请跟随程序选择您想使用的音乐平台

**第一次启动时**，请选择`登录账号`选项，跟随程序登录好后再开始下载

其余启动时，直接选择`下载歌曲`选项

## 写在后面

本程序使用`GNU General Public License v2.0`许可证，如果您对程序有建议或者bug反馈，欢迎fork我的仓库或向我提出`Issue`

玩的开心=)
