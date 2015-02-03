import urllib
import httplib
import sqlite3
import sys
import os

__version__ = "1.2"

__help__ = """
Usage:
Add links to start the crawler database
python MouCrawler.py database_name.db -a http://link.com

Start crawling
python MouCrawler.py database_name.db -c
"""

def get_content(info):
	content = info.getheaders("Content-Type")
	if (content):
		return content[0].split("/")[0]
	return ""


def get_links(link):
		'''This function load a page and return a set with
		all external links into it'''
		
		try:
			url = urllib.urlopen(link)
			page = url.read()
		except (IOError, httplib.InvalidURL, httplib.LineTooLong, TypeError):
			return set()
		
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


class Crawler:
	def __init__(self, database="Crawler database.db"):
		self.id = 1.0
		self.database = sqlite3.connect(database)
		self.cursor = self.database.cursor()
		
		try:
			self.cursor.execute("CREATE TABLE links (link text, type text, crawled real, id real)")
		except (sqlite3.OperationalError):
			pass
		self.database.commit()
		
	def add_link(self, link):
		id = self.cursor.execute('SELECT max(id) FROM links').fetchone()[0]
		
		if (id == None):
			id = 1.0
		else:
			id += 1.0
		
		self.cursor.execute("INSERT INTO links VALUES ('%s', 'text', 0, %d)" % (link, id))
		self.database.commit()
	
	def crawl(self):
		row = self.cursor.execute('SELECT * FROM links WHERE crawled=0 AND type="text" ORDER BY id').fetchone()
		url = row[0]#it means there is nothing to crawl in database, use -a to add link to it
		self.id = row[3]
		self.cursor.execute("UPDATE links SET crawled=1 WHERE id="+str(self.id))
		
		try:
			print("[*] Crawling "+url)
		except (UnicodeEncodeError):
			pass
		links = []
		try:
			links = list(get_links(url))
		except:
			print("Error")
		self.database.commit()

		
		for link in links:
			try:
				exist = self.cursor.execute("SELECT * FROM links WHERE link='%s'" % link).fetchall()
				if len(exist):
					pass
				else:
					content = get_content(urllib.urlopen(link).info())#slow down the link add
					#but at least you know if its a video, image, or text
					#content = "text"
					self.id =self.cursor.execute('SELECT max(id) FROM links').fetchone()[0]+1.0
					self.cursor.execute("INSERT INTO links VALUES ('%s', '%s', %d, %d)" % (link,content,0,self.id))
				self.database.commit()
				print(str(self.id)+"\t"+link)
			except (KeyboardInterrupt):
				print("[*] Keyboard Interrupt")
				self.database.close()
				sys.exit(0)
			except (IOError, UnicodeEncodeError, sqlite3.OperationalError):
				pass
		
		
		self.crawl()
		return 0


if (__name__ == "__main__"):
	try:
		c = Crawler(sys.argv[1])
		if (sys.argv[2]=="-a"):
			c.add_link(sys.argv[3])
		elif (sys.argv[2] == "-c"):
			c.crawl()
	except (IndexError):
		print(__help__)
	
	
