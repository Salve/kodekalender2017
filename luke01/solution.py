#!/usr/bin/env python3

words = []
with open('wordlist.txt') as fp:
    for cnt, line in enumerate(fp):
        words.append(line)
        print(cnt)

print(words[0], words[-1])

