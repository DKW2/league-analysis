# Derek Wang, 1/29/2018

import requests
import pandas as pd
import csv
import time
import matplotlib.pyplot as plt

def summoner(APIKey):
	URL = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/fortense?api_key=" + APIKey
	response = requests.get(URL)
	responseJSON = response.json()
	for i in responseJSON:
		print(i + ": " + str(responseJSON[i]))

def match(APIKey, matchID):
	URL = "https://na1.api.riotgames.com/lol/match/v3/matches/" + matchID + "?api_key=" + APIKey
	response = requests.get(URL)
	responseJSON = response.json()
	print(responseJSON)

def matches(APIKey):
	matchList = pd.read_csv("queue.csv", names = ["matchID"])
	print(matchList) 
	with open("idInfo.csv", "w") as csvfile:
		filewriter = csv.writer(csvfile, delimiter = ',', 
								quotechar = '|', quoting = csv.QUOTE_MINIMAL)

		filewriter.writerow("matchID", "")
		#for i in matchList["matchID"]:
			#print(i)
		filewriter.writerow(["secondtest", "hellow"])
		filewriter.writerow(["banana", "Apple"])

def seedMatch(APIKey):
	timeDuration = []
	for i in range(1,11):
		match = pd.read_json("matches" + str(i) + ".json")
		for i in range(100):
			timeDuration = timeDuration + [match["matches"][i]["gameDuration"]]
	plt.hist(timeDuration, bins = 20)
	plt.xlabel("Time(Seconds)")
	plt.title("Distribution of time in matches")
	plt.show()

def tournaments():
	matches = pd.read_csv("LeagueofLegends.csv")
	while(True):
		print("Here are all of the keys: ")
		count = 0
		for i in matches.keys():
			print(i, end = ', ')
			if(count == 8):
				print()
				count = 0
			count += 1
		print()
		key = input("Type which one you want to analyze: ")
		try:
			data = matches[key]
		except:
			print("Key doesn't exist.")
			return
		if(type(list(data.loc[[0]])[0]) == int):
			histofy(data)
		elif(list(data.loc[[0]])[0][0]=='['):
			print("Data can't be analyzed (yet)")
		else:
			histofy(data)
		answer = input("Quit? Press 'q' to quit: ")
		if(answer == 'q'):
			return
		print()

def histofy(data):
	plt.hist(data, bins = 20)
	plt.show()


if __name__ == "__main__":
	#summoner(APIKey)
	#matches(APIKey)
	#match(APIKey, "442454")
	#seedMatch(APIKey)
	tournaments()
