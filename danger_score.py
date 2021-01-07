
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
mpl.use("TKAgg")
from datetime import datetime
from dateutil import parser
import re

crash_data = 'nyc_database.csv'
df = pd.read_csv(crash_data, low_memory=False)

drop_list = ['off_street_name', ]

df = df.drop(df.loc[:, 'Accelerator Defective':'Van'].columns, axis=1)
df = df.drop(drop_list, axis=1)

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
df['danger_score'] = df.apply(dangerous_score)

street = df.grouby(['on_street_name']).count()

print(df.head())
