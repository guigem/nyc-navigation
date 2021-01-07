
import pandas as pd
import numpy as np


crash_data = 'nyc_database.csv'
df = pd.read_csv(crash_data, low_memory=False)


# Remove any blank spaces
def strip_str(x):
    if type(x) is str:
        return x.strip()
    return x
data = df.applymap(strip_str)


#Calculate the dangerous score based on dummy variable values of different columns
def dangerous_score(df):
    '''
    Score based on values in dummy variables
    If someone was killed, add 2 to the score
    If someone was injured, add 1 to the score
    The higher the score, the greater the street is dangerous
    Start score with 1 as an accident still occurred.
    '''
    x = 1
    if df['persons_killed'] == 1:
        x += 2
    if df['persons_injured'] == 1:
        x += 1
    if df['pedestrians_killed'] == 1:
        x += 2
    if df['pedestrians_injured'] == 1:
        x += 1
    if df['cyclist_killed'] == 1:
        x += 2
    if df['cyclist_injured'] == 1:
        x += 1
    if df['motorist_killed'] == 1:
        x += 2
    if df['motorist_injured'] == 1:
        x += 1
    return x

# Add the danger score column in the database
df['danger_score'] = df.apply(dangerous_score, axis=1)

# Melvin's function :)
df['on_street_name'] = df(remove_houses_numbers).apply
df['on_street_name'] = df(add_termination).apply

# Sum the danger_score based on on_street_name
street = df.grouby('on_street_name')['danger_score'].count()

df_final = pd.DataFrame(df[["danger_score",'on_street_name']])

df_final.to_csv('df_final.csv')
