# Author: Paul Bucci except where otherwise noted
import os
import re
import nltk
import random
import json
import sentiment_mod as s
# from nltk.corpus import movie_reviews

# -*- coding: utf-8 -*-

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

st = StanfordNERTagger('stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'stanford-ner-2015-12-09/stanford-ner.jar',
					   encoding='utf-8')


from pprint import pprint

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

# pagedir = '../test_scripts/'
pagedir = '../clean_transcripts/'
metadir = '../meta/'
outdir = './test_dir/'
regex = re.compile('(.*?)(:)(.*)')

def np_pass(txt):
	pass

def randsent():
	return random.choice(["+","-",'0'])

def nps_in_paragraph(text):
	# print(text)
	tokenized_text = word_tokenize(text)
	classified_text = st.tag(tokenized_text)

	out = []
	temp = None
	pos = 0
	for p in classified_text:
		pos = pos + 1
		if p[1] != 'O':
			if temp == None:
				temp = (p[0],p[1])
			elif p[1] == temp[1]:
				temp = (temp[0] + " " + p[0],temp[1])
			else:
				if temp != None:
					out.append((temp,pos))
				temp = (p[0],p[1])
		else:
			if temp != None:
				out.append((temp,pos))
			temp = None

	if temp != ('START','NULL') and temp != None:
		out.append((temp,pos))
	return (out,tokenized_text)

def text_pass(paragraphs):
	out = []
	for p in paragraphs:

		# tokenized = nltk.word_tokenize(p['text'])
		# tagged = nltk.pos_tag(tokenized)
		# chunked = chunker.parse(tagged)
		# nps = list(chunked.subtrees(lambda t: t.label() == 'NP'))
		# save_nps = {' '.join([x for (x,y) in np.leaves()]) for np in nps}
		
		nps = nps_in_paragraph(p['text'])

		p['concepts'] = []

		sent_label = s.sentiment(p["text"])

		for np in nps[0]:
			# print(np)
			p['concepts'].append({'concept':np[0][0],'j':int(np[1]),'i':(int(np[1]) - len(np[0][0].split(' '))),'s':sent_label})

		# for n in save_nps:
		# 	starts = [m.start() for m in re.finditer(n.replace('[','').replace(']',''), p['text'])]
		# 	positions = [{'concept':n,'i':s,'j':s+len(n),'s':sent_label} for s in starts]
		# 	for pos in positions:
		# 		# print(pos)
		# 		if pos['concept'] != "[" and pos['concept'] != "]":
		# 			p['concepts'].append(pos)
		p['concepts'].sort(key=lambda c: c['i'])
		p['text'] = nps[1]
		out.append(p)
	return out

def third_pass(paragraphs):
	out = []
	temp = paragraphs[0]
	for i in range(1,len(paragraphs)):
		if paragraphs[i]['speaker'] == temp['speaker']:
			temp['text'] = temp['text'] + " " + paragraphs[i]['text']
		else:
			out.append(temp.copy())
			temp = paragraphs[i]
	out.append(temp.copy())
	return out

def second_pass(paragraphs):
	out = []
	temp = {}
	if (paragraphs[0]['speaker'] == 'null'):
		paragraphs[0]['speaker'] = "Bill O'Reilly"
		out.append(paragraphs[0])
	for i in range(1,len(paragraphs)):
		if (paragraphs[i]['speaker'] == 'null'):
			paragraphs[i]['speaker'] = paragraphs[i-1]['speaker']
		out.append(paragraphs[i])
	return out

# Returns ...
def first_pass(lines):
	out = []
	for line in lines:
		line = line.strip()
		obj = {}
		m = regex.match(line)
		if (m):
			if m.group(1).isupper():
				obj['speaker'] = m.group(1)
				obj['text'] = m.group(3)
			else:
				obj['speaker'] = "null"
				obj['text'] = line
		elif line=="(CROSSTALK)":
			obj['speaker'] = "Meta"
			obj['text'] = line
		elif line=="(LAUGHTER)":
			obj['speaker'] = "Meta"
			obj['text'] = line
		elif line=="(BEGIN VIDEO CLIP)":
			obj['speaker'] = "Meta"
			obj['text'] = line
		elif line=="(END VIDEO CLIP)":
			obj['speaker'] = "Meta"
			obj['text'] = line
		else:
			obj['speaker'] = "null"
			obj['text'] = line
		out.append(obj)
	return out

def parsemeta(lines):
	## Meta is in the form of:
	# title : XXX
	# keywords : Transcript,Talking Points
	# date : 2003-01-03
	# summary : To watch The Talking Points Memo click here.
	title = lines[0][7:].strip()
	kw = lines[1][10:].strip()
	date = lines[2][6:].replace('-','/').strip()
	summary = lines[3][9:].strip()

	return (kw,date,summary,title)

def text_summary(paragraphs):
	concepts = {}
	speakers = set()
	for p in paragraphs:
		for c in p['concepts']:
			if c['concept'] not in concepts:
				concepts[c['concept']] = c['s']
			else:
				concepts[c['concept']] += c['s']
		speakers.add(p['speaker'])

	return(concepts,list(speakers))


summary_all = []

for file in os.listdir(pagedir):
	if file.endswith(".txt"):
		print('Chunking ' + file + " into paragraphs and idenifying speakers")
		inpt = open(pagedir + file)
		fp = first_pass(inpt.readlines())
		sp = second_pass(fp)
		tp = third_pass(sp)
		xp = text_pass(tp)
		# np = np_pass(xp)

		# with open(metadir + file) as meta:
		# 	m = parsemeta(meta.readlines())

		with open(file, 'w+') as out:
			json.dump({"paragraphs":xp},out)
		out.close()
			# summary = text_summary(xp)
			# stout = {
			# 	'filename':file,
			# 	'keywords':m[0].split(','),
			# 	'date':m[1],
			# 	'summary':m[2],
			# 	'speakers':summary[1],
			# 	'concepts':summary[0],
			# 	'title':m[3]
			# }
			# summary_all.append(stout)

# with open('summary.json','w+') as sumout:
# 	for s in summary_all:
# 		out.write("\n")
# 		json.dump(s,sumout)

# def tag_page(f):
# 	file = open(pagedir + f)
# 	out = open(outdir + f,"w+")
# 	for line in file:
# 		lines = sent_detector.tokenize(line.strip())
# 		for l in lines:
# 			# text = nltk.word_tokenize(line)
# 			# tagged = nltk.pos_tag(text)
# 			out.write(l + "\n")
# 	out.close()
# 	file.close()