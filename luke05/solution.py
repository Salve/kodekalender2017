#!/usr/bin/env python3

rekke = [0, 1, 2, 2]
current = 3
while(len(rekke)<1000000):
    rekke.extend([current]*rekke[current])
    current += 1

print(sum(rekke[:1000001]))

