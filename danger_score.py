from regex import add_termination, remove_houses_numbers
import pandas as pd
import re

crash_data = 'data_100000_out_final.csv'
df = pd.read_csv(crash_data)

#drop_list = ['off_street_name', ]

#df = df.drop(df.loc[:, 'Accelerator Defective':'Van'].columns, axis=1)
#df = df.drop(drop_list, axis=1)

#print(df.columns)

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
df['danger_score'] = df.apply(dangerous_score, axis = 1)

df['on_street_name'] = df['on_street_name'].apply(add_termination)
df['on_street_name'] = df['on_street_name'].apply(remove_houses_numbers)


street = df.groupby('on_street_name')['danger_score'].sum()
#print(type(street))


street_test = street.to_frame()
street_test.reset_index(inplace = True)


#print(street_test)

street_test.to_csv("street.csv", index=False)


#print(df.head())
