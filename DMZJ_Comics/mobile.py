import requests
import re
import json
import bs4
import os

r = requests.Session()

class MComics:
    
    def __init__(self, collection):
        url_session = f'https://m.dmzj.com/info/{collection}.html'
        res = r.get(url_session)

        # 获得分集信息
        self.episodes = json.loads(re.findall(re.compile(r'initIntroData\((.*?)\)'), res.text)[0])[0]['data']
        self.comic_id = self.episodes[0]['comic_id']

        for e in self.episodes:
            print(e)
            self.get_episode(e['id'])

    def get_episode(self, id):
        url_episode = f'https://m.dmzj.com/view/{self.comic_id}/{id}.html'
        res = r.get(url_episode)
        soup = bs4.BeautifulSoup(res.text)
        scripts = soup.findAll(attrs={"type": "text/javascript"})[11]
        print(scripts)
        links = re.findall(re.compile(r'"page_url":(.*?),"chapter_type"'), str(scripts))[0]
        print(json.loads(links))

    def download(self):
        pass


# mc = MComics('chengfazhe12')

