import pandas as pd
pd.options.mode.chained_assignment = None

batting = pd.read_csv('CSV_Files\MLB_Batting.csv')
pitching = pd.read_csv('CSV_Files\MLB_Pitching.csv')
cbattings = pd.read_csv('CSV_Files\MLB_Career_Batting.csv')
cpitching = pd.read_csv('CSV_Files\MLB_Career_Pitching.csv')

df = pd.DataFrame()
rows = []

c = cbattings['Player'].tolist()
for name in batting.iloc[:,0]:
    if name in c:
        player_row = cbattings[cbattings['Player'] == name].copy()
        team = batting[batting['Player'] == name]['Team'].values[0]
    
        player_row.loc[:, 'Team'] = team
        rows.append(player_row)
    else:
        player_row = batting[batting['Player'] == name]
        rows.append(player_row)
    df = pd.concat([df,player_row ])  
    
df.columns = batting.columns
df.fillna(0, inplace=True) 
df.to_csv('CSV_Files\MLB_Custom_Batting.csv', index=False)


dfp = pd.DataFrame()


rows = []
c = cpitching['Player'].tolist()

for name in pitching.iloc[:,0]:
    if name in c:
        player_row = cpitching[cpitching['Player'] == name].copy()
        team = pitching[pitching['Player'] == name]['Team'].values[0]
        #print(team)
        
        player_row.loc[:, 'Team'] = team
        rows.append(player_row)
    else:
      
        player_row = pitching[pitching['Player'] == name]
        rows.append(player_row)
    dfp = pd.concat([dfp,player_row ])  
    
#dfp.columns = pitching.columns
dfp.fillna(0, inplace=True) 
dfp.to_csv('CSV_Files\MLB_Custom_Pitching.csv', index=False)

