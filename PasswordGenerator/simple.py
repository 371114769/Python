from elements import element
import utils
import secrets

CN_DICT = utils.get_json("chinese_words.pinyin.dict.txt")


def xkcd_cn(words=3):
    element.word_file("chinese_words.pinyin.txt")
    words = element.get_words(words)
    words_with_case = [utils.do_case(w, 4) for w in words]
    password = '-'.join(words_with_case)
    explain = '-'.join([CN_DICT[i] for i in words])
    print(password)
    print(explain)


def xkcd_en(words=3):
    element.word_file("eff_4_dice_2.txt")
    words = element.get_words(words)
    words_with_case = [utils.do_case(w, 4) for w in words]
    password = '-'.join(words_with_case)
    print(password)


def custom(numbers=4, alphas=6, symbols=2):
    src_list = []
    src_list.extend(element.get_alpha(alphas))
    src_list.extend(element.get_numbers(numbers))
    src_list.extend(element.get_symbols(symbols))
    password = utils.break_order(src_list)
    password = utils.do_case(password, 3)
    print(password)


def url_safe(length=16):
    password = secrets.token_urlsafe(length)
    print(password)


if __name__ == "__main__":
    xkcd_en()
    xkcd_cn()
    custom()
    url_safe()
