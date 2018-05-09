import pandas as pd
import matplotlib.pyplot as plt    
league=pd.read_csv("LeagueofLegends.csv")

# Helper function, sorts data in a df
# Input a dataframe and sort paramater, returns a new dataframe with only entries with that value
def sortData(yourDF, columnName, valueInColumn):  
    searchCriteria=yourDF[columnName]==valueInColumn
    newDF=yourDF.loc[searchCriteria]
    return(newDF)

# # only sorts for dataframes
# Input a dataframe and all the values you would like it to sort by
# Input 'all' if you don't want to sort by paramater, or 0 for year
# Output sorted DF by all paramaters
def powerSort(DF, leagueName='all', year=0, season='all', typeGame='all', teamTag='all'):
        initialDF=DF
        if leagueName!='all':
                DFsort1=sortData(initialDF,'League', leagueName)
        else:
                DFsort1=initialDF
        years=[2015,2016,2017,2018]
        if year in years:
                DFsort2=sortData(DFsort1,'Year', year)
        else:
                DFsort2=DFsort1               
        seasons=['Spring','Summer']
        if season in seasons:
                DFsort3=sortData(DFsort2,'Season', season)
        else:
                DFsort3=DFsort2               
        gameTypes=['Season', 'Playoffs', 'Regional', 'International']
        if typeGame in gameTypes:
                DFsort4=sortData(DFsort3,'Type',typeGame)
        else:
                DFsort4=DFsort3               
        if teamTag!='all':
                DFB=sortData(DFsort4,'blueTeamTag', teamTag)
                DFR=sortData(DFsort4,'redTeamTag', teamTag)
                frames=[DFR,DFB]
                DFsortFinal=pd.concat(frames)
        else:
                DFsortFinal=DFsort4               
        return(DFsortFinal)
