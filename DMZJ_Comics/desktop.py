import requests
from js2py import EvalJs
from download import download
import bs4
import json
import re

HOST = "https://images.dmzj.com/"
r = requests.Session()
r.headers = {"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}


class Dmzj:
    def __init__(self, season: str):
        self.contents = []
        self.get_season_content(season)

    def get_season_content(self, season):
        print('finding season...')
        res = r.get(f"https://manhua.dmzj.com/{season}/")
        episods = re.findall(re.compile(r'<a title=".*" href="(.*html)"'), res.text)
        for i in episods:
            print(i)
            toappend = {"path": i}
            self.get_episode_links(toappend)
            self.contents.append(toappend)
        print(self.contents)

    def get_episode_links(self, item):
        url = f"https://manhua.dmzj.com/{item['path']}#@page=1"
        res = r.get(url)

        # 信息在JS里，需要用JS编译
        soup = bs4.BeautifulSoup(res.text, features="lxml")
        head_script = soup.head.script.string
        js = EvalJs()
        js.execute(head_script)

        # 从编译JS的结果提取信息
        item["links"] = [HOST + i for i in json.loads(js.pages)]
        item["sname"] = f"{js.g_comic_name}"
        item["chapter"] = f"{js.g_chapter_name}"

    def download(self):
        for e in self.contents:
            download(e['sname'], e['chapter'], e['links'])

if __name__ == "__main__":
    d = Dmzj('lydxcbdzm')
    d.download()
