# Author: Paul Bucci
with open('linxout_r.txt') as ff:
	f = [x.strip() for x in ff.readlines()]
out = open('resolved_link_duplicates.txt','w+')
lines = []
duplicates = 0
for line in f:
	if line not in lines:
		lines.append(line)
		out.write(line + "\n")
	else:
		duplicates += 1
ff.close()
out.close()
print(duplicates)