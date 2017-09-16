#!/usr/bin/python

from WordStat import WordStat

import sys
def main():

    if len(sys.argv) < 2:
        print "Usage error"
        exit (2)
        
    #ws.tokenizeFromFile("all.txt")

    #ws.tokenize(fh.read().lower())
    #fh.close()
    #ws.exportTokens("all")

    ws = WordStat()
    ws.loadTokens("all.tokens")
    ws.bigramize()

    #ws.writeTopWords(10000,4,open("words.csv","w"))
    #ws.writeTopBigrams(10000,4,open("bigrams.csv","w"))

    ws.printExcerpts(ws.getContext(" ".join(sys.argv[1:]))[0:10])

main()
