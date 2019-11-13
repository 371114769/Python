import requests
import urllib
import bs4
import codecs
try:
    import clipboard
    isIos = True
except:
    isIos = False

def purity(s: str):
    s = s.replace(';', '')
    s = s.replace('\n', '')
    return s


class Youdao():
    def __init__(self, key):
        self.key = key
        self.bs = ""
        self.ee = ""
        self.trans = []
        self.phrases = []
        self.typo = []

        # with codecs.open("./__tmp__/youdao.txt", "r", encoding="utf-8") as f:
        #     bs = bs4.BeautifulSoup(f.read(), features="html.parser")
        self.search()
        bs = bs4.BeautifulSoup(self.text, features="html.parser")
        self.web_trans(bs)
        self.ee_trans(bs)
        self.phrases_trans(bs)
        self.error_typo(bs)

    def search(self):
        url = f"http://www.youdao.com/w/{urllib.parse.quote(self.key)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
        print("[requesting..]")
        res = requests.get(url, headers=headers)
        self.text = res.text
        with codecs.open("./__tmp__/youdao.txt", "w+", encoding="utf-8") as f:
            f.write(self.text)

    def web_trans(self, bs):
        # 1.网络释义
        tags = bs.find(attrs={"id": "tWebTrans"})
        if not tags: return
        for t in [i for i in tags.children if isinstance(i, bs4.Tag)]:
            # 1.1.基本释义
            if 'wt-container' in t["class"]:
                trans = (t.div.span.getText()).strip()
                trans = purity(trans).replace('  ', '')
                sam = (t.p.getText()).strip()
                self.trans.append((trans, sam))
            # 1.2.短语释义
            elif 'webPhrase' in t["id"]:
                phrases = t.findAll(attrs={"class": "wordGroup"})
                for i in phrases:
                    phrase = i.span.getText()
                    phrase_trans = (i.getText()).replace(phrase, '')
                    phrase_trans = purity(phrase_trans).split()
                    self.phrases.append((phrase, phrase_trans))

    def ee_trans(self, bs):
        # 2.网络英英释义
        tags = bs.find(attrs={"id": "tEETrans"})
        if not tags: return
        try:
            self.ee = tags.div.ul.li.span.next_sibling.next_sibling.getText()
            self.ee = self.ee.replace('\t', '')
            self.ee = self.ee.replace('  ', '')
            self.ee = self.ee.replace('\n\n', '\n')
        except AttributeError:
            self.ee = tags.div.ul.li.span.getText()
            self.ee = self.ee.replace('\t', '')
            self.ee = self.ee.replace('  ', '')
            self.ee = self.ee.replace('\n\n', '\n')

    def phrases_trans(self, bs):
        # 3.词组短语
        tags = bs.find(attrs={"id": "eTransform"})
        if not tags: return
        wg = tags.find(attrs={"id": "wordGroup"})
        if not wg: return
        for p in [p for p in wg.contents if isinstance(p, bs4.Tag)]:
            phrase = p.span.getText()
            try:
                phrase_trans = purity(p.span.next_sibling).split()
                self.phrases.append((phrase, phrase_trans))
            # '更多'这个词条
            except TypeError:
                pass
    def error_typo(self, bs):
        tags = bs.findAll(attrs={"class": "typo-rel"})
        for i in tags:
            word = i.span.getText()
            trans = i.span.next_sibling.strip()
            self.typo.append((word, trans))

    def __str__(self):
        mlp = max([len(i[0]) for i in self.phrases] + [0])  # 最长短语的长度，排版用
        trans = ''.join([f"{t}:\n    {e}\n\n" for t, e in self.trans])
        phrases = ''.join([f"{i[0]:>{mlp}}: {' '.join(i[1])}\n" for i in self.phrases])
        typo = '\n'.join([f"{i[0]}: {i[1]}" for i in self.typo])
        f = f"\n\n{'='*42}".join([i for i in [self.ee, typo, trans, phrases] if i])
        return f"{self.key}\n{f}"


if __name__ == "__main__":
    if isIos:
        s = Youdao(clipboard.get())
        print(s)
    while True:
        key = input("[search:]")
        s = Youdao(key)
        print(s)
