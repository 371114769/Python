with open('words.txt', 'r') as fr:
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
print(min_len, max_len, avg_len, sum_len, count, sep="\n")

print(*[f"{l:>2}: {c}" for l,c in len_dict.items()], sep="\n")
