import requests
from bs4 import BeautifulSoup

def getPlayerLinks():
    initial_requests = requests.get('https://baseballsavant.mlb.com/probable-pitchers')

    soup = BeautifulSoup(initial_requests.content, 'html.parser')

    hrefs = [a['href'] for a in soup.find_all('a', class_='matchup-link')]

    unique_links = list(set(hrefs))

    return unique_links

def getPitcherName(matchup_response):
    soup = BeautifulSoup(matchup_response.content, 'html.parser')

    return soup.find_all('tr', id='player_table-tr_0')



links = getPlayerLinks()
for matchup_link in links:
    matchup_response = requests.get("https://baseballsavant.mlb.com" + matchup_link)
    pitcher_name = getPitcherName(matchup_response)
    print(pitcher_name)

