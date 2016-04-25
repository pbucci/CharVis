import os
import re
# import nltk
import random
import json
# import sentiment_mod as s
# from nltk.corpus import movie_reviews



from pprint import pprint

metadir = "../meta/"

def text_summary(paragraphs):
	concepts = {}
	speakers = set()
	# print(paragraphs)
	for p in paragraphs:
		for c in p['concepts']:
			if c['concept'] not in concepts:
				concepts[c['concept']] = [c['s']]
			else:
				concepts[c['concept']].append(c['s'])
		speakers.add(p['speaker'])

	return(concepts,list(speakers))

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

summary_all = []

for file in os.listdir('./'):
	if file.endswith(".txt"):
		with open(file) as f:
			ff = f.readlines()
			paragraphs = json.loads(ff[0])['paragraphs']
			# summary_all.append(text_summary(paragraphs))

			
		with open(metadir + file) as meta:
			m = parsemeta(meta.readlines())
			summary = text_summary(paragraphs)
			stout = {
				'filename':file,
				'keywords':m[0].split(','),
				'date':m[1],
				'summary':m[2],
				'speakers':summary[1],
				'concepts':summary[0],
				'title':m[3]
			}
			summary_all.append(stout)

with open('summary.json','w+') as sumout:
	sumout.write("[")
	for s in summary_all:
		json.dump(s,sumout)
		sumout.write(",\n")
	sumout.write("]")