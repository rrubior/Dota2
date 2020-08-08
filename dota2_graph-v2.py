# u/browjs' code
# Version 2.1 changed x axys to match match_dates


import requests
import matplotlib.pyplot as plt
from datetime import datetime #v2.1

account_id = '7000212' #enter your account ID here

queries = {'limit': 40, 'lobby_type': 7} #limit is the recent number of matches it will query, lobby type 7 = ranked, other parameters can be added based on openDOTA's API

res = requests.get(f'https://api.opendota.com/api/players/{account_id}/Matches', params = queries)

data = res.json()

def check_wins(data):
    match_results = []
    for matches in data:
        if matches['radiant_win'] == True and matches['player_slot'] <=127:
            match_results.append('Win')
        elif matches['radiant_win'] == False and matches['player_slot'] >127:
            match_results.append('Win')
        else:
            match_results.append('Loss')
    match_results.reverse() #reverses list to set origin from furthest back requested match
    return match_results

wins = check_wins(data)

def wins_numerically(match_results): #converts list with history of win loss into plot points for scatter plot +1 for a win, -1 for a loss
    match_history = [0]
    for results in match_results:
        if results == 'Win':
            match_history.append(match_history[-1]+1)
        else:
            match_history.append(match_history[-1] -1)
    return match_history

results = wins_numerically(wins)

# v2.1 - Convert the match timestamp to a dd-mm-yy format
def convert_date(data): #v2.1
    match_dates = []
    for matches in data:
        tstamp = matches['start_time']
        dtime = datetime.fromtimestamp(tstamp)
        date = dtime.strftime('%d-%m-%y')
        # print('Fecha del partido: ', date) #v2.1 (just for debug)
        return date

dates = convert_date(data) #v2.1

def create_dictionary(dates, wins): #v2.1
    dict = {}
    for win in wins:
        dict.update({win: dates})
    print(dict)


create_dictionary(dates, wins)

plt.scatter(range(len(results)), results)
plt.plot(range(len(results)), results)

plt.show()
