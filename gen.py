#!/usr/bin/env python
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()

name = args.name.lower()

vowels = "aeiou"
consts = "bcdfghjklmnpqrstvwxyz"

nonewords = [
    "about"
]

def rank2(abv):
    r = 1
    if abv[1] in vowels and abv[0] in consts:
        r *= 2
        if abv[0] in "bclsp":
            r *= 1.5
        if abv[0] in "xz":
            r /= 1.5
    return r

def rank2i(abv):
    return rank2(abv[1] + abv[0])

def rank3(abv):
    return max(
        rank2(abv[0:2]) * rank2i(abv[1:3]),
        rank2i(abv[0:2]) * rank2(abv[1:3])
    )

def rank4(abv):
    r3 = rank3(abv[1:4])
    if abv[0] in vowels:
        r3 *= 1.8
    r2a, r2b = rank2(abv[0:2]), rank2(abv[2:4])
    return max(r3, r2a, r2b)

def sum_seqs(n, m, initial=[]):
    if m == 1:
        yield initial + [n]
    else:
        for i in range(n+1):
            new = initial + [i]
            yield from sum_seqs(n-i, m-1, new)

class BadName(Exception):
    pass

def possible_names(myname):
    if len(myname) < 4:
        print("Name too short", file=sys.stderr)
        sys.exit(1)
    words = [word for word in myname.split(" ") if word not in nonewords and (len(word) >= 4)]
    if not words:
        print("Name too short", file=sys.stderr)
        sys.exit(1)
    seqs = sum_seqs(4, len(words))
    for seq in seqs:
        abv = []
        try:
            for i, n in enumerate(seq):
                if n == 0 and i == 0:
                    raise BadName()
                if len(words[i]) < n:
                    continue
                abv.append(words[i][0:n])
        except BadName:
            pass
        name = "".join(abv)
        if name != "":
            yield name

bestname = None
bestrank = 0
for aname in possible_names(name):
    rank = rank4(aname)
    if rank > bestrank:
        bestrank = rank
        bestname = aname
    #print("Name: %s, rank: %f" % (aname.upper(),rank4(aname)))
#print()
#print("Best name:")
print(bestname.upper())
