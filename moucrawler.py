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
__version__ = 5.1
__doc__ = """
MouCrawler

A python web crawler based on
the principe if http or / is after a quote
should be a link
"""

import httplib
import random
from urllib import urlopen, urlretrieve
from sys import stdout
from os import fsync, rename, remove, mkdir

class crawler:
	def __init__(self,Display=True):
		self.tested = set()
		self.links = set()
		self.display = Display
		self.file_name = "links_"+str(random.randint(1,1000))+".txt"
	
	def __len__(self):
		return len(self.links)
	
	
	def all_links(self):
		"""return all links found"""
		return list(self.links)
	
	def crawl(self, link):
		'''Main crawler recursive function'''
		if (link not in self.tested):
			self.tested.add(link)
			try:
				new_links = self.get_links(link)
			except (IOError, RuntimeError):
				pass
		
		f = open(self.file_name,"a")
		
		for url in set(new_links)-set(self.links):
			f.write("\n"+url)
		f.close()
		
		self.links = self.links.union(new_links)
		
		if (self.display):
			stdout.write("\rFound %i urls %i requests done." % (len(self), len(self.tested)))
			stdout.flush()
		
		try:
			self.crawl(list(self.links-self.tested)[0])
		except:
			print("\nRAM full...")

	
	def get_links(self, link):
		'''This function load a page and return all external links into it
		its also add links to the list of links accessible with self.all_links()
		raise an IOError if any errors'''
		
		try:
			page = urlopen(link).read()
		except (IOError, httplib.InvalidURL, httplib.LineTooLong, TypeError):
			return []
		links = set()
		new = ''
		domain = ("http://%s" % link.split("/")[2])
		page_items = (page.split('"') + page.split("'"))
		
		for potential_link in page_items:
			if (potential_link.startswith("http")):new = potential_link
			elif (potential_link.startswith("/")):new = domain + potential_link
			#begin cut and repair non html links
			if ("/>" in new):new = new[:new.find("/>")+1]
			if ("/*" in new):new = new[:new.find("/*")]
			if (new.count("//") >= 2):new = 'http://' + new.split("//")[2]
			#end cut and repair non html links
			links.add(new)
		
		return links

def save_links(links):
	print "\n"+links

def seekAndDownload(links, formats):
	'''Download all files from x formats
	example: seekAndDownload(list(crawler.all_links()), ["PNG", "MNG", "TIFF", "JPEG", "GIF", "TGA", "JPG", "RAW"])'''
	if not formats:
		return 0
	if ("*" in formats):
		path = "Crawler Downloads"
	else:
		path = "_".join(formats)
	try:
		mkdir(path)
	except:
		pass
	for link in links:
		for image_format in formats:
				if link.upper().endswith(".%s" % image_format.upper()) or "*" in formats:
					if ("/" in link):
						file_name = link.split("/")[len(link.split("/"))-1]
					else:
						file_name = link
					try:
						print("Downloading: %s" % link)
						urlretrieve(link, "%s//%s" % (path, file_name))
					except IOError:
						pass
	return 0

if (__name__ == "__main__"):
	c = crawler(True)
	print(c.crawl("http://www.google.com"))
