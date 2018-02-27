# Derek Wang, 1/29/2018

import requests
import pandas as pd
import csv
import time
import matplotlib.pyplot as plt
from collections import Counter

def tournaments():
	matches = pd.read_csv(".\data\LeagueofLegends.csv")
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
			listData = data.values.tolist()
			unique = len(set(listData))
		except:
			print("Key doesn't exist.")
			return
		if(type(listData[0]) == int or listData[0][0] != '['): #If values are ints
			if(unique <= 5):
				pieChart(listData, key)
			elif(unique <= 20):
				histofy(data, key)
			else:
				bigData(listData,key)
		else: #If values are lists
			print("Data can't be analyzed (yet)")
		answer = input("Quit? Press 'q' to quit: ")
		if(answer == 'q'):
			return
		print()

def histofy(data, key):
	plt.hist(data, bins = 20)
	plt.title(key)
	plt.show()

def pieChart(data, key):
	count = Counter(data)
	plt.pie(list(dict(count).values()), labels = list(dict(count).keys()), autopct='%1.1f%%')
	plt.title(key)
	plt.show()

def bigData(data, key):
	count = Counter(data)
	#print(dict(count))
	histofy(dict(count), key)
	#print(count)

if __name__ == "__main__":
	#summoner(APIKey)
	#matches(APIKey)
	#match(APIKey, "442454")
	#seedMatch(APIKey)
	tournaments()
