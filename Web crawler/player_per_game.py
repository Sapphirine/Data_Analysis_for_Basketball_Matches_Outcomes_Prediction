#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import requests
import re
import csv
from bs4 import BeautifulSoup
import os
import time
import random
import sys

prefix = 'http://www.basketball-reference.com'

user_agent_list = [ 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "  
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",  
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "  
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "  
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "  
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "  
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "  
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "  
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5" ]

# create a list that save the player name and its website
def ofile_writer(name, data_writer):
	ofile  = open(name, "wb")

	writer = csv.writer(ofile, delimiter=',')
	for each in data_writer:
		writer.writerow(each)

	ofile.close()

#create files that contains the players' page and name
def player_history_information(name):
	file_reader = 'player_history_season/' + name + '.csv'
	file_name = 'player_history_per_match/' + name + '.csv'

	ifile = open(file_reader, 'rb')	
	reader = csv.reader(ifile)
	url_list = [ prefix + row[1] for row in reader]

	# for row in reader:
	# 	url_list.append(prefix + row[1])
	ifile.close()
	data_writer = []
	pre_url = prefix +'/players/a/abdelal01/gamelog/0000/'
	for url in url_list:
		if url != pre_url:
			pre_url = url
			headers = {'user-agent': user_agent_list[random.randint(0,17)]}

			try:
				html = requests.get(url,headers=headers)
				text = re.findall('<div class="overthrow table_container" id="div_pgl_basic">(.*?)</div>', html.text, re.S)
				if text:
					soup = BeautifulSoup(text[0], "html.parser")
					table = soup.find('table', id='pgl_basic')

					if table:	
						n = 1				
						for item in table.tbody.children:
							if item:
								if n%21 != 0:	
									label = 0					
									player_match = []
									for each in item:	
										if each:							
											try:
												player_match.append(each.string)
											except AttributeError as err:					
												print err
												label = 1
												n = n - 1
												break
									if label == 0:
										data_writer.append(player_match)
								n = n + 1

			except requests.exceptions.HTTPError as err:
				print err
	ofile_writer(file_name, data_writer)

def collect_players_history_information(n0):
	# file in 
	ifile = open('all_player_info.csv', 'rb')
	reader = csv.reader(ifile)
	name_list = []
	#os.mkdir('player_history_per_match')

	for row in reader:
		url = row[1]
		name = url[11:(len(url)-5)]
		name_list.append(name)

	ifile.close()
	
	for i in range(n0,n0+10):
		#print n
		print i+1, name_list[i]
		player_history_information(name_list[i])

def main():
	n0 = int(sys.argv[1])
	collect_players_history_information(n0)

#create_players_list()
if __name__=='__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	main()