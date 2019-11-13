import random

len_dict = {i:[] for i in range(1,9)}

with open('words.txt', 'r') as fr:
    wlist = fr.read().split()
    for w in wlist:
        len_dict[len(w)].append(w)

class XKCD():
    LOWER = 1
    UPPER = 2
    CAPITAL = 3
    RANDOM = 4

    def __init__(self, case=3, words=3, nums=0, sep='-', length=25):
        self.words = words
        self.length = length
        if not self.check_valid():
            self.password = None
            return
        alpha_len = length - (words - 1)
        self.password = sep.join([i for i in self.generate_password(alpha_len)])
        self.trans_num(nums)
        self.make_case(case)
    
    def make_case(self, case_inx):
        if case_inx == 1:
            self.password = self.password.lower()
        elif case_inx == 2:
            self.password = self.password.upper()
        elif case_inx == 3:
            self.password = self.password.title()
        elif case_inx == 4:
            rdm_case_pwd = ""
            for a in self.password:
                random.seed()
                if not a.isalpha(): pass
                elif random.randint(1, 10) > 7:
                    a = a.upper()
                else:
                    a = a.lower()
                rdm_case_pwd = f"{rdm_case_pwd}{a}"
            self.password = rdm_case_pwd
        
    def generate_password(self, length):
        len_alpha = length - (self.words - 1)
        for i in range(1, self.words + 1):
            max_len = min(8, (length - (self.words - i)))
            min_len = max(1, length - ((self.words - i) * 8))
            word_len = random.randint(min_len, max_len)
            word = random.choice(len_dict[word_len])
            length -= word_len
            yield word

    def check_valid(self):
        max_len = (self.words-1) + self.words*8
        min_len = (self.words-1) + self.words
        if self.length < min_len or self.length > max_len:
            print(f"length should be between {min_len} ~ {max_len}")
            return False
        return True
    
    def trans_num(self, nums):
        new_pwd = ""
        while nums > 0:
            random.seed()
            index = random.randint(0, self.length)
            ran_num = random.randint(0,9)
            # 数字也跳过, 符号也跳过, 只要字母
            if not self.password[index].isalpha():
                continue
            else:
                self.password = f"{self.password[:index]}{ran_num}{self.password[index+1:]}"
                nums -= 1

    def __str__(self):
        return self.password or ''

if __name__ == "__main__":
    a = XKCD()
    print(a)
