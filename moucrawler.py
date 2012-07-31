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

class moucrawl:
	def __init__(self):
		'''The tiny web crawler'''
		self.links = []
		self.crawled = []
		self.requests_done = 0
		
	def __len__(self):
		return(len(self.all_links()))
	
	def all_links(self):
		'''This function return all found links and delete doubles before'''
		return(list(set(self.links)))
	
	def crawl(self, link):
		'''Basic crawler recursive function'''
		for url in self.get_links(link):
			if (url not in self.crawled):
				self.crawl(url)
				self.crawled.append(url)
	
	def get_links(self, link, display=True):
		'''This function load a page and return all external links into it
		its also add links to the list of links accessible with self.all_links()'''
		try:
			page = urlopen(link).read()
			self.requests_done += 1
		except(IOError):
			return([])
		links = []
		protocols = ["http://", "https://"]
		items = page.split('"') + page.split("'")#separing with quotes to find links faster
		for item in items:
			for protocol in protocols:
				try:
					if (protocol in item[:len(protocol)]):
						links.append(item)
				except(IndexError):
					pass
		self.links.extend(links)
		if (display):
			stdout.write("\rFound %i urls %i requests done." % (len(self), self.requests_done))
			stdout.flush()
		return(list(set(links)))

def main():
	'''Example of moucrawler'''
	print("CTRL+C to quit")
	crawler = moucrawl()
	try:
		crawler.crawl(raw_input("start searching with this link: "))
	except(KeyboardInterrupt):
		print("[*] Keyboard Interrupt!")
	print("found %s links" % len(crawler))
	with open("links.html", "a") as file:
		file.write("\n%s" % "\n\n".join(crawler.all_links()))

if __name__ == "__main__":
	main()
