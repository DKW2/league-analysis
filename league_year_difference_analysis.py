# Derek Wang, 1/29/2018

import requests
import pandas as pd
import csv
import time
import matplotlib.pyplot as plt
from collections import Counter

#Creates a pie chart with the data given and titles the chart with the variable key
def pieChart(data, key):
	count = Counter(data)
	plt.pie(list(dict(count).values()), labels = list(dict(count).keys()), autopct='%1.1f%%')
	plt.title(key)
	plt.show() 

#Finds the column of the DataFrame year and returns it as a list
def columnFinder(year, column):
	data = year[column]
	return data.values.tolist()

#Seperates the DataFrame matches into a list of DataFrames of each year
def seperateToYears(matches):
	years = []
	for i in range(2014, 2019):
		years.append(matches[matches["Year"] == i])
	return years

def portrayYears():
	matches = pd.read_csv(".\data\LeagueofLegends.csv")
	matches.sort_values("Year")
	years = seperateToYears(matches)
	listData = columnFinder(years[1], "League")
	pieChart(listData, "Something")

def leagueDifference(matches):
	leagues = []
	leagueCount = []
	names = []
	year = [2014,2015,2016,2017,2018]
	for i in years:
		leagues.append(columnFinder(i, "League"))
	for i in leagues:
		leagueCount.append(dict(Counter(i)))
	for i in range(0, 5):
		for key in leagueCount[i].keys():
			if key not in names:
				names.append(key)
	for key in names:
		count = []
		for i in range(0,5):
			if key not in leagueCount[i]:
				count.append(0)
			else:
				count.append(leagueCount[i][key])
		plt.plot(year, count, label = key)
#Almost there?

	#for i in names:
	#	plt.plot(year, )
	#rint(names)
	plt.legend(loc= 'best')
	plt.xlabel("Year")
	plt.ylabel("Games")
	plt.title("# of League games vs. Year")
	plt.show()
	#graphLeagueDifference(leagueCount)

def graphLeagueDifference(leagueCount):
	print("hi")


if __name__ == "__main__":
	matches = pd.read_csv(".\data\LeagueofLegends.csv")
	years = seperateToYears(matches)
	leagueDifference(matches)