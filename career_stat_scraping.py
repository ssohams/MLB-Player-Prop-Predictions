import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.mlb.com/stats/all-time-totals'

response = requests.get(url)
page = "?page="
page_num = 2
df = pd.DataFrame()
batting = pd.read_csv('MLB_Batting.csv')
if batting['Player'].str.contains('1AaronA JudgeJudgeCF1'):
    print('HES THERE')
while page_num < 818:
    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')

    rows = []
    for row in table.find_all('tr')[1:]:
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        
        if name:
            player_row = batting[batting['Player'].str.contains(name[0], case=False, regex=False)]
            
            if not player_row.empty:
                appended_row = [name[0],player_row['Teams'].values[0]] + stats
                rows.append(appended_row)


    if rows:
        data = pd.DataFrame(rows)
        df = pd.concat([df,data],ignore_index = True)
        print(f"Page {page_num-1}: Added {data.shape[0]} rows.")
        print(data.shape)
    else:
        print(f"Page {page_num-1}: No matching players found.")
    response = requests.get(url+page+str(page_num))
    
    page_num += 1

df.columns = ['Player','Team','G','AB','R','H','2B','3B','HR','RBI','BB','SO','SB','CS','AVG','OBP','SLG','OPS']
df.to_csv("MLB_Career_Batting.csv",index = False)

##############################
##############################
##############################
##############################
##############################
##############################
##############################
##############################


p_url = "https://www.mlb.com/stats/pitching/all-time-totals"
page = "?page="
page_num == 2

dfp = pd.DataFrame()
pitching = pd.read_csv('MLB_Pitching.csv')
while page_num < 471:
    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')

    rows = []
    for row in table.find_all('tr')[1:]:
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        
        
        if name[0] in pitching['Player'].values:
            player_row = pitching[pitching['Player'] == name[0]]
            appended_row = [name[0], player_row['Teams'].values[0]]

            for stat in stats:
                appended_row.append(stat)
            rows.append(appended_row)
    if rows:
        data = pd.DataFrame(rows)
        dfp = pd.concat([dfp, data], ignore_index=True)

    response = requests.get(p_url + str(page_num))
    print(f'page {page_num-1} complete')
    page_num += 1

dfp.columns = ['Player','Team','W','L','ERA','G','GS','CG','SHO','SV','SVO','IP','H','R','ER','HR','HB','BB','SO','WHIP','AVG']
df.to_csv("MLB_Career_Pitching.csv",index = False)