import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.mlb.com/stats/'

response = requests.get(url)

while response.status_code == 200:

    soup = BeautifulSoup(response.content,'html.parser')

    table = soup.find('table')


# Extract rows
    
    rows2 = []
    for row in table.find_all('tr')[1:]: 
        name = [col.text.strip() for col in row.find_all('th')]
        stats = [col.text.strip() for col in row.find_all('td')]
        appended_row = [name[0]]
        
        for stat in stats:
            appended_row.append(stat)
        
        rows2.append(appended_row)

    



else:
    print( f"Failed to retried data.\nSatus code {response.status_code}")

df = pd.DataFrame(rows2)
df.columns = ['Player','Team','G','AB','R','H','2B','3B','HR','RBI','BB','SO','SB','CS','AVG','OBP','SLG','OPS']
df.to_csv("MLB_Stats2.csv",index = False)

