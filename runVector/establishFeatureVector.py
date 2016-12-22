import csv
import sys
import os

#file writing function, imput a list list
def ofile_writer(name, data_writer):
	ofile  = open(name, "wb")
	writer = csv.writer(ofile, delimiter=',')
	for each in data_writer:
		writer.writerow(each)
	ofile.close()

#main function()
def main():
	fileList = [ '2008-2009.csv', '2009-2010.csv', '2010-2011.csv',
				  '2011-2012.csv', '2012-2013.csv', '2013-2014.csv',
				  '2014-2015.csv', '2015-2016.csv' ]
	leagueList = [ 'NBA_2008-2009.csv', 'NBA_2009-2010.csv', 'NBA_2010-2011.csv',
				   'NBA_2011-2012.csv', 'NBA_2012-2013.csv', 'NBA_2013-2014.csv',
				   'NBA_2014-2015.csv', 'NBA_2015-2016.csv' ]

	for n in range(0,8):		
		
		#team performance per game in the season
		filename = 'leagues/' + leagueList[n]		
		ifile = open(filename, 'rb')	
		reader = csv.reader(ifile)
		teamDictionary = {row[0]:row[2:len(row)] for row in reader}
		# teamDictionary = {}
		# for row in reader:
		# 	readline = []
		# 	for i in range(0,25):
		# 		if i not in [0,1,2,3,4,5,18,24]:
		# 			readline.append(row[i])
		# 	teamDictionary[row[0]] = readline
		ifile.close()
		
		#teams matchs played
		result = []
		filename = 'seasonmatch/' + fileList[n]		
		ifile = open(filename, 'rb')	
		reader = csv.reader(ifile)

		#'1' labels home team win the game
		#'0' labels home team lost
		for row in reader:
			try:
				if float(row[3]) > float(row[6]):
					readline = [1, row[1], row[4]]
					for item in teamDictionary[row[2]]:
						readline.append(item)
					for item in teamDictionary[row[5]]:
						readline.append(item)				
					result.append(readline)
				else:
					readline = [0, row[1], row[4]]
					for item in teamDictionary[row[2]]:
						readline.append(item)
					for item in teamDictionary[row[5]]:
						readline.append(item)				
					result.append(readline)
			except KeyError as err:
				print err
			except ValueError as err:
				print err 
		ifile.close()

		fileWriter = 'vector/vector' + fileList[n]
		ofile_writer(fileWriter, result)


if __name__ == '__main__':
	
	reload(sys)	
	sys.setdefaultencoding('utf-8')	

	main()
	