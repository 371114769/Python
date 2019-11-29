import random
import utils
from elements import element

pwd_len = 15
cmin = 3
SYMBELS = ['`', '!', '"', '?', '$', '?', '%',
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


class PwdPart():
    pwd_remain = pwd_len
    remain_parts = 0
    pwd_seq = []

    def __init__(self, choice, chr_pool, at_least=cmin):
        PwdPart.remain_parts -= 1
        self.choice = choice
        self.chr_pool = chr_pool
        self.text = ""
        self.at_least = at_least
        self.random_length()
        self.make_choice()

    def random_length(self):
        if PwdPart.pwd_remain <= 0:
            self.length = 0
            return
        elif self.choice == -2 or PwdPart.remain_parts == 0:
            self.length = PwdPart.pwd_remain
        elif self.choice == -1:
            a = self.at_least
            b = PwdPart.pwd_remain - cmin * PwdPart.remain_parts
            random.seed()
            self.length = random.randint(a, b)
        else:
            self.length = self.choice
        PwdPart.pwd_remain -= self.length

    def make_choice(self):
        random.seed()
        chrs = random.choices(self.chr_pool, k=self.length)
        self.text = ''.join([i for i in chrs])
        PwdPart.pwd_seq += chrs

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)


def reorder_text(rawstring):
    chr_pool = [i for i in rawstring]
    pwd_seq = []
    for i in range(pwd_len):
        index = random.randrange(len(chr_pool))
        pwd_seq.append(chr_pool.pop(index))
    password = ''.join(pwd_seq)
    return password


def chars16(case=3, c_sym=3, c_num=-2, c_alpha=-1):
    """
    :case: 1:lower, 2:upper, 3:random, 4:title
    :c_sym, c_num, c_alpha: -2:fill the rest, -1:random, 0-15:how much you want
    """
    global pwd_len
    PwdPart.remain_parts = bool(c_sym) + bool(c_num) + bool(c_alpha)
    order = [c_sym, c_num, c_alpha]

    if order.count(-2) >= 2:
        print("Could only have one type to fill")
        return
    if not PwdPart.remain_parts:
        print("Nothing to make")
        return
    if sum(order) > pwd_len:
        pwd_len = sum(order)
        PwdPart.remain_parts = pwd_len

    order = list(set(order))
    order.sort()
    order.reverse()

    for i in order:
        if c_alpha == i:
            alpha = PwdPart(c_alpha, ALPHAS, at_least=6)
            alpha.text = utils.do_case(alpha.text, case)
        if c_sym == i:
            PwdPart(c_sym, SYMBELS)
        if c_num == i:
            PwdPart(c_num, NUMBERS)

    return reorder_text(PwdPart.pwd_seq)


if __name__ == "__main__":
    pwd = chars16()
    print(pwd)
