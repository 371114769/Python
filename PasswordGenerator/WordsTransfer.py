import codecs
with codecs.open('words.txt', 'r', encoding='utf-8') as f:
    word_list = f.read().split()

with open('words.txt', 'w') as fw:
    for word in word_list:
        if not word.isalpha(): continue
        if len(word) <= 8:
            fw.write(f"{word}\n")
