# Author: Paul Bucci

import os
import re
from html.parser import HTMLParser
parser = HTMLParser()
pagedir = "./pages/"

stopphrases = ["O'Reilly Factor, hosted by Bill O'Reilly, airs on Weekdays at 8PM ET on Fox News Channel.",
				"ALL RIGHTS RESERVED",
				'that has been edited for clarity',
				"All materials herein are protected by United States copyright law and may not be reproduced, distributed, transmitted, displayed, published or broadcast",
				"This is a RUSH transcript from",
				'Watch "The O\'Reilly Factor" weeknights']


def stopphrases_scrub(l):
	for s in stopphrases:
		if s in l:
			return "\n"
	return l

# Select a single item from a list
def select(l,s):
	for item in l:
		if s in item:
			ret = item.replace(s,'')
			return ret

def trans_out(lines,uri):
	out = open('./transcripts/' + uri, 'w+')
	for l in lines:
		out.write(l.strip() + "\n")
	out.close()

def meta_out(meta,uri):
	out = open('./meta/' + uri, 'w+')
	# meta = {'keywords':keywords,'date':date,'title':title,'summary':summary,'speakers':speakers}
	out.write('title : ' + meta['title'] + '\n')
	out.write('keywords : ' + meta['keywords'] + '\n')
	out.write('date : ' + meta['date'] + '\n')
	out.write('summary : ' + meta['summary'] + '\n')
	out.close()

# Parse the page
# uri is string
def parse_page(uri):
	with open(pagedir + uri) as p:
		original_page = [x.strip() for x in p.readlines()]
	if original_page[1] == "An error occurred while processing your request.<p>":
		print('Skipping ' + uri)
		return False
	else:
		transcript_only = [parser.unescape(x) for x in original_page if x != "" and x[0:3] == "<p>"]
		regex_html_scrub = [re.sub(r'<.*?>','',string).strip() for string in transcript_only]

		stopphrases_scrubbed = [stopphrases_scrub(x) for x in regex_html_scrub]

		meta_only = [parser.unescape(x.replace('<meta name="dc.','').replace('" content="',': ').replace('">','')) for x in original_page if '<meta name="dc.' in x]
		
		keywords = ','.join([x.strip() for x in select(meta_only,'subject: ').split(',')])
		date = select(meta_only,'date:').strip()
		title = select(meta_only,'title:').strip()
		summary = select(meta_only,'description:').strip()

		# Transcript
		meta = {'keywords':keywords,'date':date,'title':title,'summary':summary}
		trans_out(stopphrases_scrubbed,uri)
		meta_out(meta,uri)

for file in os.listdir(pagedir):
    if file.endswith(".txt"):
        parse_page(file)