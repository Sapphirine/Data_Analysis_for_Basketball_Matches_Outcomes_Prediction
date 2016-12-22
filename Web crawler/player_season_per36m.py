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
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "  
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "  
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

# create a list that save the player name and its website
def ofile_writer(name, data_writer):
	ofile  = open(name, "wb")

	writer = csv.writer(ofile, delimiter=',')
	for each in data_writer:
		writer.writerow(each)

	ofile.close()

def player_history_information(url):

	file_name = url[11:(len(url)-5)]
	
	print file_name
	file_name = 'player_history_season_per36m/' + file_name + '.csv'

	url = prefix + url 
	time.sleep(1)

	headers = {'user-agent': user_agent_list[random.randint(0,17)]}
	try:
		html = requests.get(url,headers=headers)
	except requests.exceptions.HTTPError as err:
		print err	
	# testing
	#print html.text
	soup = BeautifulSoup(html.text, "html.parser")

	table = soup.find('table', id='per_minute')
	print table
	if table == None:
		table = soup.find('table',id='per_minute_clone')

	dataset = []

	if table:
		n = 0
		for item in table.tbody.children:

			if n % 2 == 0 and item.find('a')!=None:
				#print item
				# item
				player_season = []
				i = 0
				label = 0
				for each in item:
					#print each
					try:
						if i == 0:
							player_season.append(each.string)
							player_season.append(each.a['href'])
						
						else:
							player_season.append(each.string)

					except AttributeError as err:
						print err
						label = 1

					i = i + 1
				#print player_season
				if label==0:
					dataset.append(player_season)

			n = n + 1

	ofile_writer(file_name, dataset)


def collect_players_history_information():
	# os.mkdir('player_history_season_per36m')
	# file in 
	ifile = open('all_player_info.csv', 'rb')
	reader = csv.reader(ifile)
	url_list = []

	for row in reader:
		url_list.append(row[1])
	ifile.close()
	
	n = 1
	n0 = 0
	for url in url_list:
		print n
		if n>=n0:
			player_history_information(url)
		n = n + 1
		break

def main():
	collect_players_history_information()
	#create_players_list()

if __name__=='__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	main()