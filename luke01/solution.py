#!/usr/bin/env python3
import sys
from collections import Counter

def create_ngram(word, n):
    ngrams=[]
    for pos, char in enumerate(word):
        if (pos+n <= len(word)):
            ngrams.append(word[pos:pos+n])
    return ngrams

words = []
with open('wordlist.txt') as fp:
    for cnt, line in enumerate(fp):
        words.append(line.strip())

word_to_match = Counter(sys.argv[1])
max_n = int(sys.argv[2])

#print(''.join(create_ngram(sys.argv[1], max_n)))

for n in range(2,max_n+1):
    print("Scanning with n={0}".format(n))
    for word in words:
        word_ngram = ''.join(create_ngram(word, n))
        if (word_to_match == Counter(word_ngram)):
            print("MATCH! {0}-{1}".format(n, word))

