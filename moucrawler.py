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

__author__ = "Arnaud Alies"
__version__ = 4.0
__doc__ = """
MouCrawler

A python web crawler based on
the principe if http or / is after a quote
should be a link
"""

from urllib import urlopen
from sys import stdout

class MouCrawler:
	def __init__(self, display=False):
		'''The tiny web crawler'''
		self.display = display
		self.links = set()
		self.tested = set()

	def __len__(self):
		return len(self.links)
	
	
	def all_links(self):
		"""return all links found"""
		return list(self.links)
	
	def crawl(self, link):
		'''Main crawler recursive function'''
		for url in self.get_links(link):
			self.crawl(url)
	
	def get_links(self, link):
		'''This function load a page and return all external links into it
		its also add links to the list of links accessible with self.all_links()'''
		if (link in self.tested):
			return []
		self.tested.add(link)
		try:
			page = urlopen(link).read()
		except IOError:
			return []
		links = set()
		domain = ("http://%s" % link.split("/")[2])
		page_items = (page.split('"') + page.split("'"))
		for potential_link in page_items:
			if (potential_link.startswith("http")):
				new = potential_link
			elif (potential_link.startswith("/")):
				new = domain + potential_link
			else:
				new = ''
			#begin cut and repair non html links
			if ("/>" in new):new = new[:new.find("/>")+1]
			if ("/*" in new):new = new[:new.find("/*")]
			if (new.count("//") >= 2):new = 'http://' + new.split("//")[2]
			#end cut and repair non html links
			links.add(new)
		self.links = self.links.union(links)
		if (self.display):
			stdout.write("\rFound %i urls %i requests done." % (len(self), len(self.tested)))
			stdout.flush()
		return list(links)

def main():
	'''Example of moucrawler'''
	crawler = MouCrawler(display=True)
	site = raw_input("start crawler link (do not forget the 'http://'\n: ")
	try:
		crawler.crawl(site)
	except(KeyboardInterrupt):
		print("\nKeyboard Interrupt")
	#writing out the page
	html_page = '<title>Sites Found</title>'
	for link in crawler.all_links():
		html_page += '</br ><a href="%s" target=_blanc>%s</a>\n' % (link, link)
	with open("links.html", "w") as file:
		file.write(html_page)
	

if __name__ == "__main__":
	main()
