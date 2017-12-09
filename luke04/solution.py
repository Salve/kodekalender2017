#!/usr/bin/env python3
from collections import Counter

def is_palindrome(word):
    return word == word[::-1]

with open('ordliste.txt') as fp:
    words = [line.strip() for line in fp.readlines()]

num_possible_palindromes = 0
for word in words:
    if is_palindrome(word): continue
    letter_count = Counter(word)
    odd_lettercounts = [x for x in letter_count.values() if x % 2 == 1]
    if len(odd_lettercounts) <= 1:
        num_possible_palindromes += 1

print(num_possible_palindromes)

