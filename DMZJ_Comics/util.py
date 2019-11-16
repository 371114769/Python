import os
import requests


def download(season, episode, links):
    pics = len(links)
    # Check dir
    folder = f"./{season}/{episode}/"
    if not os.path.exists(f"./{season}"):
        os.mkdir(f"./{season}")
    if not os.path.exists(folder):
        os.mkdir(folder)
    # 下载图片
    for index, link in enumerate(links):
        print(f"downloading {index+1:>2}/{pics}...")
        print(f"{season} {episode} {index+1}")
        print(link)
        file_name = f"{str(index+1)}.{link.rsplit('.', 1)[1]}"
        res = requests.get(link)
        with open(folder + file_name, 'wb') as fw:
            fw.write(res.content)


def check_input(string):
    if "https" in string or "dmzj" in string:
        if "info/" in string and not string.rsplit("info/")[1]:
            print("sorry, I don't reconize this url")
            return
        elif "com/" in string and not string.rsplit("com/")[1]:
            print("sorry, I don't reconize this url")
            return
        season = string.rsplit("/", 1)[1] or string.rsplit("/", 2)[1]
        season = season.split(".")[0]  # 移动端网页还有.html的后缀
        return season
    elif string.isalpha():
        return string
    else:
        string.replace("/", "")
        return string
