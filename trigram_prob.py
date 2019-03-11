#!/usr/bin/python
two_gram = dict()
three_gram = dict()
from math import log
#get n-gram counts
with open("ner_rare.counts", "r") as f_in:
    for line in f_in:
        line = line.split()
        if line[1] == "2-GRAM":
            two_gram[(line[-2], line[-1])] = int(line[0])
        elif line[1] == "3-GRAM":
            three_gram[(line[-3], line[-2], line[-1])] = int(line[0])

with open("trigrams.txt", "r") as f_in:
    with open("5_1.txt", "w") as f_out:
        for line in f_in:
            line = tuple(line.split())
            if line in three_gram:
                three_gram[line] = log(three_gram[line]/two_gram[(line[0], line[1])])
            f_out.write(" ".join(line) + " " + str(three_gram[line]) + "\n")
