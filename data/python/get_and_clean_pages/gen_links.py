# Author: Paul Bucci

## build_url(string,string,string)
# Returns list of strings
# start : string representing a start date
# end   : string representing an end date
# page  : string representing a page number
def build_url(start_datestring,end_datestring,page_numstring):
	base_url = "http://www.foxnews.com/shows/the-oreilly-factor/transcripts.html#"

	start = "st=" + start_datestring
	page = "si=" + page_numstring
	end = "ed=" + end_datestring
	url = base_url + start + "&" + page + "&" + end

	return url

# Makes all digits two characters long
def my_str(x):
	ret = str(x)
	if (len(ret) == 1):
		ret = "0" + ret
	return ret

outlist = [4,6,9,11]
def gen_dates(first_year,last_year):
	ret = []
	for i in range(first_year,last_year):
		for j in range(1,13):
			for k in range(1,32):
				if ((k == 31) and (j in outlist)) or ((k > 28) and (j == 2)):
					pass
				else:
					ret.append(("-".join( (my_str(x) for x in [i,j,k]) )))
	return ret

def gen_links(s,e):
	dates = gen_dates(s,e)
	links = []
	for i in range(1,len(dates),1):
		links.append(build_url(dates[i-1],dates[i],"0"))
	return links


linx = gen_links(2010,2011)
f = open('new_links.txt',"w+")
for l in linx:
	f.write(l + "\n")
f.close()