# League of Legends Championship Analysis
# Julian Marks, Ryan and Derek

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
import sklearn
import sys
import string
from datetime import datetime
from sklearn.linear_model import LinearRegression



INFO = 'C:/users/julian/school/programming/projects/league-analysis/data/LeagueofLegends.csv'
LOL = pd.read_csv(INFO)



### Helper Functions

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
    x = string.capwords(x)
    if isinstance(x,str):
        return Lanes.index(x)
    elif isinstance(x,int):
        return Lanes[x]
    else:
        print("ErrorL Invalid Input")

def ConvertGold(rb, lane):  # First cap for lane, not for rb
    rb = rb.lower()
    if rb=='red':
        br = 'blue'
    else:
        br = 'red'
    yGet = 'gold'+rb+lane
    champ = LOL[rb+lane+'Champ']
    Ochamp = LOL[br+lane+'Champ']
    convert = LOL[yGet]
    converted = pd.DataFrame()
    final = pd.DataFrame()
    for i in range(0,convert.shape[0]):
        String = convert.iloc[i][1:-1]
        x = pd.DataFrame(list(map(int,String.split(', ')))).T
        converted = converted.append(x, ignore_index=True)

    # Change the range on this loop to cycle through more than 1 game.
    # for i in range(0,len(converted.index)):   # This is the real loop. The replacement uses less data/time.
    for i in range(0,100):
        y = converted.iloc[i]
        y = y.dropna(how='any')
        const = pd.Series([y[0]]*len(y))
        t = pd.Series(list(range(0,len(y))))
        t2 = t**2
        x1 = pd.Series([WhichLane(lane)]*len(y))
        x2 = pd.Series([WhoChamp(champ[i])]*len(y))
        x3 = pd.Series([WhoChamp(Ochamp[i])]*len(y))
        merge = pd.concat([y,const,t,t2,x1,x2,x3], axis=1)
        merge.columns = ['Gold','Constant','Time','Time^2','Lane','Champ','OppChamp']  # In one lane, lane coefficient looks like intercept estimate.
        final = final.append(merge)
    return final


### Main Program

print('----------------------- Begin Program -----------------------')
timeStart = datetime.now().time()
print(timeStart)

# Functions create a data frame per lane per team, consisting of the gold earned during the game.
# Possibility to add a factor which considers difference between games.

time1 = datetime.now().time()
RedTop = ConvertGold('red','Top')

time2 = datetime.now().time()
RedJungle = ConvertGold('red','Jungle')
RedMid = ConvertGold('red','Middle')
RedADC = ConvertGold('red','ADC')
RedSupp = ConvertGold('red','Support')

time3 = datetime.now().time()
RedAll = [RedTop, RedJungle, RedMid, RedADC, RedSupp]

time4 = datetime.now().time()

BlueTop = ConvertGold('blue','Top')
BlueJungle = ConvertGold('blue','Jungle')
BlueMid = ConvertGold('blue','Middle')
BlueADC = ConvertGold('blue','ADC')
BlueSupp = ConvertGold('blue','Support')
BlueAll = [BlueTop, BlueJungle, BlueMid, BlueADC, BlueSupp]

time5 = datetime.now().time()

Total = pd.DataFrame()
Total = Total.append(RedAll)
Total = Total.append(BlueAll)

time6 = datetime.now().time()

singleTime = time2-time1
teamTime = time3-time1
totTeamTime = time4-time1
totTime = time5-time1
lastTime = time6-time5
fullTime = time6-time1

print([singleTime, teamTime, totTeamTime, totTime, lastTime, fullTime])


# print(list(map(int,LOL['goldblueTop'])))
# top_gold = pd.DataFrame(LOL['goldblueTop'])
# blueTopChamp = LOL['blueTopChamp']
# redTopChamp = LOL['redTopChamp']
# print(map(int, LOL['goldblueTop'].split(',')))
# type(top_gold.iloc[1])



# For estimation, starting gold is known, passive 'Gold per Minute' is known. All other gold is from cs, kills, items or masteries, so these are the qualities to be studied. To find best results, find a way to account for these in the model (Maybe remove their effect, or at least add it to the known regression equation)
# 
target = Total['Gold']
predictor = Total.drop(['Gold'], axis=1)

fit = sm.OLS(target,predictor).fit()  # Linear Regression without an intercept estimate. Lane variable looks like intercept since it is constant for 1 game.
print(fit.summary())

predictions = fit.predict(predictor)
xfit = np.linspace(0,10,1000)

# x = sm.add_constant(predictor)  # This adds the intercept estimate when other lanes are added into the data matrix.
# fit0 = sm.OLS(target,x).fit()
# print(fit0.summary())



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

timeEnd = datetime.now().time()
print(timeEnd)
print('----------------------- End Program. Run Time: {} -----------------------'.format(timeEnd-timeStart))