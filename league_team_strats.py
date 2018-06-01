# Look through baron, dragon, kills in 5 minute bins and compare the order from first to last?
# TSM, Immortals, C9
# Summer season and playoffs

# Derek Wang, 5/3/2018

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import sortData
import ast

def findFirst(objective):
	x = objective[0][0]
	for i in objective:
		if (i[0] < x):
			x = i[0]
	return x

def towerChoices(indexValues, team, teamName): # Prints out the most taken tower per tower. For example, the top first tower taken in the bottom lane
	choices = []
	for i in range(0, len(indexValues)):
		color, negColor = getTeamColor(team, indexValues, teamName, i)
		towers = ast.literal_eval(team.at[indexValues[i], color + "Towers"])
		if towers:
			towers.sort()
			for i in range(0, len(towers)):
				if(len(choices) < i + 1):
					choices.append([0,0,0])
				if(towers[i][1] == "TOP_LANE"):
					choices[i][0] = choices[i][0] + 1
				elif(towers[i][1] == "MID_LANE"):
					choices[i][1] = choices[i][1] + 1
				else:
					choices[i][2] = choices[i][2] + 1

	print("The list of the number of each tower taken per tower kill for " + teamName + " (i[0] = Top, i[1] = Mid, i[2] = Bot) is: ")
	print(choices)
	print()
	print("The most done tower picks for " + teamName + " are: ")

	order = ""
	for i in choices:
		if(i[0] > i[1] and i[0] > i[2]):
			order = order + "Top Lane, "
		elif(i[1] > i[0] and i[1] > i[2]):
			order = order + "Mid Lane, "
		else:
			order = order + "Bot Lane, "
	print(order + '\n')

def findFirstTake(objective):
	x = objective[0]
	for i in objective:
		if (i[0] < x[0]):
			x = i
	return x

def getTeamColor(team, indexValues, teamName, index):
	if(team.at[indexValues[index], "blueTeamTag"] == teamName):
		return "b", "r"
	else:
		return "r", "b"


def firstObjective(indexValues, team, teamName, objectiveName):
	time = []
	negTime = []
	for i in range(0, len(indexValues)):
		color, negColor = getTeamColor(team, indexValues, teamName, i)
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

def firstTower(indexValues, team, teamName):
	count = [0,0,0]
	for i in range(0, len(indexValues)):
		color, negColor = getTeamColor(team, indexValues, teamName, i)
		towers = ast.literal_eval(team.at[indexValues[i], color + "Towers"]) #Retrieve list of a list of rDragons at indexValues[i], list of rDragons is [time, type]
		if towers:
			lane = findFirstTake(towers)[1]
			if(lane == "TOP_LANE"):
				count[0] = count[0] + 1
			elif(lane == "MID_LANE"):
				count[1] = count[1] + 1
			else:
				count[2] = count[2] + 1

	names = ("Top Lane", "Mid Lane", "Bot Lane")
	y_pos = np.arange(len(names))

	plt.bar(y_pos, count, align = 'center', alpha = 0.8, color = "blue")
	plt.xticks(y_pos, names)
	plt.ylabel("# of Games")
	plt.title("Frequency of first tower picks for " + teamName)

	plt.show()

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
		#firstObjective(indexValues, team, i, "Towers") #There might be an error? Check number of losses and wins and see if they're consistant
		#firstTower(indexValues, team, i)
		towerChoices(indexValues, team, i)

		
	
	
