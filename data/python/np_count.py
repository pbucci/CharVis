# Author: Paul Bucci
import operator
import os
# don't forget trailing slash
dir = '../pos_chunker/chunked/'

def prettify(s):
	st = str(s)
	ret = st + (" "*(5 - len(st))) + "\t"
	return ret

nps = {}
def count_nps(file,dir):
	print('Counting ' + file)
	with open(dir + file) as f:
		lines = [x.strip() for x in f.readlines()]
	for line in lines:
		if line[0:3] == "(NP":
			if line not in nps:
				nps[line] = 1
			else:
				nps[line] += 1

for file in os.listdir(dir):
        if file.endswith(".txt"):
            count_nps(file,dir)

sorted_nps = sorted(nps.items(), key=operator.itemgetter(1))

out = open('count_summaries.txt', 'w+')
for np in sorted_nps:
	x = np[0].strip().replace('(NP (NBAR ','').replace('))','').replace('/NNPS','').replace('/NNP','').replace('/NNS','').replace('/NN','').replace('/JJ','')
	out.write(prettify(np[1]) + x +  '\n')