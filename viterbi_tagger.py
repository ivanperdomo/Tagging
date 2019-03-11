#!/usr/bin/python
#Emission,trigram probabilities copy/pasted from 4_2.py, 5_1.py
import math

emission_cts = dict() #(word, tag): count
unigram_cts = dict() #(tag): count
two_gram = dict()
three_gram = dict()
words = list()


# READ IN RARE.COUNTS TO GET TRIGRAM, BIGRAM, UNIGRAM COUNTS
with open("ner_rare.counts", "r") as f_in:
    for line in f_in:
        line = line.split()

        if line[1] == "WORDTAG":
            words.append(line[-1])
            emission_cts[(line[-1],line[-2])] = int(line[0])
        elif line[1] == "1-GRAM":
            unigram_cts[line[-1]] = int(line[0])
        elif line[1] == "2-GRAM":
            two_gram[(line[-2], line[-1])] = int(line[0])
        elif line[1] == "3-GRAM":
            three_gram[(line[-3], line[-2], line[-1])] = int(line[0])

words = tuple(words) #small speed improvement
possible_tags = [x for x in unigram_cts]
# CONVERT EMISSION COUNTS TO LOG PROBABILITIES
for key, value in emission_cts.items():
    emission_cts[key] = math.log(value / unigram_cts[key[1]])

# READ FILE INTO LIST OF LISTS, EACH SENTENCE IS ITS OWN LIST
sentences = list()
with open("ner_dev.dat", "r") as f_in:
    file = f_in.read().splitlines()

sentences.append(list())
for word in file:
    if word == "":
        sentences.append(list())
    else:
        sentences[-1].append(word)

f_out = open("5_2.txt", "w")
for sentence in sentences:
    bp = dict()
    pi_table = {(0,"*","*"): 0}# (index, TAG u, TAG v)=probability
    for index, word in enumerate(sentence):
        # DETERMINING POSSIBLE TAGS FOR EACH POSITION
        if index == 0:
            u_tags, w_tags = ["*"], ["*"]
        elif index == 1:
            u_tags = possible_tags
            w_tags = ["*"]
        else:
            u_tags = possible_tags
            w_tags = possible_tags
        v_tags = possible_tags

        # IF WORD IS INFREQUENT OR DOES NOT APPEAR IN TRAINING DATA
        if word not in words:
            word = "_RARE_"

        for tag in v_tags:
            for tag_1 in u_tags:
                # new_pi = float("-inf")
                for tag_2 in w_tags:
                    tri = (index,tag_2,tag_1)
                    try:
                        new_pi = pi_table[tri] + math.log(three_gram[(tag_2,tag_1,tag)]/two_gram[(tag_2,tag_1)]) + emission_cts[(word,tag)]
                    except KeyError:
                        new_pi = float("-inf")
                    if new_pi != float("-inf"):
                        try:
                            if new_pi > pi_table[index+1, tag_1, tag]:
                                pi_table[(index+1, tag_1, tag)] = new_pi
                                bp[(index+1, tag_1, tag)] = tag_2
                        except KeyError: #pi table not populated yet
                            pi_table[(index+1, tag_1, tag)] = new_pi
                            bp[(index+1, tag_1, tag)] = tag_2

    last_two = ["", ""]
    last_two_prob = []
    biggest_so_far = float("-inf")
    if len(sentence) == 1: # EDGE CASE FOR SENTENCE OF LENGTH 1
        for tag in possible_tags:
            try:
                new = pi_table[(len(sentence),"*",tag)] + math.log(three_gram[("*",tag,"STOP")]/two_gram[("*",tag)])
                if new > biggest_so_far:
                    biggest_so_far = new
                    last_two = [tag]
            except KeyError:
                pass
        last_two_prob = [pi_table[(1, "*", last_two[0])]]
    else: # FOR SENTENCES LONGER THAN 1
        for tag1 in possible_tags: # U
            for tag2 in possible_tags: # V
                try:
                    new = pi_table[(len(sentence),tag1,tag2)] + math.log(three_gram[(tag1,tag2,"STOP")]/two_gram[(tag1,tag2)])
                    if new > biggest_so_far:
                        biggest_so_far = new
                        last_two = [tag1,tag2]
                except KeyError:
                    pass

    for k in range(len(sentence)-2,0,-1):
        try:
            last_two.insert(0, bp[(k+2,last_two[0],last_two[1])])
            last_two_prob.insert(0, pi_table[(k+1, last_two[0], last_two[1])])
        except KeyError:
            pass

    if len(sentence) > 1:
        last_two_prob.insert(0, pi_table[(2, last_two[0], last_two[1])])
        last_two_prob.insert(0, pi_table[(1, "*", last_two[0])])

    for index, word in enumerate(sentence):
        f_out.write(word+ " " +last_two[index] + " " + str(last_two_prob[index]) + "\n")
    f_out.write("\n")

f_out.close()







