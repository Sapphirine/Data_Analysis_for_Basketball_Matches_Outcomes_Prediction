#!/usr/bin/python -tt

import requests
import re
import csv
from bs4 import BeautifulSoup
import os
from datetime import date, timedelta
import sys

prefix = 'http://www.basketball-reference.com'

def ofile_writer(name, data_writer):
	ofile  = open(name, "wb")
	writer = csv.writer(ofile, delimiter=',')
	for each in data_writer:
		writer.writerow(each)
	ofile.close()

def read_page_score(url, recordlist, date_time):
	try:
		html = requests.get(url)
		soup = BeautifulSoup(html.text,"html.parser")

		divs = soup.find_all('div',class_='game_summary expanded nohover')

		if divs:
			for div_per in divs:
				tables = div_per.find_all('table')
				if tables:

					new_record = [date_time]
					item = tables[0].tbody.find_all('tr')

					i = 0
					for each in item[0]:
						if i == 1:
							new_record.append(each.string)
							new_record.append(each.a['href'])
						if i == 3:
							new_record.append(each.string)
						i = i + 1
					
					i = 0
					for each in item[1]:
						if i == 1:
							new_record.append(each.string)
							new_record.append(each.a['href'])
						if i == 3:
							new_record.append(each.string)
						i = i + 1


					item = tables[1].tbody.find_all('td')
					
					for each in item:
						new_record.append(each.string)


					print (new_record)
					recordlist.append(new_record)

	except requests.exceptions.HTTPError as err:
		print (err, date_time)


def main():
	
	date_from_list = [ 
					   date(2000,1,1), date(2001,1,1), date(2002,1,1), date(2003,1,1),
					   date(2004,1,1), date(2005,1,1), date(2006,1,1), date(2007,1,1),
					   date(2008,1,1), date(2009,1,1), date(2010,1,1), date(2011,1,1),
					   date(2012,1,1), date(2013,1,1), date(2014,1,1), date(2015,1,1), 
					   date(2016,1,1), date(2016,9,12)
					   ]

	#os.mkdir('per_year_season')

	for i in range(6,10):
		date1 = date_from_list[i]
		date2 = date_from_list[i+1]

		file_name = 'per_year_season/year%d_%d.csv' % (date1.year, date2.year)
		score_list = []

		while (date1-date2) != timedelta(days=0):
			print (date2)
			if date2.month<7 or date2.month>9:
				url = ( 'http://www.basketball-reference.com/boxscores/index.cgi?month=%d&day=%d&year=%d' 
					% (date2.month, date2.day, date2.year))
				read_page_score(url, score_list, date2)
			date2 = date2 - timedelta(days=1)
		ofile_writer(file_name, score_list)
	
if __name__=='__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	main()



