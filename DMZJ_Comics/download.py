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
