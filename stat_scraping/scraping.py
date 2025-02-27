import requests
from bs4 import BeautifulSoup
import pandas as pd

import re
url = 'https://www.mlb.com/stats/'

response = requests.get(url)
page = "?page="
page_num = 2
df = pd.DataFrame()
content = True
while content:

    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')

    rows2 = []
    for row in table.find_all('tr')[1:]: 
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        name[0] = re.sub(r'[^a-zA-Z]', '', name[0])
        appended_row = [name[0]]
        
        for stat in stats:
            appended_row.append(stat)
        
        rows2.append(appended_row)

    new_data = pd.DataFrame(rows2)
    df = pd.concat([df, new_data], ignore_index=True)

    response = requests.get(url+page+str(page_num))
    
    page_num+=1
    if len(rows2) == 0:
        content = False

    





df.columns = ['Player','Team','G','AB','R','H','2B','3B','HR','RBI','BB','SO','SB','CS','AVG','OBP','SLG','OPS']
df.to_csv("CSV_Files\MLB_Batting.csv",index = False)

pitching_url = "https://www.mlb.com/stats/pitching"
sort = "&sortState=asc"
page_num = 1

pitch = pd.DataFrame()
content = True
while content:
    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')

    rows2 = []
    for row in table.find_all('tr')[1:]: 
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        name[0] = re.sub(r'[^a-zA-Z]', '', name[0])
        appended_row = [name[0]]
        
        for stat in stats:
            appended_row.append(stat)
        
        rows2.append(appended_row)


    new_data = pd.DataFrame(rows2)
    
    pitch = pd.concat([pitch, new_data], ignore_index=True)

    response = requests.get(pitching_url + page + str(page_num))
    
    page_num+=1
    if page_num != 2 and len(rows2) == 0:
        content = False

pitch.columns = ["Player","Team","W","L",'ERA','G',"GS","CG","SHO","SV","SVO","IP","H","R","ER","HR","HB","BB","SO","WHIP","AVG"]
pitch.to_csv("CSV_Files\MLB_Pitching.csv",index = False)


