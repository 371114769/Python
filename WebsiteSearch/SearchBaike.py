import requests
import codecs
import bs4
# import urllib


class Baike():
    def __init__(self, key):
        self.key = key
        self.related = []
        self.breif = ""
        self.link = ""
        self.baike()
        bs = bs4.BeautifulSoup(self.text, features="html.parser")
        self._related(bs)
        self._breif(bs)

    def baike(self):
        url = "https://baike.baidu.com/search/word"
        # cookie_quote = urllib.parse.quote('{"key":[' + self.key + ']}')
        # headers = {"Cookie": f"BK_SEARCHLOG={cookie_quote}"}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
        payload = {"word": self.key}
        res = requests.get(url, headers=headers, params=payload)
        self.link = res.url
        content = res.content
        self.text = content.decode('utf-8')
        with codecs.open("./__tmp__/baike.txt", "w+", encoding="utf-8") as fw:
            fw.write(self.text)
        return None if "no-result" in self.text else self.text

    def _related(self, bs):
        tags = bs.findAll(attrs={"class": "item"})
        for i in tags:
            title = i.getText()
            try:
                link = f'https://baike.baidu.com{i.a["href"]}'
            except TypeError:
                link = self.link
            self.related.append({"title": title, "link": link})

    def _breif(self, bs):
        tags = bs.find(attrs={"class": "lemma-summary"})
        if tags:
            self.breif = tags.getText()
            print(self.breif)
        else:
            print()

    def print_related(self):
        for i in self.related:
            print(i["title"], i["link"])


if __name__ == "__main__":
    key = input("[Search:]")
    s = Baike(key)
    s.print_related()
