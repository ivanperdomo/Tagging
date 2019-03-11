#!/usr/bin/python
from collections import defaultdict
counts = defaultdict(int)
words = list()

# TALLY UP HOW MANY TIMES EACH WORD APPEARS IN TRAINING SET
with open("ner_train.dat", "r") as f_in:
    for line in f_in:
        line = line.split()
        if len(line) > 0: counts[line[0]] += 1

with open("ner_train.dat", "r") as f_in:
    with open("ner_train_rare.dat", "w") as f_out:
        for line in f_in:
            line = line.split()

            if len(line) == 0: #empty line
                f_out.write("\n")
            elif counts[line[0]] < 5:
                f_out.write("_RARE_ " + line[-1]+ "\n")
            else:
                f_out.write(" ".join(line) + "\n")

