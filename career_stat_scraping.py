import requests
from bs4 import BeautifulSoup
import pandas as pd

import re

url = 'https://www.mlb.com/stats/all-time-totals'

response = requests.get(url)
page = "?page="
page_num = 2
df = pd.DataFrame()
batting = pd.read_csv('MLB_Batting.csv')


#print(batting[batting['Player'].str.contains('1AaronA JudgeJudge', case=False, na=False)])

while page_num < 818:
    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')

    rows = []
    for row in table.find_all('tr')[1:]:
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        
        appended_row = [name[0]]
        for stat in stats:
            appended_row.append(stat)
        rows.append(appended_row)

    if rows:
        data = pd.DataFrame(rows)
        df = pd.concat([df,data],ignore_index = True)
        print(f"Page {page_num-1}: Added {data.shape[0]} rows.")

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
page_num = 2

dfp = pd.DataFrame()
pitching = pd.read_csv('MLB_Pitching.csv')
response = requests.get(p_url)
while page_num < 471:
    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')

    rows = []
    for row in table.find_all('tr')[1:]:
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        
        appended_row = [name[0]]
        for stat in stats:
            appended_row.append(stat)
        rows.append(appended_row)
   
    if rows:
        data = pd.DataFrame(rows)
        dfp = pd.concat([dfp, data], ignore_index=True)
        print(f'Page {page_num-1}: Added {data.shape[0]} rows.')
    else:
        print(f'Page {page_num-1}: No matching players found.')  

    response = requests.get(p_url + page + str(page_num))
    page_num += 1

dfp.columns = ['Player','Team','W','L','ERA','G','GS','CG','SHO','SV','SVO','IP','H','R','ER','HR','HB','BB','SO','WHIP','AVG']
dfp.to_csv("MLB_Career_Pitching.csv",index = False)