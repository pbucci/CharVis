#---------------------------------------------------------------------
# Identifies all concepts and outputs as a list
# Author: Paul Bucci except where otherwise noted
#---------------------------------------------------------------------


# Imports ------------------------------------------------------------
import os
import pprint
import ast
import nltk
import nltk.data

# Grammar ------------------------------------------------------------
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


pagedir = 'clean_transcripts/'
outdir = 'one_sentence_per_line/'


## Concepts -----------------------------------------------------------
# A class for dealing with concepts in a document
class Concepts:
	def __init__(self):
		self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		self.chunker = nltk.RegexpParser(grammar)

	## find_concepts --------------------------------------------------
	# page : list of strings where every string 
	# 		 could be one or more sentences
	# Returns : set of concepts as a dictionary
	def find_concepts(page):
		concepts = {}
		for line in page:
			sentences = find_sentences(line)
			for s in sentences:
				tagged = tag_sentence(s)

	## chunk_sentence -------------------------------------------------
	def chunk_sentence(ts):
		tree = chunker.parse(ts)
		


	## find_sentences -------------------------------------------------
	# Parses a paragraph for all sentences
	# Returns : list of strings that are sentences
	# p : string
	def find_sentences(p):
		sentences = self.sent_detector.tokenize(p.strip())
		return sentences

	## tag_sentence ---------------------------------------------------
	# Parses a sentence for part of speech tags
	# Returns : POS-tagged string
	# s : string
	def tag_sentence(s):
		text = nltk.word_tokenize(s.strip())
		tagged = nltk.pos_tag(text)
		return tagged

def tag_page(f):
	file = open(pagedir + f)
	out = open(outdir + f,"w+")
	
	out.close()
	file.close()

for file in os.listdir(pagedir):
	if file.endswith(".txt"):
		print('Tagging ' + file)
		tag_page(file)