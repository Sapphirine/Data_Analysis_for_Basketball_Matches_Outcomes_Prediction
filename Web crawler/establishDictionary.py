#!/usr/bin/python -tt
import requests
import re
import csv
from bs4 import BeautifulSoup
import os

prefix = 'http://www.basketball-reference.com'

# create a list that save the player name and its website
def ofile_writer(name, data_writer):
	ofile  = open(name, "wb")
	writer = csv.writer(ofile, delimiter=',')
	for each in data_writer:
		writer.writerow(each)
	ofile.close()

#create files that contains the players' page and name
def create_players_list():
	players_alphabet_list = []
	for character in range(97,123):
		new_string = 'http://www.basketball-reference.com/players/' + chr(character) + '/'
		players_alphabet_list.append(new_string)

	player_list = {}
	data_writer = []
	
	for i in range(0,26):
		url = players_alphabet_list[i]
		try:
			html = requests.get(url)
		except requests.exceptions.HTTPError as err:
			print err
		player_info = re.findall('<strong><a href="(.*?)">(.*?)</a>', html.text, re.S)
		for each in player_info:
			data_writer.append(each)

	ofile  = open('player_info.csv', "wb")
	writer = csv.writer(ofile, delimiter=',')
	for each in data_writer:
		writer.writerow(each)
	ofile.close()

#create the team_page info and team name
def create_team_pages():
	url = 'http://www.basketball-reference.com/teams/'
	try:
		html = requests.get(url)
	except requests.exceptions.HTTPError as err:
		print err
		print 'unable to access http://www.basketball-reference.com/teams/'

	teampage_list = []
	soup = BeautifulSoup(html.text,"html.parser")
	#team_page = <th scope="row" class="left" data-stat="franch_name">
	#<a href="/teams/ATL/">Atlanta Hawks</a></th>
	teampage_th = soup.find_all('th', scope='row', class_='left')
	for each in teampage_th:
		website = prefix + each.a['href']
		team_name = each.string
		teampage_list.append([website,team_name])	
	ofile_writer('teampage_info.csv', teampage_list)

#single team members in a year
def single_team_homepage(homepage):
	url = homepage
	ofile_name = url[42:(len(url)-10)] + '.csv'
	try:
		html = requests.get(url)
	except requests.exceptions.HTTPError as err:
		print err
		print 'uable to access' + homepage
	soup = BeautifulSoup(html.text,"html.parser")
	#print soup.prettify()
	#find the table id = "roster"
	tables = soup.find('table', id = "roster")
	team_member = []
	team_member.append(['player website','Player','Pos','Ht','Wt','Birth Date','Country','Exp','College'])

	for child_tr in tables.tbody.children:
		n = 0
		child_info = []
		for child in child_tr:
			if n == 1:
				website = prefix + child.a['href']
				player_name = child.string
				child_info.append(website)
				child_info.append(player_name)
			if n > 1:
				child_info.append(child.string)
			n = n + 1
		team_member.append(child_info)
	ofile_writer(ofile_name, team_member)

#allocate single team 
def every_team_homepage():
	year = '2017'
	os.mkdir(year)

#file reader


#create_players_list()
#create_team_pages()
#single_team_homepage()
every_team_homepage()
