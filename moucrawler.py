#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  moucrawler.py
#  
#  Copyright 2012 Arnaud Alies <arnaudalies.py@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from urllib import urlopen
from sys import stdout

class MouCrawler:
	def __init__(self):
		'''The tiny web crawler'''
		self.links = []
		self.tested = []

	def __len__(self):
		return(len(self.all_links()))
	
	def reOrder(self):
		'''Delete duplicate links'''
		self.links = list(set(self.links))
	
	def all_links(self):
		'''This function return all found links and delete doubles before'''
		self.reOrder()
		return(self.links)
	
	def Crawl(self, link):
		'''Basic crawler recursive function'''
		for url in self.get_links(link):
			self.Crawl(url)
	
	def get_links(self, link, display=True):
		'''This function load a page and return all external links into it
		its also add links to the list of links accessible with self.all_links()'''
		if (link in self.tested):
			return([])
		self.tested.append(link)
		try:
			page = urlopen(link).read()
		except(IOError):
			return([])
		domain = "http://%s" % link.split("/")[2]
		links = []
		beginnings = ["http://", "https://", "/"]
		items = page.split('"') + page.split("'")
		for item in items:
			for begin in beginnings:
				try:
					if (begin in item[:len(begin)]):
						if (begin == "/"):
							url = domain + item
						else:
							url = item
						if ("/>" in url):
							url = url[:url.find("/>")+1]
						links.append(url)
				except(IndexError):
					pass
		links = list(set(links))
		self.links.extend(links)
		if (display):
			stdout.write("\rFound %i urls %i requests done." % (len(self), len(self.tested)))
			stdout.flush()
		return(links)

def main():
	'''Example of moucrawler'''
	crawler = MouCrawler()
	try:
		crawler.Crawl(raw_input("start crawler link (do not forget the 'http://'\n: "))
	except(KeyboardInterrupt):
		print("\nKeyboard Interrupt")
	html_page = '<title>Sites Found</title>'
	for link in crawler.all_links():
		html_page += '</br ><a href="%s" target=_blanc>%s</a>\n' % (link, link)
	with open("links.html", "w") as file:
		file.write(html_page)
	

if __name__ == "__main__":
	main()
