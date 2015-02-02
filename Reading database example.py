#This script is an example f what you can do once you have a database
import sqlite3
import hashlib
from sys import stdout
from time import time
from urllib import urlretrieve
from os import getcwd, path
import random

class download:
	def __init__(self, link, file_name='', checksum='md5'):
		'''Download a file, you must catch errors yourself'''
		'''Just a class to download files using urllib'''
		self.checksum = checksum.lower()
		self.file_name = file_name
		self.link = link
		if (self.checksum not in ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']):
			self.checksum = 'md5'
		if (self.file_name == ''):
			if ("/" in self.link):
				self.file_name = str(random.randint(0,100000))+self.link.split("/")[len(self.link.split("/"))-1]
			else:
				self.file_name = link
		self.get()

	@staticmethod
	def GetFileHash(file_name, encryption):
		'''Returns the hash of one file
		this is the long fonction , you can also simply do urllib.urlretrieve(link, name, hook)'''
		return getattr(hashlib, encryption)(open(file_name).read(path.getsize(file_name))).hexdigest()

	
	def hook(self, *data):
		self.file_size = int(data[2]/1000)
		total_packets = data[2]/data[1]
		downloaded_packets = data[0]
		stdout.write("\rDownload size\t= %i ko, packet: %i/%i" % (self.file_size, downloaded_packets, total_packets+1))
		stdout.flush()

	def get(self):
		'''Download a file from web with showing progression and hash'''
		timer = time()
		urlretrieve(self.link, self.file_name, self.hook)
		print("\nFile name\t= %s\nETA\t\t= %i second(s)\n%s checksum\t= %s\nFile size\t= %i kb\nSaved in: %s" %
		(self.file_name, int(time()-timer), self.checksum, self.GetFileHash(self.file_name, self.checksum), self.file_size, getcwd()))
		return [self.file_name, int(timer-time()), self.file_size,self.checksum, self.GetFileHash(self.file_name, self.checksum)]

db = sqlite3.connect("Crawler database.db")

c = db.cursor()

for x in c.execute('SELECT * FROM links WHERE type="image" ORDER BY id'):
	try:
		download(x[0])
	except:
		pass

db.close()
