#!/usr/bin/python
import math
emission_cts = dict() #(word, tag): count
unigram_cts = dict() #(tag): count
words = list()

with open("ner_rare.counts", "r") as f_in:
    for line in f_in:
        line = line.split()

        if line[1] == "WORDTAG":
            words.append(line[-1])
            emission_cts[(line[-1],line[-2])] = int(line[0])
        elif line[1] == "1-GRAM":
            unigram_cts[line[-1]] = int(line[0])
        else: #small speed improvement
            break
words = tuple(words) #small speed improvement
for key, value in emission_cts.items():
    emission_cts[key] = math.log(value / unigram_cts[key[1]])

with open("ner_dev.dat", "r") as f_in:
    with open("4_2.txt", "w") as f_out:
        for line in f_in:
            rare = False
            line = line.split()
            if len(line) == 0:
                f_out.write("\n")
                continue

            largest = ("tag",float("-inf"))
            if line[0] not in words:
                rare = True

            for key in unigram_cts:
                if rare:
                        word = "_RARE_"
                else:
                    word = line[0]
                if (word,key) in emission_cts and emission_cts[(word,key)] > largest[1]:
                        largest = (key, emission_cts[(word, key)])
            f_out.write(line[0] + " " + largest[0] + " " +str(largest[1]) + "\n")
