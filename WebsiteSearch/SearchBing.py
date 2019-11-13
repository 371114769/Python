import requests
import urllib
import bs4
import codecs

try:
    import console
    on_phone = True
except ModuleNotFoundError:
    on_phone = False


r = requests.Session()


class Bing():
    def __init__(self, key):
        self.key = key
        self.result_count = 0
        self.results = []
        self.url = "https://cn.bing.com/search"
        self.cvid = "003674F74281416D835441F945419D2D"
        self.search()
        self.search()
        self.get_result()

    def search(self):
        payload = {
            "q": self.key,
            "qs": "n",
            "form": "QBRE",
            "sp": "-1",
            "pq": self.key,
            "sc": "10-10",
            "sk": "",
            "cvid": self.cvid}
        # encoded_payload = urllib.parse.urlencode(payload)
        # headers = {"path": f"/search?q={encoded_payload}",
        #            "referer": f"https://cn.bing.com/search?q={encoded_payload}"}
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
        res = r.get(self.url, headers=headers, params=payload)
        print(res)
        self.restext = res.text
        with codecs.open("./__tmp__/bing.txt", "w+", encoding="utf-8") as fw:
            fw.write(self.restext)

    def get_result(self):
        bs = bs4.BeautifulSoup(self.restext, features="html.parser")
        # 本次搜索有多少条结果
        result_count = bs.find(attrs={"class": "sb_count"})
        self.result_count = result_count.getText()
        # 本页的结果
        result = bs.findAll(attrs={"class": "b_algo"})
        for i in result:
            title = not i.h2 or i.h2.getText()
            caption = not i.p or i.p.getText()
            link = not i.a or i.a["href"]
            self.results.append({"title": title, "caption": caption, "link": link})

    def print_result(self):
        print(self.result_count, end="\n\n")
        if not on_phone:
            for i in self.results:
                print(f"{i['title']}\n{i['caption']}\n{i['link']}\n\n")
        else:
            for i in self.results:
                console.set_color(.0, .81, .23)
                print(i['title'])
                console.set_color(0, 0, 0)
                print(i['caption'])
                print(i['link'])
                print('\n')


if __name__ == "__main__":
    key = input("[Search:]")
    search = Bing(key)
    search.print_result()
