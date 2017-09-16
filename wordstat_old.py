from __future__ import division
import nltk, re, pprint
from nltk import FreqDist
from nltk import word_tokenize
from nltk.collocations import *
import io
import string
import sys
import getopt
import pickle

in_file = False
out_file = False
min_freq = 50
min_len = 3
phrase_len = 1
out_dir =  "out/"
preload_tokens = False
tokenize_mode = False
token_file = ""
conc_term = ""

def parseArgs ():
    global in_file, out_file, min_freq, min_lin, out_dir,preload_tokens,tokenize_mode,token_file, conc_term
    
    print "Parsing arguments..."
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hi:o:m:f:bt:c:z",
                                   ["in_file=",
                                    "out_file=",
                                    "min_len=",
                                    "min_freq=",
                                    "bigram",
                                    "token_file=",
                                    "tokenize",
                                    "conc="])

    except getopt.GetoptError:
        print 'Usage message tmp: options: -i -o -h -m -f -b -t'
        sys.exit(2)

    print opts
    print sys.argv
    
    for opt, arg in opts:
        print opt + " " + arg
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--in_file"):
            in_file = arg
        elif opt in ("-o", "--out_file"):
            out_file = arg
        elif opt in ("-l", "--min_len"):
            max_len = arg
        elif opt in ("-f", "--min_frequency"):
            min_freq = arg
        elif opt in ("-b", "--bigram"):
            phrase_len = 2
        elif opt in ("-t", "--token_file"):
            preload_tokens = True
            token_in_file = arg
        elif opt in ("-z", "--tokenize"):
            tokenize_mode = True
            print "Tokenize mode..."
        elif opt in ("-c", "--conc"):
            conc_term = arg

        
def printTop(n,min_len):
    out_file = out_dir + "output_min_" + str(n) + "_len_gt_" + str(min_len) + ".csv"
    fdist1 = FreqDist(tokens)
    most_common =  fdist1.most_common(n)
    out_fh = open(out_file, "w")
    header = "word,frequency\n"
    out_fh.write(header);
    for tup in most_common:
        if (len(tup[0]) >= min_len):
            line = "\"" + tup[0] + "\"," + str(tup[1]) + "\n"
#            print line
            out_fh.write(line)

    out_fh.close()

def printTopBigrams(n):
    out_file = out_dir + "output_bigrams.csv"
    bigrams = nltk.bigrams(tokens)

    fdist1 = nltk.FreqDist(bigrams)
    most_common = fdist1.most_common(2000)

    out_fh = open(out_file,"w")
    header = "word1,word2,frequency\n"
    out_fh.write(header);
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

# read in a text file and output a token file
def tokenize():
    
    # Process input file
    #-----------------------------

    f = io.open (in_file)
    raw = f.read().lower()
    f.close()

    printable = set(string.printable)
    raw = filter(lambda x: x in printable, raw)
    raw = filter(lambda x: x.isalpha() or x.isspace(), raw)
    print "Opened file " + in_file + " of size " + str(len(raw)) + " bytes."
    print "Tokenizing..."
    tokens = word_tokenize(raw)

    return tokens

def tokenize_to_file():

    if in_file == False or out_file == False:    
        print "Error: Tokenize mode requires input and output files"
        exit (2)
    # save to binary file
    #-----------------------------

    tokens = tokenize()
    
    if ".token" not in out_file:
        out_file += ".token"

    of = open(out_file,"w")
    pickle.dump(tokens, of)

    of.close()

def main():

    parseArgs()
    
    if tokenize_mode:
        tokenize_to_file()
        exit(1)
    else:
        print "Tokenize mode: false..."
        
def oldMain():
    
    set(word.lower() for word in raw if word.isalpha())

    print "Found " + str(len(tokens)) + " tokens."

    #printTop(2000, 1)

    print "Now processing bigrams"

    #printTopBigrams(50)

    print "Done!"

main()
