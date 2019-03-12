# Tagging
Part of Speech Tagging
Helper files and training data needed to run these files have been excluded as they do not belong to me.
 
rare_words.py - maps words seen infrequently in the training data (less than 5 times) to a common class.
simple_tagger.py - computes most likely tag and corresponding log likelihood for each word.
trigram_prob.py - calculates maximum likelihood estimates for all trigrams seen in the training data.
viterbi_tagger.py - computes most likely tag sequence using the Viterbi algorithm.
