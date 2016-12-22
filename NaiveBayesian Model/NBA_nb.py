#filename spark_demo.py
import sys
from operator import add
from math import exp
import warnings
import numpy
from numpy import array
from pyspark import RDD, since, SparkContext
from pyspark.mllib.linalg import DenseVector, SparseVector, _convert_to_vector
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.util import MLUtils
import csv

#file writer function 
def ofile_writer(name, data_writer):
	ofile  = open(name, "wb")
	writer = csv.writer(ofile, delimiter=',')
	for each in data_writer:
		writer.writerow(each)
	ofile.close()

if __name__ == '__main__':
	sc = SparkContext("local", "testing")

	#test_array = array([1.0, 2.0, 3.0])
	data = []
	test = []

	fileList = ['2008-2009.csv', '2009-2010.csv', '2010-2011.csv',
				'2011-2012.csv', '2012-2013.csv', '2013-2014.csv',
				'2014-2015.csv', '2015-2016.csv' ]
	leagueList = [ ('vector' + item) for item in fileList ]
	file_list = leagueList[0:len(fileList)-1]
	file_train = leagueList[len(fileList)-1]
	y_test = []
	
	#input the training data
	for filename in file_list:
		filename = 'spark_data/' + filename
		with open(filename) as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				row[1:3] = []
				row = [ float(item) for item in row ]
				for i in range(1,len(row)/2+1):
					row[i]=row[i]/row[i+len(row)/2]
				data.append( LabeledPoint( row[0], array(row[1:len(row)/2])))				
			csvfile.close()

	#input the test data
	with open(('spark_data/'+file_train)) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:	
			y_test.append(row[0:3])		
			row[1:3] = []
			row = [ float(item) for item in row ]
			for i in range(1,len(row)/2+1):
					row[i]=row[i]/row[i+len(row)/2]
			test.append( array(row[1:len(row)/2]) )
		csvfile.close()

	#train model
	model = NaiveBayes.train(sc.parallelize(data))
	prediction = [ model.predict(item) for item in test ]

	data_writer = []
	for i in range(0,len(prediction)):
		dataline = y_test[i]
		dataline.append(prediction[i])
		data_writer.append(dataline)
	ofile_writer('testoutput.csv', data_writer)

	#calculation the accuracy of NaiveBayesModel 
	count1 = 0.0
	count2 = 0.0
	for i in range(0,len(prediction)):
		if prediction[i] == float( y_test[i][0] ):
			count1 = count1 + 1
		else:
			count2 = count2 + 1
	print count1 / ( count1 + count2 )

	sc.stop()



