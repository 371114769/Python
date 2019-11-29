import codecs
import json

with codecs.open('chinese_words.pinyin.txt', 'r', encoding="utf-8") as fr:
    wlist = fr.read().split()
wlist = [w for w in wlist if 6 <= len(w) <= 10]
print(len(wlist))

to_write = '\n'.join(wlist)
with codecs.open("chinese_words.pinyin.simple.txt", 'w+', encoding="utf-8") as fw:
    fw.write(to_write)

with codecs.open('chinese_words.pinyin.dict.txt', 'r', encoding="utf-8") as fr:
    aldict = json.load(fr)

aldict = {x:y for x,y in aldict.items() if 6 <= len(x) <= 10}
print(len(aldict))
with codecs.open('chinese_words.pinyin.dict.txt', 'w+', encoding="utf-8") as fw:
    json.dump(aldict, fw, ensure_ascii=False)
