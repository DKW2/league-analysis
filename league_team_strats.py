# Look through baron, dragon, kills in 5 minute bins and compare the order from first to last?
# TSM, Immortals, C9
# Summer season and playoffs

# Derek Wang, 5/3/2018

import pandas as pd
import csv
import matplotlib.pyplot as plt
import sortData
import ast

def findFirst(objective):
	x = objective[0][0]
	for i in objective:
		if (i[0] < x):
			x = i[0]
	return x

def firstObjective(indexValues, team, teamName, objectiveName):
	time = []
	negTime = []
	for i in range(0, len(indexValues)):
		if(team.at[indexValues[i], "blueTeamTag"] == teamName): #Checks whether the team is blue or red
			color = "b"
			negColor = "r"
		else:
			color = "r"
			negColor = "b"
		objective = ast.literal_eval(team.at[indexValues[i], color + objectiveName]) #Retrieve list of a list of rDragons at indexValues[i], list of rDragons is [time, type]
		negObjective = ast.literal_eval(team.at[indexValues[i], negColor + objectiveName])
		if objective:
			if(team.at[indexValues[i], color + "Result"] == 1):
				time.append(findFirst(objective))
			else:
				negTime.append(findFirst(objective))
			# if negObjective:
			# 	if(findFirst(objective) < findFirst(negObjective)):
			# 		time.append(findFirst(objective))
			# 	else:
			# 		negTime.append(findFirst(objective))
			# else:
			# 	time.append(findFirst(objective))

	plt.hist(time, bins = 25, edgecolor = "black", range = (0, 50), color = "blue")
	plt.hist(negTime, bins = 25, edgecolor = "black", color = "red", range = (0, 50), alpha = 0.5)
	plt.xlabel("Time in minutes")
	plt.ylabel("# of Games")
	plt.title("All first " + objectiveName + " kills for " + teamName + " compared with wins and losses")

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
		firstObjective(indexValues, team, i, "Towers") #There might be an error? Check number of losses and wins and see if they're consistant
	
		
	
	
