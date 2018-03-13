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
def columnFinder(year, column, both):
	if both:
		#data = year["red" + column]
		#data.append(year["blue" + column], ignore_index = True)
		data = pd.concat([year["red" + column], year["blue" + column]], ignore_index = True)
	else:
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

# Creates a line graph of the count of each <column> through the years
# Main method to create linear graphs for time differences
# Accepts 8 Parameters: years (list of dataframes of each year), 
#						column (which column the user would like to compare through the years)
#						xlabel (the label of the x-axis)
#						ylabel (the label of the y-axis)
#						title (the title of the graph)
#						tooMuch (Used only when there are too many different data points that they 
#								will make the graph unreadable)
#						min (The minimum # of counts that a data point can have to be posted on the graph.
#							 Only used when tooMuch = True)
#						both (Determines whether to use both teams data or just the column stated.
#							  Disclaimer: when using both, the column name needs to be the string after
#							  the team name. For example, redADCChamp would just be ADCChamp if using both
#							  Otherwise, if you would like to look ONLY at ADC champions from the red team,
#							  enter redADCChamp as the column name and make both equal to false)
def leagueDifference(years, column, xlabel, ylabel, title, tooMuch = False, min = 200, both = False):
	leagueCount = []
	names = []
	leagueCount, names = getNames(years, leagueCount, names, column, both)
	getCountAndPlot(names, leagueCount, xlabel, ylabel, title, tooMuch, min)

#Returns a list of 5 dictionaries for each year that contains
#the count of each <column> and a list of the names of each <column>
def getNames(years, leagueCount, names, column, both):
	leagues = []
	for i in years:
		leagues.append(columnFinder(i, column, both))
	for i in leagues:
		leagueCount.append(dict(Counter(i)))
	for i in range(0, 5):
		for key in leagueCount[i].keys():
			if key not in names:
				names.append(key)
	return leagueCount, names

#Gets the count of each league seperately and graphs them
def getCountAndPlot(names, leagueCount, xlabel, ylabel, title, tooMuch, min):
	year = [2014,2015,2016,2017,2018]
	tiny = False
	for key in names:
		count = []
		for i in range(0,5):
			if key not in leagueCount[i]:
				count.append(0)
			else:
				count.append(leagueCount[i][key])
		#print(max(count))
		if(tooMuch and max(count) < min):
			tiny = True
		if not tiny:
			plt.plot(year, count, label = key)
		tiny = False
	plotData(xlabel, ylabel, title)

#Plots the data with the given parameters
def plotData(xlabel, ylabel, title):
	plt.legend(loc= 'best')
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.show()


if __name__ == "__main__":
	matches = pd.read_csv(".\data\LeagueofLegends.csv")
	years = seperateToYears(matches)
	leagueDifference(years, "League", "Year", "Games", "# of League games vs. Year")
	leagueDifference(years, "MiddleChamp", "Year", "Games", 
					"# of appearances of Middle Lane Champion vs. Year",
		            True, 200, True)
	leagueDifference(years, "TopChamp", "Year", "Games", 
					"# of appearances of Top Lane Champion vs. Year", 
					True, 200, True)
	leagueDifference(years, "ADCChamp", "Year", "Games",
					"# of appearances of ADC Champions vs. Year",
					True, 200, True)
	leagueDifference(years, "SupportChamp", "Year", "Games",
					"# of appearances of Support Champions vs. Year",
					True, 200, True)
	leagueDifference(years, "JungleChamp", "Year", "Games",
					"# of appearances of Jungler Champions vs. Year",
					True, 200, True)