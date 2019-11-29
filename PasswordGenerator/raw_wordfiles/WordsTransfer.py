# import openpyxl
import pypinyin
import codecs


def temp1(word):
    if not word.isalpha():
        return None
    if len(word) <= 8:
        return word


def eff_large(word):
    if word.isalpha():
        return word
    return False


alphabet = [chr(i) for i in range(97, 123)]
alphabet.extend([chr(i) for i in range(65, 91)])
def chinese(word):
    word = ''.join([w for w in word if not w.isdigit()])
    word = ''.join([w for w in word if w not in alphabet])
    word = word.replace(" ", "")
    if len(word) == 1:
        return False
    return word


def to_pinyin(word):
    pinyin = pypinyin.lazy_pinyin(word, style=pypinyin.Style.TONE3)
    for i in pinyin:
        if i.isalpha():
            return False
    pinyin = ','.join(pinyin)
    return f"{pinyin}|{word}"


def to_lazy_pinyin(word):
    pinyin = pypinyin.lazy_pinyin(word)
    return ''.join(pinyin)


def get_word_list(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        word_list = f.read().split()
    return word_list


def remove_repeat(filename):
    word_list = get_word_list(filename)
    word_list = list(set(word_list))
    word_list.sort()
    with codecs.open(filename, 'w', encoding="utf-8") as fw:
        for word in word_list:
            fw.write(f"{word}\n")


def transfer(filename, new_name=None, ext_name=None):
    word_list = get_word_list(filename)

    new = filename.rsplit('.', 1)
    new.insert(1, ext_name or 'transed')
    new_file = new_name or '.'.join(new)
    with codecs.open(new_file, 'w', encoding="utf-8") as fw:
        for word in word_list:
            word = to_pinyin(word)
            if word:
                fw.write(f"{word}\n")
                print(word)
    remove_repeat(new_file)


def tran_from_exel(filename):
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    for row in range(1, ws.max_row + 1):
        print(ws.cell(row, 1).value)


# tran_from_exel("chinese_words.xlsx")
transfer("chinese_words.txt", ext_name='pinyin')
# remove_repeat("chinese_words.pinyin.no.tune.txt")
