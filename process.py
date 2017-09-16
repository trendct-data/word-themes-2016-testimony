from __future__ import division
import nltk, re, pprint
from nltk import FreqDist
from nltk import word_tokenize
from nltk.collocations import *
import io
import string

def printTop(n,min_len):
    out_file = "output_min_" + str(n) + "_len_gt_" + str(min_len) + ".csv"
    fdist1 = FreqDist(tokens)
    most_common =  fdist1.most_common(n)
    out_fh = open(out_file, "w")
    for tup in most_common:
        if (len(tup[0]) >= min_len):
            line = "\"" + tup[0] + "\"," + str(tup[1]) + "\n"
#            print line
            out_fh.write(line)

    out_fh.close()

def printTopBigrams(n):
    out_file = "output_bigrams.csv"
    bigrams = nltk.bigrams(tokens)

    fdist1 = nltk.FreqDist(bigrams)
    most_common = fdist1.most_common(2000)

    out_fh = open(out_file,"w")
    for tup in most_common:
        #print tup
        line = "\"" + str(tup[0][0]) + "\",\"" + str(tup[0][1]) + "\"," + str(tup[1]) + "\n"
        #print line
        out_fh.write(line)

    out_fh.close()

def context(word):

    return nltk.ConcordanceIndex(tokens)

def context2(word, word2):
    #len = 255
    trail_len = 255 - len(word) - len(word2)
    cont = context(word)
    strs = []
    for i in cont.offsets(word):

        start = max(0, i - trail_len)

        end = end = min(i+120,len(raw))

#        print str(start) + ":" + str(end)
        excerpt = raw[start:end]

        if word2 in excerpt:
            strs.append(excerpt)

    return strs
in_file = "all.txt"
f = io.open (in_file)
raw = f.read().lower()
f.close()

printable = set(string.printable)
raw = filter(lambda x: x in printable, raw)
raw = filter(lambda x: x.isalpha() or x.isspace(), raw)
print "Opened file " + in_file + " of size " + str(len(raw)) + " bytes."
print "Tokenizing..."
tokens = word_tokenize(raw)
set(word.lower() for word in raw if word.isalpha())

print "Found " + str(len(tokens)) + " tokens."

printTop(2000, 1)

print "Now processing bigrams"

printTopBigrams(50)

print "Done!"
