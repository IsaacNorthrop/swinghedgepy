import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json

teams = {
    "108": "Los Angeles Angels",
    "117": "Houston Astros",
    "133": "Oakland Athletics",
    "141": "Toronto Blue Jays",
    "144": "Atlanta Braves",
    "158": "Milwaukee Brewers",
    "138": "St. Louis Cardinals",
    "112": "Chicago Cubs",
    "109": "Arizona Diamondbacks",
    "119": "Los Angeles Dodgers",
    "137": "San Francisco Giants",
    "114": "Cleveland Guardians",
    "136": "Seattle Mariners",
    "146": "Miami Marlins",
    "121": "New York Mets",
    "120": "Washington Nationals",
    "110": "Baltimore Orioles",
    "135": "San Diego Padres",
    "143": "Philledelphia Phillies",
    "134": "Pittsburgh Pirates",
    "140": "Texas Rangers",
    "139": "Tampa Bay Rays",
    "113": "Cinncinati Reds",
    "111": "Boston Red Sox",
    "115": "Colorado Rockies",
    "118": "Kansas City Royals",
    "116": "Detroit Tigers",
    "142": "Minnesota Twins",
    "145": "Chicago White Sox",
    "147": "New York Yankees"
}

def getPlayerLinks():
    initial_response = requests.get('https://baseballsavant.mlb.com/probable-pitchers')

    soup = BeautifulSoup(initial_response.content, 'html.parser')

    hrefs = [a['href'] for a in soup.find_all('a', class_='matchup-link')]

    unique_links = list(set(hrefs))

    return unique_links

def getPlayerData(matchup_response):
    soup = BeautifulSoup(matchup_response, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and 'var qs' in script.string:
            #print(script.string)
            json_split = script.string.split(';')
            matchup_json = json_split[0].split('=')[1].strip()
            player_json = json_split[1].split('=')[1].strip()
            matchup_data = json.loads(matchup_json)
            player_data = json.loads(player_json)
            print("Matchup:")
            print(teams[matchup_data['teamPitching']] + " vs. " + teams[matchup_data['teamBatting']])
            print("Pitcher: ")
            if len(player_data['player']) > 0: # some of the names aren't loading
                print(player_data['player'][0]['player_name'])
            else:
                print("No announced pitcher.")
            # pretty = json.dumps(player_data, indent=4)
            # print(pretty)
    return scripts


links = getPlayerLinks()
for matchup_link in links:
    url = "https://baseballsavant.mlb.com" + matchup_link
    try:
        session = HTMLSession()
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    getPlayerData(response.content)

