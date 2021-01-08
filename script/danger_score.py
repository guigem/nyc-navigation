from regex import add_termination, remove_houses_numbers
import pandas as pd
import re

crash_data = 'data_100000_out_final.csv'
df = pd.read_csv(crash_data)

#drop_list = ['off_street_name', ]

#df = df.drop(df.loc[:, 'Accelerator Defective':'Van'].columns, axis=1)
#df = df.drop(drop_list, axis=1)


#Calculate the dangerous score based on dummy variable values of different columns
def dangerous_score_global(df:pd.DataFrame) -> int:
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


def dangerous_score_pedestrians(df:pd.DataFrame) -> int:
    x = 1

    if df['pedestrians_killed'] == 1:
        x += 2
    if df['pedestrians_injured'] == 1:
        x += 1
    
    return x

def dangerous_score_cyclists(df:pd.DataFrame) -> int:
    x=1

    if df['cyclist_killed'] == 1:
        x += 2
    if df['cyclist_injured'] == 1:
        x += 1
    
    return x

def dangerous_score_motorists(df:pd.DataFrame) -> int:
    x = 1

    if df['motorist_killed'] == 1:
        x += 2
    if df['motorist_injured'] == 1:
        x += 1
    
    return x

def dangerous_score_reversed(df:pd.DataFrame, user:str) -> pd.DataFrame:
    column = df[f"danger_score_{user}"]
    max_danger_score = column.max()

    df[f"reversed_danger_score_{user}"] = max_danger_score

    df[f"reversed_danger_score_{user}"] = df[f"reversed_danger_score_{user}"] - df[f"danger_score_{user}"]

    return df

# Add dangers scores columns in the database.
df['danger_score_global'] = df.apply(dangerous_score_global, axis = 1)
df['danger_score_pedestrians'] = df.apply(dangerous_score_pedestrians, axis = 1)
df['danger_score_cyclists'] = df.apply(dangerous_score_cyclists, axis = 1)
df['danger_score_motorists'] = df.apply(dangerous_score_motorists, axis = 1)

# Clean streets names.
df['on_street_name'] = df['on_street_name'].apply(add_termination)
df['on_street_name'] = df['on_street_name'].apply(remove_houses_numbers)

# Group data by streets names.
columns_list = ["danger_score_global", 
               "danger_score_pedestrians", 
               "danger_score_cyclists", 
               "danger_score_motorists", 
               ]
street = df.groupby('on_street_name')[columns_list].sum()

# Add the reversed danger scores in the database.
dangerous_score_reversed(street, "global")
dangerous_score_reversed(street, "pedestrians")
dangerous_score_reversed(street, "cyclists")
dangerous_score_reversed(street, "motorists")

street.reset_index(inplace = True)

street.to_csv("street.csv", index=False)
