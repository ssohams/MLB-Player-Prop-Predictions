import pandas as pd

batting = pd.read_csv('MLB_Batting.csv')
pitching = pd.read_csv('MLB_Pitching.csv')

batting_team = batting.groupby('Team').agg({'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum', '2B': 'sum', '3B': 'sum', 'HR': 'sum',
    'RBI': 'sum', 'BB': 'sum', 'SO': 'sum', 'SB': 'sum', 'CS': 'sum', 'AVG': 'mean',
    'OBP': 'mean', 'SLG': 'mean', 'OPS': 'mean'
}).reset_index()

pitching_team = pitching.groupby('Team').agg({
    'W': 'sum', 'L': 'sum', 'ERA': 'mean', 'G': 'sum', 'GS': 'sum', 'CG': 'sum', 'SHO': 'sum',
    'SV': 'sum', 'SVO': 'sum', 'IP': 'sum', 'H': 'sum', 'R': 'sum', 'ER': 'sum', 'HR': 'sum',
    'HB': 'sum', 'BB': 'sum', 'SO': 'sum', 'WHIP': 'mean', 'AVG': 'mean'
}).reset_index()

team_stats = pd.merge(batting_team, pitching_team, on = 'Team')

matchups = []
teams = team_stats['Team'].unique()

for i, team_a in enumerate(teams):
    for team_b in teams[i+1:]:
        matchups.append((team_a,team_b))

matchup_data = []
for team_a,team_b in matchups:
    stats_a = team_stats[team_stats['Team'] == team_a].iloc[0]
    stats_b = team_stats[team_stats['Team'] == team_b].iloc[0]
    features = stats_a.tolist() + stats_b.tolist()
    matchup_data.append(features)

columns = [f'TeamA_{col}' for col in team_stats.columns] + [f'TeamB_{col}' for col in team_stats.columns]
matchup_df = pd.DataFrame(matchup_data, columns=columns)

matchup_df['Target'] = (matchup_df['TeamA_W'] / (matchup_df['TeamA_W'] + matchup_df['TeamA_L'])) > \
                       (matchup_df['TeamB_W'] / (matchup_df['TeamB_W'] + matchup_df['TeamB_L']))
matchup_df['Target'] = matchup_df['Target'].astype(int)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

X = matchup_df.drop(columns=['Target', 'TeamA_Team', 'TeamB_Team'])
y = matchup_df['Target']

X.to_csv('X')
y.to_csv('y')

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.8,random_state=12)

model = RandomForestClassifier(random_state=12)
model.fit(X_train,y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))


y_pred_proba = model.predict_proba(X_test)

win_probability = y_pred_proba[:,1]

print(win_probability)
print(y_pred)
