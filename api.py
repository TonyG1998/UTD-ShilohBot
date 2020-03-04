#testing faceit requests
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
AUTH = os.getenv('API_AUTH')


headers = {'authorization' : AUTH}
#converts the request into python object
def load_json(request):
	j = json.dumps(request.json(), sort_keys=True, indent=4)
	print(j)
	data = json.loads(j)
	return data


def num_of_ongoing_matches():
	url = 'https://open.faceit.com/data/v4/hubs/860cace2-43ef-490d-ab72-ca4c760d959c/matches?type=ongoing&offset=0&limit=20'
	
	r = requests.get(url, headers=headers)
	data = load_json(r)
	return len(data['items'])

def ongoing_match_data():
	url = 'https://open.faceit.com/data/v4/hubs/860cace2-43ef-490d-ab72-ca4c760d959c/matches?type=ongoing&offset=0&limit=2'
	r = requests.get(url, headers=headers)
	data=load_json(r)

	#if no ongoing matches, return 0
	if len(data['items']) == 0:
		return 0

	team1 = data['items'][0]['teams']['faction1']['name']
	team2 = data['items'][0]['teams']['faction2']['name']
	map_pick = data['items'][0]['voting']['map']['pick'][0]

	team1_players = []
	team2_players = []

	#loops to retrieve player rosters and add them to a list
	team = data['items'][0]['teams']['faction1']['roster']

	for player in team:
		team1_players.append(player['nickname'])

	team = data['items'][0]['teams']['faction2']['roster']

	for player in team:
		team2_players.append(player['nickname'])


	parsed = {
	'team1' : team1,
	'team2' : team2,
	'map' : map_pick,
	'team1_roster' : team1_players,
	'team2_roster' : team2_players
	}

	return parsed
def past_match_data():
	url = 'https://open.faceit.com/data/v4/hubs/860cace2-43ef-490d-ab72-ca4c760d959c/matches?type=past&offset=0&limit=1'
	r=requests.get(url, headers=headers)
	data = load_json(r)
	
	print(data)




