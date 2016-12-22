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

#create files that contains the players' page and name
#no player's first character is 'x'
# def create_players_list():

# 	players_alphabet_list = []
# 	for character in range(97,123):
# 		if chr(character)!='x':
# 			new_string = 'http://www.basketball-reference.com/players/' + chr(character) + '/'
# 			players_alphabet_list.append(new_string)

# 	data_writer = []
# 	for character in range(0,25):

# 		url = players_alphabet_list[character]
# 		headers = {'user-agent': user_agent_list[random.randint(0,17)]}
# 		try:
# 			html = requests.get(url,headers=headers)
# 		except requests.exceptions.HTTPError as err:
# 			print err
		
# 		soup = BeautifulSoup(html.text,"html.parser")
# 		table = soup.find('table', id='players')

# 		if table == None:
# 			print 0
# 			try:
# 				html = requests.get(url,headers=headers)
# 			except requests.exceptions.HTTPError as err:
# 				print err
		
# 			soup = BeautifulSoup(html.text,"html.parser")
# 			table = soup.find('table', id='players')

# 		n = 0
# 		for item in table.tbody.children:
# 			if n%2 == 0:
# 				player_info = []
# 				i = 0
# 				for each in item:
# 					if i == 0:
# 						player_info.append(each.string)
# 						player_info.append(each.a['href'])
# 					elif i in range(1,4):
# 						player_info.append(each.string)
# 					else:
# 						break
# 					i = i + 1
# 				data_writer.append(player_info)

# 			n = n + 1
# 		print n/2, chr(character+97)
# 	ofile_writer('all_player_info.csv', data_writer)

def player_history_information(url):

	file_name = url[11:(len(url)-5)]
	print file_name
	file_name = 'player_history_season/' + file_name + '.csv'

	url = prefix + url 
	time.sleep(1)

	headers = {'user-agent': user_agent_list[random.randint(0,17)]}
	try:
		html = requests.get(url,headers=headers)
	except requests.exceptions.HTTPError as err:
		print err	
	# testing
	soup = BeautifulSoup(html.text, "html.parser")
	table = soup.find('table', id='per_game')
		
	dataset = []
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
	#print dataset

	# pre_url = prefix +'/players/a/abdelal01/gamelog/0000/'
	
	# data_writer = []
	# for website in dataset:

	# 	url = prefix + website[1]
	# 	if pre_url != url:
	# 		pre_url = url
	# 		time.sleep(random.uniform(1,3))
	# 		headers = {'user-agent': user_agent_list[random.randint(0,17)]}
	# 		try:
	# 			html = requests.get(url,headers=headers)
	# 		except requests.exceptions.HTTPError as err:
	# 			print err

	# 		soup = BeautifulSoup(html.text, "html.parser")
	# 		table = soup.find('table', id='pgl_basic')

	# 		if table:
	# 			player_info = []
				
	# 			n = 1	
	# 			hold_on = 0		
	# 			for item in table.tbody.children:
					
	# 				if n%21 != 0:
	# 					player_season = []
	# 					label = 0
	# 					for each in item:
							
	# 						try:
	# 							player_season.append(each.string)
	# 						except AttributeError as err:	
	# 							label = 1	
	# 							hold_on = 1					
	# 							print err
	# 							sys.exit(n)
	# 							break

	# 					if label == 0:
	# 						data_writer.append(player_season)
	# 				n = n + 1

	# file_name = 'all_player_per_match/' + file_name + '.csv'

	# ofile_writer(file_name, data_writer)

def collect_players_history_information():
	#os.mkdir('player_history_season')
	# file in 
	ifile = open('all_player_info.csv', 'rb')
	reader = csv.reader(ifile)
	url_list = []

	for row in reader:
		url_list.append(row[1])
	ifile.close()
	
	n = 1
	n0 = 157
	for url in url_list:
		#print n
		if n>=n0:
			print n
			player_history_information(url)
		n = n + 1

def main():
	collect_players_history_information()
	#create_players_list()

if __name__=='__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	main()


