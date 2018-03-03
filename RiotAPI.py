### Required Libraries
## Look at Pandas and Numpy
import requests
import pyperclip    # To help with receiving long text responses to local machine
import os

### Important URLs
API_KEY = "RGAPI-59a50598-2258-408b-ad72-421643a011a6"
CHAMPIONS = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
SPECTATOR_FEAT = "https://na1.api.riotgames.com/lol/spectator/v3/featured-games?api_key="

BASE_URL = "https://na1.api.riotgames.com/lol/"
SUMMONER_ID = "summoner/v3/summoners/by-name/Bjergsen?api_key="
MATCH_ID = "match/v3/matchlists/by-account/214376669?api_key="
GAME_ID = "match/v3/matches/2707683651?api_key="

GET = BASE_URL+SUMMONER_ID+API_KEY

print('-------------------- Begin Program -------------------------\n')

STATE = requests.get(GET)
print(STATE.text)

GET = BASE_URL+MATCH_ID+API_KEY
MATCHES = requests.get(GET)
print(MATCHES.text)

GET = BASE_URL+GAME_ID+API_KEY
GAME = requests.get(GET)
print(GAME.text)

# CHAMPS = requests.get(CHAMPIONS)    # Response is json lib of all champions and their personal game information
#
# STATE = SPECTATOR_FEAT + API_KEY
# SPEC = requests.get(STATE)
# print(SPEC.text)

print('-------------------- End Program -------------------------\n')
