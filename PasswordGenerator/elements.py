import random
import utils

DEFAULT_WORDFILE = "eff_4_dice_2.txt"
WORD_LIST = utils.get_wordlist(DEFAULT_WORDFILE)
WORD_DICT = utils.get_worddict_from_list(WORD_LIST)

SYMBOLS = ['`', '!', '"', '?', '$', '?', '%',
           '^', '&', '*', '(', ')', '_', '-',
           '+', '=', '{', '[', '}', ']', ':',
           ';', '@', "'", '~', '#', '|', '<',
           ',', '>', '.', '?', '/']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6',
           '7', '8', '9']
ALPHAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
          'h', 'i', 'j', 'k', 'l', 'm', 'n',
          'o', 'p', 'q', 'r', 's', 't', 'u',
          'v', 'w', 'x', 'y', 'z']


class Element:
    def len_min(self):
        return min(WORD_DICT)

    def len_max(self):
        return max(WORD_DICT)

    def word_file(self, cus_wordfile=None):
        global WORD_LIST, WORD_DICT
        if not cus_wordfile:
            return
        WORD_LIST = utils.get_wordlist(DEFAULT_WORDFILE, cus_wordfile)
        WORD_DICT = utils.get_worddict_from_list(WORD_LIST)

    def get_alpha(self, length=1):
        random.seed()
        return random.choices(ALPHAS, k=length)

    def get_numbers(self, length=1):
        random.seed()
        return random.choices(NUMBERS, k=length)

    def get_symbols(self, length=1):
        random.seed()
        return random.choices(SYMBOLS, k=length)

    def get_words(self, count=1):
        return self.choices(WORD_LIST, k=count)

    def get_words_by_len(self, length=-1, count=1):
        if length not in WORD_DICT:
            return []
        else:
            random.seed()
            return self.choices(WORD_DICT[length], k=count)

    def choices(self, population, k=1):
        """make sure we don't get repeat result from random.choices"""
        while True:
            random.seed()
            words = random.choices(population=population, k=k)
            if len(set(words)) == k:
                return words


element = Element()