	# League of Legends Championship Analysis
# Julian Marks, Ryan and Derek
# 5/16/18

import sortData as sd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
import math
import sklearn
import sys
import string
import time
from sklearn.linear_model import LinearRegression

### Helper Functions ###

Champion = [x.lower() for x in ["Aatrox","Ahri","Akali","Alistar","Amumu","Anivia","Annie","Ashe","AurelionSol","Azir","Bard","Blitzcrank","Brand","Braum","Caitlyn","Camille","Cassiopeia","ChoGath","Corki","Darius","Diana","DrMundo","Draven","Ekko","Elise","Evelynn","Ezreal","Fiddlesticks","Fiora","Fizz","Galio","Gangplank","Garen","Gnar","Gragas","Graves","Hecarim","Heimerdinger","Illaoi","Irelia","Ivern","Janna","JarvanIV","Jax","Jayce","Jhin","Jinx","Kalista","Karma","Karthus","Kassadin","Katarina","Kayle","Kayn","Kennen","KhaZix","Kindred","Kled","KogMaw","LeBlanc","LeeSin","Leona","Lissandra","Lucian","Lulu","Lux","Malphite","Malzahar","Maokai","MasterYi","MissFortune","Mordekaiser","Morgana","Nami","Nasus","Nautilus","Nidalee","Nocturne","Nunu","Olaf","Orianna","Ornn","Pantheon","Poppy","Quinn","Rakan","Rammus","RekSai","Renekton","Rengar","Riven","Rumble","Ryze","Sejuani","Shaco","Shen","Shyvana","Singed","Sion","Sivir","Skarner","Sona","Soraka","Swain","Syndra","TahmKench","Taliyah","Talon","Taric","Teemo","Thresh","Tristana","Trundle","Tryndamere","TwistedFate","Twitch","Udyr","Urgot","Varus","Vayne","Veigar","VelKoz","Vi","Viktor","Vladimir","Volibear","Warwick","Wukong","Xayah","Xerath","XinZhao","Yasuo","Yorick","Zac","Zed","Ziggs","Zilean","Zoe","Zyra"]]

Lanes = ['Top','Jungle','Middle','Adc','Support']


def WhoChamp(x):
	if isinstance(x,str):
		return Champion.index(x.lower())
	elif isinstance(x,int) and x <= len(Champion):
		return Champion[x]
	else:
		print("Error: Invalid Input")

def WhichLane(x):
    if isinstance(x,str):
        return Lanes.index(string.capwords(x))
    elif isinstance(x,int):
        return Lanes[x]
    else:
        print("Error: Invalid Input")


# This is difference of gold regression by (redLaneGold-blueLaneGold).
def GoldLaneDiff(lane,DF):  # First cap for lane, not for rb
    yr = 'goldred'+lane
    yb = 'goldblue'+lane
    champ = DF['red'+lane+'Champ']
    Ochamp = DF['blue'+lane+'Champ']
    convert1 = DF[yr]
    convert2 = DF[yb]
    converted1 = pd.DataFrame()
    converted2 = pd.DataFrame()
    for i in range(0,convert1.shape[0]):
        String = convert1.iloc[i][1:-1]
        x = pd.DataFrame(list(map(int,String.split(', ')))).T
        converted1 = converted1.append(x, ignore_index=True)
        String = convert2.iloc[i][1:-1]
        x = pd.DataFrame(list(map(int,String.split(', ')))).T
        converted2 = converted2.append(x, ignore_index=True)

    final = pd.DataFrame()
    for i in range(0,len(converted1.index)):   # This is the real loop. The replacement uses less data/time.
    # for i in range(0,5):
        yr = converted1.iloc[i]
        yr = yr.dropna(how='any')
        yb = converted2.iloc[i]
        yb = yb.dropna(how='any')
        t = pd.Series(list(range(0,len(yr))))
        t2 = t**2
        x1 = pd.Series([WhichLane(lane)]*len(yr))
        x2 = pd.Series([WhoChamp(champ[i])]*len(yr))
        x3 = pd.Series([WhoChamp(Ochamp[i])]*len(yr))
        merge = pd.concat([yr,yb,t,t2,x1,x2,x3], axis=1)
        merge.columns = ['RedGold','BlueGold','Time','Time^2','Lane','Champ','OppChamp'] 
        final = final.append(merge)
    return final


def ConvertGold(column, DF):
	final=DF
	change=DF[column]
	convert=pd.DataFrame()
	for i in range(0,change.shape[0]):
		string=change.iloc[i][1:-1]
		# print(string)
		x = pd.DataFrame(list(map(int,string.split(', ')))).T
		convert = convert.append(x,ignore_index=True)
		# print(convert)

	merge=pd.DataFrame()		# NaN values denote the first minute after the game has ended
	for i in range(0,len(convert.index)):
		fix=convert.iloc[i].dropna(how='any')
		merge=merge.append(fix,ignore_index=True)
	return merge

def Regression(target, predictor):
	return sm.OLS(target,predictor).fit()

### Options and File Dependencies ###

np.set_printoptions(threshold=np.nan)
INFO = 'C:/users/julian/school/programming/projects/league-analysis/data/LeagueofLegends.csv'
LOL = pd.read_csv(INFO)


### Preprocessing ###

print('----------------------- Begin Program -----------------------')
timeStart = time.time()
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

# Functions create a data frame per lane per team, consisting of the gold earned during the game.
# Possibility to add a factor which considers difference between games.


TSM=sd.powerSort(LOL, leagueName='NALCS', year=2017, season='Spring', typeGame='Season', teamTag='TSM')

# print(TSM.head(1)['golddiff'])

TSMGold=ConvertGold(column='golddiff',DF=TSM)	# Gold Difference is measured by BlueGold-RedGold
												# Make sure when specifying a team, use TeamGold-OppGold
												# If Team=blue, leave as is. If Team=red, use (-1)*GoldDiff

numGames=TSMGold.shape[0]

wins=list()
diff=pd.DataFrame()
for i in range(numGames):			# Loop to observe bar plots of gold difference per game
	
	# plt.figure(i)
	
	if TSM['redTeamTag'].iloc[i]=='TSM':
		TSMGold.iloc[i]=(-1)*TSMGold.iloc[i]
		if TSM['rResult'].iloc[i] == 0:
			plt.title('TSM Gold Difference from a Loss')
			wins.append(0)
		else:
			plt.title('TSM Gold Difference from a Win')
			wins.append(1)
	else:
		if TSM['bResult'].iloc[i] == 0:
			plt.title('TSM Gold Difference from a Loss')
			wins.append(0)
		else:
			plt.title('TSM Gold Difference from a Win')
			wins.append(1)

	x=TSMGold.iloc[i].dropna(how='any')
	y_pos=np.arange(len(x))

	# plt.bar(y_pos, x, align='center', alpha=.5)
	# plt.xticks(y_pos,range(0,len(x)))
	# plt.ylabel('Difference')

	# plt.show()

	ins=list()
	for j in range(0,len(x)-1):							# diff is a dataframe containing the relative gain/loss of gold over each minute
		ins.append(x[j+1]-x[j])
	diff=pd.concat([diff,pd.Series(ins)],axis=1)

diff.columns=range(numGames)

indMinMax=list()
pindMinMax=list()
for i in range(0,diff.shape[1]):
	x=diff[i].dropna(how='any')
	indMinMax.append( (x.idxmin([0]),x.idxmax([0])) )					# Give indices in tuples of (Time of max loss, Time of max gain)
	pindMinMax.append( (x.idxmin([0])/len(x),x.idxmax([0])/len(x)) )	# Gives same information in proportion of game played
																		# Attempt to measure 


# print(pindMinMax)
# print(indMinMax)

ranked=list()

for j in range(diff.shape[1]):							# Create ranked list which is indexed by time. 1 is the time of biggest loss,
	sort=diff[j].dropna(how='any')						# len(list) is the time of largest gain
	indices = list(range(len(sort)))
	indices.sort(key=lambda x: sort[x])
	output = [0] * len(indices)
	for i, x in enumerate(indices):
		output[x]=i
	ranked.append(output)

for i in range(len(ranked)):
	bin=list()
	tempBin=list()
	for it in ranked[i]:
		tempBin.append(it)
		if(len(tempBin)==5):
			bin.append(tempBin)
			tempBin=list()

	print(bin)
	binSum=list()
	for it in bin:
		binSum.append(sum(it))

	print(binSum)
	y_pos=np.arange(len(binSum))
	plt.bar(y_pos, binSum, align='center', alpha=.5)
	plt.xticks(y_pos,range(0,len(binSum)))
	plt.ylabel('Ranked Difference')
	if wins[i]==0:
		plt.title('TSM Binned Gold from a Loss')
	else:
		plt.title('TSM Binned Gold from a Win')
	plt.show()


# print(ranked[0])

# for i in range(len(ranked)):
	# print(ranked[i])
	# print(ranked[i].index(0))


# for i in range(len(ranked[o])):



# print(ranked)
# print(len(ranked))



sys.exit()



time1 = time.time()

RedTop = GoldLaneDiff('Top', LOL)

# This part is extremely compacted to test if all functions above work properly, and to see if regression programming runs bug free.
# ##########################################################################################

# print(RedTop)
# print(RedTop.shape)
# print(RedTop.columns)

# Total = RedTop


# LaneChange = pd.get_dummies(Total['Lane'])
# for i in LaneChange.columns:
# 	LaneChange.rename(columns={int(i):WhichLane(int(i))}, inplace=True)


# OChampChange = pd.get_dummies(Total['OppChamp'])

# ChampChange = pd.get_dummies(Total['Champ'])


# for i in ChampChange.columns:
# 	ChampChange.rename(columns={int(i):WhoChamp(int(i))}, inplace=True)

# for i in OChampChange.columns:
# 	x=WhoChamp(int(i))+'Opp'
# 	OChampChange.rename(columns={int(i):x}, inplace=True)

# ChampChange = pd.concat([ChampChange, OChampChange], axis=1)

# Total = pd.concat([Total.drop(['Lane','Champ','OppChamp'], axis=1), LaneChange, ChampChange], axis=1)


# target = Total['GoldDiff']
# predictor = Total.drop(['GoldDiff'], axis=1)

# fit = sm.OLS(target,predictor).fit()
# print(fit.summary())

# sys.exit()


# ######################################################################################

time2 = time.time()

RedJungle = GoldLaneDiff('Jungle',LOL)
RedMid = GoldLaneDiff('Middle',LOL)
RedADC = GoldLaneDiff('ADC',LOL)
RedSupp = GoldLaneDiff('Support',LOL)
RedAll = [RedTop, RedJungle, RedMid, RedADC, RedSupp]

time3 = time.time()

Total = pd.concat(RedAll, axis=0)

LaneChange = pd.get_dummies(Total['Lane'])
for i in LaneChange.columns:
	LaneChange.rename(columns={int(i):WhichLane(int(i))}, inplace=True)


# Incorrect merging of data. All missing information is converted to NA instead of 0 dummies (for missing champs/lanes)
# 3/28/18 :: I believe the problem has been fixed, and results were obtained via regression, however due to the layout of dummies (-1,1) and the data included the output is a bit confusing. How to correct the issue:
	## Separate by lanes to keep counters lane specific
	## Put Opponent champ into separate dummies
		## Could also include interaction effects

# PLAN: Find a way to merge Champ and OppChamps into 1 data frame as +1/-1 to consolidate champion effects.


## FIXED: Now instead creates a Champ and OppChamp Dataframe, concatenates them horizontally and thus each Champ and OppChamp have independent dummy variables. Currently Opp is set to -1 to "Reduce" gold gain from the player.

OChampChange = pd.get_dummies(Total['OppChamp'])

ChampChange = pd.get_dummies(Total['Champ'])

# ChampChange = pd.get_dummies(Total['Champ']).join((-1)*pd.get_dummies(Total['OppChamp']), how='outer')

for i in ChampChange.columns:
	ChampChange.rename(columns={int(i):WhoChamp(int(i))}, inplace=True)

for i in OChampChange.columns:
	x=WhoChamp(int(i))+'Opp'
	OChampChange.rename(columns={int(i):x}, inplace=True)

ChampChange = pd.concat([ChampChange, OChampChange], axis=1)

Total = pd.concat([Total.drop(['Lane','Champ','OppChamp'], axis=1), LaneChange, ChampChange], axis=1)

### Main Program ###

usr=-1
while(usr!=0):
	print("What results would you like to see?")
	print("1: Red - Blue Gold Difference Regression")
	print("2: Red Gold Regression")
	print("3: Blue Gold Regression")
	print("4: Red Lane Gold Regression")
	print("5: Blue Lane Gold Regresion")
	print("6: Lane Gold Regression")
	print("7: Lane Gold Difference Regression (Red - Blue)")
	usr=int(input("Enter 0 to exit"))
	if(usr==1):
		target = Total['RedGold']-Total['BlueGold']
		predictor = Total.drop(['RedGold','BlueGold'], axis=1)
		fit = sm.OLS(target,predictor).fit()
		print(fit.summary())
	if(usr==2):
		target = Total['RedGold']
		predictor = Total.drop(['RedGold','BlueGold'], axis=1)
		fit = sm.OLS(target,predictor).fit()
		print(fit.summary())
	if(usr==3):
		target = Total['BlueGold']
		predictor = Total.drop(['RedGold','BlueGold'], axis=1)
		fit = sm.OLS(target,predictor).fit()
		print(fit.summary())
	if(usr==4):
		target = Total['RedGold']
		predictor = Total.drop(['RedGold','BlueGold'], axis=1)
		fit = sm.OLS(target, predictor).fit()
		print(fit.summary())
	if(usr==5):
		target = Total['BlueGold']
		predictor = Total.drop(['RedGold','BlueGold'], axis=1)
		fit = sm.OLS(target, predictor).fit()
		print(fit.summary())
	if(usr==6):
		target = pd.concat([Total['RedGold'],Total['BlueGold']],axis=0)
		predictor = pd.concat([Total[['Time','Time^2','Top','Jungle','Middle','Adc','Support']],Total[['Time','Time^2','Top','Jungle','Middle','Adc','Support']]],axis=0)
		# pd.concat([Total.drop(['RedGold','BlueGold'],axis=1),Total.drop(['RedGold','BlueGold'],axis=1)],axis=0)
		fit = sm.OLS(target, predictor).fit()
		print(fit.summary())
	if(usr==7):
		target = Total['RedGold']-Total['BlueGold']
		predictor = Total[['Time','Time^2','Top','Jungle','Middle','Adc','Support']]
		fit = sm.OLS(target, predictor).fit()
		print(fit.summary())



# For estimation, starting gold is known, passive 'Gold per Minute' is known. All other gold is from cs (sub for time), kills, items or masteries, so these are the qualities to be studied. To find best results, find a way to account for these in the model (Maybe remove their effect, or at least add it to the known regression equation)
# If time variable is limited to the passive gold income/time then the entire gold effect can be carried in the weight of the champion variable.

# target = Total['GoldDiff']
# predictor = Total.drop(['GoldDiff'], axis=1)

# fit = sm.OLS(target,predictor).fit()
# print(fit.summary())

# predictions = fit.predict(predictor)
# xfit = np.linspace(0,10,1000)

# x = sm.add_constant(predictor)  # This adds the intercept estimate when other lanes are added into the data matrix.
# fit0 = sm.OLS(target,x).fit()
# print(fit0.summary())


timeEnd = time.time()
print('----------------------- End Program. Run Time: {} -----------------------'.format(timeEnd-timeStart))



### Appendix of Unused Code (So Far) ###


### Graphing and Visuals will follow Eventually

# model.summary()

# lm = LinearRegression(fit_intercept=True)
# lm.fit(t,y)

# xfit = np.linspace(0,10,1000)
# yfit = lm.predict(xfit[:, np.newaxis])

# plt.scatter(t,y)
# plt.plot(xfit, yfit)
# plt.show()

# print(pd.Series(t).T)
# pred = lm.predict(t)
# print(pred)
# plt.plot(pred, color='blue')
# plt.scatter(t,y)
# plt.show()


# plt.bar(range(len(x)),x)
# plt.show()


# print(LOL['goldblueTop'].iloc[1])

# print(LOL[['blueTopChamp','goldblueTop','redTopChamp','goldredTop']])