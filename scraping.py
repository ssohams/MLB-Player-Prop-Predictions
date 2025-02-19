import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.mlb.com/stats/'

response = requests.get(url)
page = "?page="
page_num = 2
df = pd.DataFrame()
while page_num < 8:

    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')

    rows2 = []
    for row in table.find_all('tr')[1:]: 
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        appended_row = [name[0]]
        
        for stat in stats:
            appended_row.append(stat)
        
        rows2.append(appended_row)

    new_data = pd.DataFrame(rows2)
    df = pd.concat([df, new_data], ignore_index=True)

    response = requests.get(url+page+str(page_num))
    
    page_num+=1

    





df.columns = ['Player','Team','G','AB','R','H','2B','3B','HR','RBI','BB','SO','SB','CS','AVG','OBP','SLG','OPS']
df.to_csv("MLB_Batting.csv",index = False)

pitching_url = "https://www.mlb.com/stats/pitching"
sort = "&sortState=asc"
page_num = 1

pitch = pd.DataFrame()

while page_num < 5:
    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')

    rows2 = []
    for row in table.find_all('tr')[1:]: 
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        appended_row = [name[0]]
        
        for stat in stats:
            appended_row.append(stat)
        
        rows2.append(appended_row)


    new_data = pd.DataFrame(rows2)
    
    pitch = pd.concat([pitch, new_data], ignore_index=True)

    response = requests.get(pitching_url + page + str(page_num) + sort)
    
    page_num+=1

pitch.columns = ["Player","Team","W","L",'ERA','G',"GS","CG","SHO","SV","SVO","IP","H","R","ER","HR","HB","BB","SO","WHIP","AVG"]
pitch.to_csv("MLB_Pitching.csv",index = False)


