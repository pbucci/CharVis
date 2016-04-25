# Author: Paul Bucci
import requests
with open('resolved_duplicates_transcript_links.txt') as f:
	links = [x.strip() for x in f.readlines()]


print("There are " + str(len(links)) + " to parse here today.")
count = 0
for link in links:
	if link[-1] == '/':
		link = link[:-1]
	count += 1
	print("[" + str(count) + "] Getting " + link)
	
	sp = link.split('/')
	uri = '-'.join([sp[-4],sp[-3],sp[-2],sp[-1]])
	out = open('./pages/' + uri + '.txt', 'w+')
	
	page = requests.get(link)
	out.write(page.content)
	
	out.close()
	
	print("Done.\n")