import os
import codecs

def analyze(file):
    with codecs.open(file, 'r', encoding="utf-8") as fr:
        wlist = fr.read().split()

    min_len = 10
    max_len = 0
    avg_len = 0
    sum_len = 0
    len_dict = {}
    count = len(wlist)

    for word in wlist:
        w_len = len(word)
        sum_len += w_len
        min_len = min(min_len, w_len)
        max_len = max(max_len, w_len)
        if w_len in len_dict:
            len_dict[w_len] += 1
        else:
            len_dict[w_len] = 1

    avg_len = round(sum_len / count, 1)
    print(file)
    print("min:", min_len)
    print("max:", max_len)
    print("avg:", avg_len)
    print("words set:", len(set(wlist)))
    print("words:", len(wlist))
    print("count:", count)
    for i in range(1, max(len_dict.keys()) + 1):
        if i in len_dict:
            print(f"{i:>2}: {len_dict[i]}")
        else:
            print(f"{i:>2}: 0")

    print("")

if __name__ == "__main__":
    for wfile in os.listdir('./'):
        if wfile.rsplit('.', 1)[1] == 'txt':
            analyze(wfile)
