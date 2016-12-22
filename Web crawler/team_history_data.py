#!/usr/bin/python -tt
import requests
import re
import csv
from bs4 import BeautifulSoup
import os

prefix = 'http://www.basketball-reference.com'

def ofile_writer(name, data_writer):
	ofile  = open(name, "wb")
	writer = csv.writer(ofile, delimiter=',')
	for each in data_writer:
		writer.writerow(each)
	ofile.close()

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
			print child
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

# create a list that save the player name and its website
def teams_member_of_years():
	
	ifile = open('teampage_info.csv', 'rb')
	reader = csv.reader(ifile)
	team_list ＝ { row[1]:row[0] for row in reader} #row[0]
	ifile.close()

	for key in team_list:
		print key   #test

		url = team_list[key]
		try:
			html = requests.get(url)
		except requests.exceptions.HTTPError as err:
			print err
			print 'uable to access' + url
		soup = BeautifulSoup(html.text,"html.parser")
		tables = soup.find('table')
		
		dataset = []
		i = 0
		for child_tr in tables.tbody.children:
			if i%2 == 0:
				n = 0
				child_info = []

				child_info.append(prefix + child_tr.th.a['href'])

				for child in child_tr:
			 	# 	print child
					# if n in range(3,9):
					# 	child_info.append(child.string)
					# n = n + 1
					child_info.append(child.string)
				dataset.append(child_info)
			i = i + 1
		ofile_writer('teams_page/'+ key +'.csv', dataset)

teams_member_of_years()
