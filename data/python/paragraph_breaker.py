#---------------------------------------------------------------------
# Runs NLTK tagger on given file
# Author: Paul Bucci, unless otherwise noted
#---------------------------------------------------------------------
import os
import pprint
import ast
import nltk
import nltk.data

# This grammar is described in the paper by S. N. Kim,
# T. Baldwin, and M.-Y. Kan.
# Evaluating n-gram based evaluation metrics for automatic
# keyphrase extraction.
# Technical report, University of Melbourne, Melbourne 2010.
grammar = r"""
    NBAR:
        # Nouns and Adjectives, terminated with Nouns
        {<NN.*|JJ>*<NN.*>}

    NP:
        {<NBAR>}
        # Above, connected with in/of/etc...
        {<NBAR><IN><NBAR>}
"""
chunker = nltk.RegexpParser(grammar)
pagedir = 'clean_transcripts/'
outdir = 'one_sentence_per_line/'
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def tag_page(f):
	file = open(pagedir + f)
	out = open(outdir + f,"w+")
	for line in file:
		lines = sent_detector.tokenize(line.strip())
		for l in lines:
			# text = nltk.word_tokenize(line)
			# tagged = nltk.pos_tag(text)
			out.write(l + "\n")
	out.close()
	file.close()

for file in os.listdir(pagedir):
	if file.endswith(".txt"):
		print('Tagging ' + file)
		tag_page(file)