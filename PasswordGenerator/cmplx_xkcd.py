import random
import utils
from elements import element

DEFAULT_WORDFILE = "eff_4_dice_2.txt"


class XKCD():
    LOWER = 1
    UPPER = 2
    RANDOM = 3
    CAPITAL = 4

    def __init__(self,
                 case=4,
                 count=4,
                 c_num=0,
                 sep='-',
                 length=25,
                 wordfile=None):
        if wordfile:
            element.word_file(wordfile)
        self.len_min = element.len_min()
        self.len_max = element.len_max()
        self.count = count
        self.length = length
        if not self.check_valid():
            self.password = None
            return
        self.password = sep.join(self.choose_words())
        self.insert_random_numbers(c_num)
        self.password = utils.do_case(self.password, case)

    def choose_words(self):
        length = self.length - (self.count - 1)
        words = []
        if length <= 0:
            return element.get_words(self.count)
        for i in range(1, self.count + 1):
            max_len = min(self.len_max,
                          length - (self.count - i) * self.len_min)
            min_len = max(self.len_min,
                          length - (self.count - i) * self.len_max)
            word_len = random.randint(min_len, max_len)
            words.extend(element.get_words_by_len(word_len))
            length -= word_len
        return words

    def check_valid(self):
        sep_count = self.count - 1
        max_len = sep_count + self.count * self.len_max
        min_len = sep_count + self.count * self.len_min
        if self.length <= 0:
            return True
        elif self.length < min_len or self.length > max_len:
            print(f"length should be between {min_len} ~ {max_len}")
            return False
        return True

    def insert_random_numbers(self, c_num):
        while c_num > 0:
            random.seed()
            index = random.randint(0, self.length)
            ran_num = random.randint(0, 9)
            if not self.password[index].isdigit():
                self.password = f"{self.password[:index]}{ran_num}{self.password[index+1:]}"
                c_num -= 1

    def __str__(self):
        return self.password or ''


if __name__ == "__main__":
    a = XKCD()
    print(a)
