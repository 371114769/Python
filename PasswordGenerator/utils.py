import random
import os
import codecs
import json


def do_case(text: str, case):
    """转换英文的格式
    :case: 1:lower, 2:upper, 3:random, 4:title"""
    if int(case) == 1:
        text = text.lower()
    elif int(case) == 2:
        text = text.upper()
    elif int(case) == 4:
        text = text.title()
    elif int(case) == 3:
        if text.isalpha():
            random.seed()
            alpha_upper_count = random.randint(1, len(text) - 1)
            text = text[:alpha_upper_count].upper() + text[alpha_upper_count:]
        else:
            new_word = ""
            for char in text:
                random.seed()
                if not char.isalpha():
                    pass
                elif random.randint(1, 10) > 5:
                    char = char.upper()
                else:
                    char = char.lower()
                new_word = f"{new_word}{char}"
            text = new_word
    return text


def get_wordfile(DEFAULT_WORDFILE, cus_wordfile=None):
    word_files = []
    default_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'wordfiles')

    if cus_wordfile:
        word_files.append(os.path.join("wordfiles", cus_wordfile))
        word_files.append(os.path.join(default_dir, cus_wordfile))
        word_files.append(os.path.join(os.path.expanduser(cus_wordfile)))

    word_files.append(os.path.join(default_dir, DEFAULT_WORDFILE))
    for wfile in word_files:
        if os.path.isfile(wfile):
            return wfile


def get_json(wfile):
    file = get_wordfile(wfile)
    with codecs.open(file, 'r', encoding="utf-8") as fr:
        cn_dict = json.load(fr)
    return cn_dict


def get_wordlist(DEFAULT_WORDFILE,
                 cus_wordfile=None,
                 minimun=0,
                 maximun=99):
    word_file = get_wordfile(DEFAULT_WORDFILE, cus_wordfile)
    word_list = []
    with codecs.open(word_file, 'r', encoding="utf-8") as fr:
        while True:
            word = fr.readline()
            if not word:
                break
            word_len = len(word)

            if word_len > minimun and word_len < maximun:
                word = word.strip("\n")
                word_list.append(word)
    return word_list


# version1
def get_worddict(DEFAULT_WORDFILE,
                 cus_wordfile=None,
                 minimun=0,
                 maximun=99):
    word_list = get_wordlist(DEFAULT_WORDFILE,
                             cus_wordfile,
                             minimun,
                             maximun)
    word_dict = {}
    for word in word_list:
        if len(word) in word_dict:
            word_dict[len(word)].append(word)
        else:
            word_dict[len(word)] = [word]


# version2
def get_worddict_from_list(wordlist):
    word_dict = {}
    for word in wordlist:
        if len(word) in word_dict:
            word_dict[len(word)].append(word)
        else:
            word_dict[len(word)] = [word]
    return word_dict


def break_order(src_iterable):
    old_list = [i for i in src_iterable]
    new_list = []
    for i in range(len(old_list)):
        index = random.randrange(len(old_list))
        new_list.append(old_list.pop(index))
    dst_string = ''.join(new_list)
    return dst_string

# class Words():
#     def __init__(self,
#                  DEFAULT_WORDFILE,
#                  wordfile=None,
#                  minimun=0,
#                  maximun=99):
#         self.word_file = get_wordfile(DEFAULT_WORDFILE, cus_wordfile=wordfile)
#         self.wdict = {}
#         self.wlist = []
#         self.make_wordlist()
#         self.make_worddict()
#         self.len_min = min(self.wdict.keys())
#         self.len_max = max(self.wdict.keys())

#     def make_wordlist(self, minimun=0, maximun=99):
#         with codecs.open(self.word_file, 'r', encoding="utf-8") as fr:
#             while True:
#                 word = fr.readline()
#                 if not word:
#                     break
#                 word_len = len(word)
#                 if word_len > minimun and word_len < maximun:
#                     word = word.strip("\n")
#                     self.wlist.append(word)

#     def make_worddict(self):
#         for word in self.wlist:
#             if len(word) in self.wdict:
#                 self.wdict[len(word)].append(word)
#             else:
#                 self.wdict[len(word)] = [word]

#     def __getitem__(self, key):
#         return self.wdict[int(key)]

#     def __iter__(self):
#         return self.wlist

#     def __len__(self):
#         return len(self.wlist)
