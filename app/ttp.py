import json
k = open('summary.json')
# print(k.readlines()[0])
p = json.load(k)

cps = {}
for date in p:
  for c in date['concepts']:
    if c in cps:
      cps[c] += 1
    else:
      cps[c] = 1

delete = set()
for k,v in cps.items():
  if v == 1:
    delete.add(k)

for date in p:
  for c in delete:
    if c in date['concepts']:
      del date['concepts'][c]
      
with open("summary_reduce.json","w+") as outfile:
  json.dump(p,outfile)
