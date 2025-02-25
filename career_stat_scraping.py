import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

url = 'https://www.mlb.com/stats/all-time-totals'
page = "?page="
page_num = 2
max_page_num = 818
batting = pd.read_csv('MLB_Batting.csv')

def fetch_page(page_num):
    response = requests.get(url + page + str(page_num))
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    rows = []

    if table:
        for row in table.find_all('tr')[1:]:
            name = [col.text.strip() for col in row.find_all('th')]
            stats = [col.text.strip() for col in row.find_all('td')]

            if name:
                name[0] = re.sub(r'[^a-zA-Z]', '', name[0])
                player_row = batting[batting['Player'].str.contains(name[0], case=False, regex=False)]

                if not player_row.empty:
                    appended_row = [name[0], player_row['Team'].values[0]] + stats
                    rows.append(appended_row)

    return rows

all_rows = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(fetch_page, range(page_num, max_page_num))

    for result in results:
        all_rows.extend(result)

if all_rows:
    df = pd.DataFrame(all_rows, columns=['Player', 'Team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS'])
    df.to_csv("MLB_Career_Batting.csv", index=False)

# Pitching stats scraping
p_url = "https://www.mlb.com/stats/pitching/all-time-totals"
page_num = 2
max_page_num = 471
pitching = pd.read_csv('MLB_Pitching.csv')

def fetch_pitching_page(page_num):
    response = requests.get(p_url + page + str(page_num))
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    rows = []

    if table:
        for row in table.find_all('tr')[1:]:
            name = [col.text.strip() for col in row.find_all('th')]
            stats = [col.text.strip() for col in row.find_all('td')]

            if name:
                name[0] = re.sub(r'[^a-zA-Z]', '', name[0])
                player_row = pitching[pitching['Player'].str.contains(name[0], case=False, regex=False)]

                if not player_row.empty:
                    appended_row = [name[0], player_row['Team'].values[0]] + stats
                    rows.append(appended_row)

    return rows

all_pitching_rows = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(fetch_pitching_page, range(page_num, max_page_num))

    for result in results:
        all_pitching_rows.extend(result)

if all_pitching_rows:
    dfp = pd.DataFrame(all_pitching_rows, columns=['Player', 'Team', 'W', 'L', 'ERA', 'G', 'GS', 'CG', 'SHO', 'SV', 'SVO', 'IP', 'H', 'R', 'ER', 'HR', 'HB', 'BB', 'SO', 'WHIP', 'AVG'])
    dfp.to_csv("MLB_Career_Pitching.csv", index=False)