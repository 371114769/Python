import requests
from js2py import EvalJs
import bs4
import json
import os

HOST_URL = "https://images.dmzj.com/"
r = requests.Session()
r.headers = {"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

class MComics:
    def __init__(self, collection: str):
        self.season_dict = {}

        self.get_season_content(collection)
        for path in self.season_dict.values():
            self.links = []
            self.episode_name = ""
            self.total_img = 0
            self.get_episode_links(path)
            self.download()

    def get_season_content(self, session):
        print('finding session...')
        res = r.get(f"https://manhua.dmzj.com/{session}/")

        bs = bs4.BeautifulSoup(res.text, features="lxml")
        link_tag = bs.find(attrs={'class': 'cartoon_online_border'})
        for i in link_tag.find_all('li'):
            title = i.a['title']
            path = i.a['href']
            self.season_dict[title] = path
        print(self.season_dict)

    def get_episode_links(self, path):
        print("requesting...")
        url = f"https://manhua.dmzj.com/{path}#@page=1"
        res = r.get(url)

        # 信息在JS里，需要用JS编译
        print("picking the soup...")
        soup = bs4.BeautifulSoup(res.text)
        head_script = soup.head.script.string
        print("executing js script...")
        js = EvalJs()
        js.execute(head_script)

        # 从编译JS的结果提取信息
        self.links = [HOST_URL + i for i in json.loads(js.pages)]
        self.season_name = self.season_name or f"{js.g_comic_name}"
        self.episode_name = f"{js.g_chapter_name}"
        self.total_img = int(js.g_max_pic_count)

    def download(self):
        # Check dir
        folder = f".{os.sep}{self.season_name}{os.sep}{self.episode_name}{os.sep}"
        if not os.path.exists(f".{os.sep}{self.season_name}"):
            os.mkdir(f".{os.sep}{self.season_name}")
        if not os.path.exists(folder):
            os.mkdir(folder)
        # 下载图片
        for index, link in enumerate(self.links):
            file_name = f"{str(index+1)}.{link.rsplit('.', 1)[1]}"
            res = r.get(link)
            with open(folder + file_name, 'wb') as fw:
                print(f"downloading {index+1}/{self.total_img}...")
                print(f"{self.season_name} {self.episode_name} {index+1}")
                print(link)
                fw.write(res.content)

if __name__ == "__main__":
    MComics('lydxcbdzm')
