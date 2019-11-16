import requests
import re
import json
from util import download, check_input

r = requests.Session()


class DmzjMobile:
    """移动端网页
    :season: 要下载的漫画主页的网址 or 最后的目录"""

    def __init__(self, season: str):
        self.contents = {}
        season = check_input(season)
        self.get_season_content(season)
        # print(self.contents)

    def get_season_content(self, season):
        print(f"searching for {season}")
        url = f'https://m.dmzj.com/info/{season}.html'
        res = r.get(url)

        self.season_info = json.loads(re.findall(re.compile(r'initIntroData\((.*?)\)'), res.text)[0])[0]['data']
        self.season_name = re.findall(re.compile(r'<div class="BarTit" id="comicName">(.*)</div>'), res.text)[0]

        for e in self.season_info:
            title = e['chapter_name']
            self.contents[title] = {"chapter": title}
            self.contents[title]["links"] = self.get_img_links(e)

    def get_img_links(self, ep_info):
        url = f"https://m.dmzj.com/view/{ep_info['comic_id']}/{ep_info['id']}.html"
        res = r.get(url)
        pattern = re.compile(r'"page_url":(.*?),"chapter_type"')
        links_str = re.findall(pattern, res.text)[0]
        links = json.loads(links_str)
        return links

    def download(self):
        for e in self.contents.values():
            download(self.season_name, e['chapter'], e['links'])


if __name__ == "__main__":
    # 把网站赋值到这里
    url = 'https://manhua.dmzj.com/lydxcbdzm/'

    comic = DmzjMobile(url)
    comic.download()
