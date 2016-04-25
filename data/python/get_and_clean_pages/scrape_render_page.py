# NOT authored by Paul Bucci, all code from http://stackoverflow.com/questions/34603886/pyqt4-loop-main-render-class

import sys  
import asyncio
import time
import sys
from lxml import html
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage



class Render(QWebPage):
  def __init__(self, cb):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.cb = cb

  def crawl(self, url):
    print('Downloading', url)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    frame = self.mainFrame()
    url = str(frame.url().toString())
    html = frame.toHtml()
    self.cb(url, html)
    self.app.quit()


def scrape(url, result):
	#Next build lxml tree from formatted_result
	tree = html.fromstring(result)
	transcripts = []
	#Now using correct Xpath we are fetching URL of archives
	archive_links = tree.xpath('//h3[@class="title"]/a/@href')
	
	print("##############################")	
	print("                              ")
	print(archive_links)
	print("                              ")
	print("##############################")

	linxout = open("linxout.txt","a")

	for a in archive_links:
		linxout.write(a + "\n")
		if (len(archive_links) > 9):
			linxout.write("check here paul\n")
	return True

r = Render(cb=scrape)
lines = []
with open('links.txt') as listoflinks:
	lines = listoflinks.readlines()
	r.crawl(lines[0].strip())

listoflinks.close()

out = open('links.txt','w+')
for l in lines[1:]:
	out.write(l)