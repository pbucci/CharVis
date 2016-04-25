import os
import re
# import nltk
import random
import json
# import sentiment_mod as s
# from nltk.corpus import movie_reviews



from pprint import pprint

metadir = "../meta/"
outdir = "./out/"

for file in os.listdir('./'):
	if file.endswith(".txt"):
		with open(file) as f:
			ff = f.readlines()
			paragraphs = json.loads(ff[0])['paragraphs']
			speakers = set()
			max_speaker_length = -1
			for p in paragraphs:
				speakers.add(p['speaker'])
				if (len(p['speaker'].split()) > max_speaker_length):
					max_speaker_length = len(p['speaker'].split())
			resolved = set()
			for i in list(range(0,max_speaker_length)).reverse():
				for speaker in speakers:
					if len(speaker.split()) == i:
						for sw in speaker.split():
							if (sw in resolved):
								print(sw)
