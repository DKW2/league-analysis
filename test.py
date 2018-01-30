### Required Libraries
## Look at Pandas and Numpy
import requests
import pyperclip    # To help with receiving long text responses to local machine
import os

### Important URLs
API_KEY = "RGAPI-eaca5c50-8809-47da-a474-02807152917c"
CHAMPIONS = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
SPECTATOR_FEAT = "https://na1.api.riotgames.com/lol/spectator/v3/featured-games?api_key="
TEST = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/mastershark101?api_key="


GET = TEST+API_KEY




print('-------------------- Begin Program -------------------------\n')
STATE = requests.get(GET)

print(STATE.text)

CHAMPS = requests.get(CHAMPIONS)    # Response is json lib of all champions and their personal game information

STATE = SPECTATOR_FEAT + API_KEY
SPEC = requests.get(STATE)
print(SPEC.text)

print('-------------------- End Program -------------------------\n')
