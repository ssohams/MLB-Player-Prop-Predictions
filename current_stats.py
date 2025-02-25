import pandas as pd

batting = pd.read_csv('CSV_Files\MLB_Batting.csv')
pitching = pd.read_csv('CSV_Files\MLB_Pitching.csv')
cbattings = pd.read_csv('CSV_Files\MLB_Career_Batting.csv')
cpithing = pd.read_csv('CSV_Files\MLB_Career_Pitching.csv')

df = pd.DataFrame()
rows = []
c = cbattings['Player'].tolist()

for name in batting.iloc[:,0]:
    if name in c:
        player_row = cbattings[cbattings['Player'] == name]
        rows.append(player_row)
    else:
        player_row = batting[batting['Player'] == name]
        rows.append(player_row)
    df = pd.concat([df,player_row ])  
    
df.columns = batting.columns
df.to_csv('CSV_Files\MLB_Custom_Batting.csv', index=False)


dfp = pd.DataFrame()
c = cpithing['Player'].tolist()
rows = []
for name in pitching.iloc[:,0]:
    if name in c:
        player_row = cpithing[cpithing['Player'] == name]
        rows.append(player_row)
    else:
        player_row = pitching[pitching['Player'] == name]
        rows.append(player_row)
    dfp = pd.concat([dfp,player_row ])
    

dfp.columns = pitching.columns
dfp.to_csv('CSV_Files\MLB_Custom_Pitching.csv', index=False)
