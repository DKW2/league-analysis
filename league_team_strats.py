# Look through baron, dragon, kills in 5 minute bins and compare the order from first to last?
# TSM, Immortals, C9
# Summer season and playoffs

# Derek Wang, 5/3/2018

import pandas as pd
import csv
import matplotlib.pyplot as plt
import sortData
import ast

def firstDragon(indexValues, team, teamName):
	first = []
	timeDragons = []
	for i in range(0, len(indexValues)):
		if(team.at[indexValues[i], "blueTeamTag"] == teamName): #Checks whether the team is blue or red
			color = "b"
		else:
			color = "r"
		dragon = ast.literal_eval(team.at[indexValues[i], color + "Dragons"]) #Retrieve list of a list of rDragons at indexValues[i], list of rDragons is [time, type]
		if dragon:
			first.append(dragon[0])
			timeDragons.append(dragon[0][0])
	plt.hist(timeDragons, bins = 20, edgecolor = "black")
	plt.xlabel("Time in minutes")
	plt.ylabel("# of Games")
	plt.title("All first dragon kills for " + teamName)
	plt.show()

	# types = seperateTypes(first)
	# for i in types:
	# 	plotTypes(first, i)

def plotTypes(data, type): #If we want to see the contribution of each type of kill
	num = []
	for i in data:
		if(i[1] == type):
			num.append(i[0])
	print(num)
	plt.hist(num, bins = 20, color = "red")
	plt.title(type)
	plt.show()

def seperateTypes(data):
	types = []
	for i in data:
		if(not i[1] in types):
			types.append(i[1])
	return types

def compareTeams(matches, teamName):
	team = sortData.powerSort(matches, "NALCS", 2017, "Summer", all, teamName)
	indexValues = team.index.values.tolist()
	return team, indexValues

if __name__ == "__main__":
	matches = pd.read_csv(".\data\LeagueofLegends.csv")
	for i in {"C9", "TSM", "IMT"}:
		team, indexValues = compareTeams(matches, i)
		firstDragon(indexValues, team, i)
	
		
	
	
