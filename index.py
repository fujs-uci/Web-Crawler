
import os
import json
from pprint import pprint
import re
from collections import Counter, defaultdict
import pickle
from bs4 import BeautifulSoup





index = defaultdict(list) #list of index




def get_words():
	path = "WEBPAGES_CLEAN"
	file = ""
	#gets all directory in WEBPAGES_CLEAN
	direct = [f for f in os.listdir(path) if os.path.isdir(path+"/"+f)]
	#iterate through each docu
	for directory in direct:
		file ="/"+directory
		#gets the all files in the directory
		files = [f for f in os.listdir(path+file)]
		for filename in files:
			temp_file = file + "/" + filename
			#this opens the file 
			with open(path+temp_file) as website:
				print("----"+path+temp_file+"------")
				all_words = list()
				header_and_bolded = set()
				title = list()
				word_in_title = ""
				html = website.read();
				#check if theres a title
				if('<title>' in html and '</title>' in html):
					word_in_title = html[html.index('<title>'):html.index('</title>')]
				elif('<title>' in html and '<body>' in html):
					word_in_title = html[html.index('<title>')+7:html.index('<body>')]
				elif('<body>' in html):
					word_in_title = html[:html.index('<body>')]
			    #get each word of the title 
				title = re.findall(r'[a-zA-Z]+',word_in_title)

				#need to get header and bolded words
				soup = BeautifulSoup(html)

				#finds bolded words and headers
				for bolded in soup.find_all('b'):
					header_and_bolded.add(bolded)

				for header1 in soup.find_all('h1'):
					header_and_bolded.add(header1)

				for header2 in soup.find_all('h2'):
					header_and_bolded.add(header2)

				for header3 in soup.find_all('h3'):
					header_and_bolded.add(header3)


				#print(header_and_bolded)
				all_words = re.findall(r"[a-zA-Z]+",html)
				#lowercase all the words 
				all_words = [x.lower() for x in all_words] #only if not case sensitive
				#create a list of (word, count)
				word_dict = Counter(all_words)
				#create a dict of index
				index_words(temp_file[1:], word_dict, title, header_and_bolded)
	print("finish indexing")
				


def index_words(path,word_dict, title, handb):
	global index
	#makes a dictionary of all index
	for key, values in word_dict.items():
		#its a key is in the title
		if(key in title):
			index[key].append((path,values, 3))
		#header or bolded
		elif(key in handb):
			index[key].append((path,values, 2))
		#basic body text
		else:
			index[key].append((path,values, 1))

	

def save_dict():
	global index
	#saves the dict to file
	with open('indexed_words.json', 'w') as outfile:
		json.dump(index, outfile)
	print("saving dictionary to file")










if __name__ == '__main__':
	get_words()
	save_dict()














