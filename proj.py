# League of Legends Championship Analysis
# Julian Marks, Ryan and Derek

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

INFO = 'C:/users/julian/school/programming/projects/league-analysis/data/LeagueofLegends.csv'
LOL = pd.read_csv(INFO)


# Find some directional ideas for the course of this project

print('------------------------- Begin Program -------------------------')

# print(list(map(int,LOL['goldblueTop'])))
df = pd.DataFrame(LOL['goldblueTop'])
# print(map(int, LOL['goldblueTop'].split(',')))
# type(df.iloc[1])


########################### Successful Piece ################################

# Create a data frame for the gold/time for all games provided (Generalize a function to apply to any lane)
goldblueTop = pd.DataFrame()
for i in range(0,df.shape[0]):
    String = LOL['goldblueTop'].iloc[i][1:-1]
    x = pd.DataFrame(list(map(int,String.split(', ')))).T
    goldblueTop = goldblueTop.append(x, ignore_index=True)

plt.bar(range(len(x)),x)
plt.show()

#############################################################################

# print(LOL['goldblueTop'].iloc[1])

# print(LOL[['blueTopChamp','goldblueTop','redTopChamp','goldredTop']])

print('------------------------- End Program -------------------------')
