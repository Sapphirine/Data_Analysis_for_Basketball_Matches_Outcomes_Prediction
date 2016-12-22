# Data_Analysis_for_Basketball_Matches_Outcomes_Prediction

##Introduction

This program is used to predict the result of 2015-1016 NBA regular season using naive bayesian model. This program did not use any public dataset, all the data were downloaded by python web crawler, from NBA reference 'http://www.basketball-reference.com'. This program also contains all the used web crawler.

##Environments
- Operating System: MAC OS X EI Captian
- Language: python 
- Software: pyspark
- Lib: numpy, pyspar.mlib, requests, re, BeautifulSoup

##Programs
###NaiveBayesianModel

####NBA_nb.py
- run on spark, using spark-submit.
- from spark_data folder read the training and testing dataset.
- use training dataset to train Naive Bayesian model.
- calculate the accuracy.

outputfiles:
- result.csv record the win/loss of a game in predict regular season 2015-2016
- testoutput.csv record the true result at the leftmost and predicted result at the rightmost of each game. In each match, the team on the left is the home team.


###runVector

####establishFeatureVector.py
- from seasonmatch folder input the matches data of each game in the selected season.
- from leagues folder input the statical data of each team.
- label each matches and replace the team name using weight vectors.
- save the data in vector folder. The *.csv in this folder can directly used in naive Bayesian model.

###web crawler 

This folder contains seven web crawler written on python, for downloading different dataset from 'http://www.basketball-reference.com'.

- player_per_game.py: save players' performance in each game.
- player_season_per36m.py: save players' performance in each season per 36 minute.
- team_history_data.py: save teams' history performance.
- matchWithPer.py: save each match's info.
- establishDictionary.py: establish dictionary used in other web crawler.
- player_info.py: save all the players' info.
- player_season_info.py: save players' performance in each season per game.
