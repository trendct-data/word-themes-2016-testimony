# WORDSTAT
# --------
# by Jake Kara

import nltk
import sys, getopt, pickle, string, io, pprint
from nltk import FreqDist
from nltk.collocations import *
from nltk import word_tokenize

class WordStat:

    verbose = True;

    # verbose-mode printing
    def printV(self,message):
        if self.verbose:
            print message

    # tokenize from a text file
    def tokenizeFromFile(self, in_file):
        fh = open(in_file,"r")
        self.tokenize(fh.read())
            
    # turn text into tokens
    def tokenize(self,raw):
        printable = set(string.printable) 
        
        self.raw = filter(lambda x: x in printable, raw)
        self.raw = filter(lambda x: x.isalpha() or x.isspace(), raw)

        self.printV("Tokenizing...")
        self.tokens = word_tokenize(self.raw)

        self.printV("Done tokenizing.")

    # get bigrams
    def bigramize(self):
        if not hasattr(self,"tokens"):
            print "Error: No tokens found."

        self.printV("Detecting bigrams (2-word pairs)...")
        self.bigrams = nltk.bigrams(self.tokens)
        self.printV("Done detecting bigrams.")

    # helper function for checking file extension
    def setExtension(self,word,ext):
        if word[-(len(ext)):] == ext:
            return word
        else:
            return word + "." + ext
        
    # helper function to export an object (via pickle)
    def exportObj(self,obj,out_file):
        fh = open(out_file,"w")
        pickle.dump(self.tokens,fh)
        fh.close()
        
    # export a token to a file
    def exportTokens(self,out_file):
        if not hasattr(self,"tokens"):
            print "Error: No tokens to export."

        self.printV("Exporting tokens to file...")
        self.exportObj(self.tokens,self.setExtension(out_file,"tokens"))
        self.printV("Done exporting tokens.")
            
    # export bigrams to a file
    # def exportBigrams(self,out_file):
    #     if not hasattr(self,"bigrams"):
    #         print "Error: No bigrams to export."

    #     self.printV("Exporting bigrams to file...")
    #     self.exportObj(self.bigrams,self.setExtension(out_file,"bigrams"))
    #     self.printV("Done exporting bigrams.")

    
    # load a pickled token
    def loadTokens(self,in_file):
        fh = open(in_file,"r")
        self.printV("Loading tokens from file...")
        self.tokens = pickle.load(fh)
        fh.close()
        self.printV("Done loading tokens.")
        
        
    # load bigrams from a file
    # def loadBigrams(self,in_file):
    #     return "Not implemented"

    #pint top words (CSV format)
    def writeTopWords(self, n, min_len,fh):
        fdist = FreqDist(self.tokens)
        most_common = fdist.most_common(n)
        header = "word,frequency\n"

        self.printV("Writing top words to file...")
        
        fh.write(header)        
        for tup in most_common:
            if (len(tup[0]) >= min_len):
                line = "\"" + tup[0] + "\"," + str(tup[1]) + "\n"
                fh.write(line)
        fh.close()

        self.printV("Done writing top words.")

    # print top bigrams in CSV format
    def writeTopBigrams(self,n,min_len,fh):
        fdist = nltk.FreqDist(self.bigrams)
        most_common = fdist.most_common(n)

        self.printV("Writing top bigrams to file...")
        

        header = "word1,word2,frequency\n"
        fh.write(header)
        for tup in most_common:
            if min(len(tup[0][0]),len(tup[0][1])) < min_len:
                   continue
            line = "\"" + str(tup[0][0]) + "\",\"" + str(tup[0][1]) + "\","
            line += str(tup[1]) + "\n"
            fh.write(line)
            
        fh.close()
        self.printV("Done writing top bigrams.")

    # return array of excerpts containing phrase
    def getContext(self,phrase):
        phrase = phrase.lower()
        first_word = phrase.split(" ")[0]

        context = nltk.ConcordanceIndex(self.tokens)
        
        excerpt_padding = 6
                
        excerpts = []
        
        for i in context.offsets(first_word):

            start = max(0, i - excerpt_padding)
            end = min(len(self.tokens), i + excerpt_padding)

            excerpt = " ".join(self.tokens[start:end])


            if phrase in excerpt:
                i_phrase = excerpt.index(phrase)
                excerpt = excerpt[i_phrase - 30:i_phrase+30+len(phrase)]
                if len(excerpt)  < 10:
                    continue
                excerpts.append(excerpt)
        return excerpts

    # pretty-print an excerpts array
    def printExcerpts(self, excerpts):
        for excerpt in excerpts:
            print "\t..." + excerpt + "..."

# def test():

#     ws = WordStat()
#     #fh = open("all.txt")

#     #ws.tokenizeFromFile("all.txt")

#     #ws.tokenize(fh.read().lower())
#     #fh.close()
#     #ws.exportTokens("all")

#     ws.loadTokens("all.tokens")
#     ws.bigramize()

#     #ws.writeTopWords(10000,4,open("words.csv","w"))
#     #ws.writeTopBigrams(10000,4,open("bigrams.csv","w"))

#     ws.printExcerpts(ws.getContext("mental health")[0:10])

# test()
