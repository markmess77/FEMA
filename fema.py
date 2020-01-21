# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Creating dataframe
df = pd.read_csv('DisasterDeclarationsSummaries.csv')

# Determining disaster type frequency
disaster_frequency = df.groupby('incidentType')['disasterNumber'].nunique().reset_index()
disaster_frequency = disaster_frequency.sort_values(ascending=False, by='disasterNumber')

most_frequent = disaster_frequency.head(n=6)
most_frequent = most_frequent['incidentType']

# Renaming column
disaster_frequency.rename(columns = {'disasterNumber': 'frequency'}, inplace = True)

# Finding frequency of disasters by year 
frequency_year = df.groupby(['incidentType', 'fyDeclared'])['disasterNumber'].nunique().reset_index()
frequency_year.rename(columns = {'disasterNumber': 'frequency'}, inplace = True)

# Dropping columns to prepare for filtered dataframe
df = df.drop(['ihProgramDeclared', 'iaProgramDeclared',
       'paProgramDeclared', 'hmProgramDeclared', 'declarationDate','disasterType',
       'disasterCloseOutDate','declaredCountyArea', 'placeCode', 'hash', 'lastRefresh'], axis=1)

# Storing duration of each event in days
df['incidentBeginDate'] = pd.to_datetime(df['incidentBeginDate'])
df['incidentEndDate'] = pd.to_datetime(df['incidentEndDate'])
new_col = (df['incidentEndDate'] - df['incidentBeginDate']).dt.days
df.insert(7, 'durationDays', new_col)

# Grouping by number of disasterNumber occurrences to indicate magnitude
df = df.groupby(list(df.columns)).size().reset_index().rename(columns={0:'count'})

# Creating custom rating for intensity
df['durationDays'] += df['durationDays'].eq(0) # converting 0's to 1's
df['rating'] = df['count'] / abs(df['durationDays']) # better remove negatives  or take absolute value?

# Creating new df excluding outliers
rating_outliers = df[(np.abs(stats.zscore(df['rating'])) < 3)]
count_outliers = df[(np.abs(stats.zscore(df['count'])) < 3)]

# Finding total count/rating by year of all disaster types
df['count'] = pd.to_numeric(df['count'])
years_total = df.groupby(['fyDeclared', 'incidentType'])['count', 'rating'].sum().reset_index()

# New df only for disasters after 2000
rating_2000 = rating_outliers['fyDeclared'] >= 2000
rating_2000 = rating_outliers[rating_2000]
count_2000 = count_outliers['fyDeclared'] >= 2000
count_2000 = count_outliers[count_2000]

average_count = count_2000.groupby('incidentType')['count'].mean().reset_index()
average_rating = rating_2000.groupby('incidentType')['rating'].mean().reset_index()

# Grouping by disaster type / duration days
target = ['Hurricane', 'Flood', 'Snow', 'Tornado']
disaster_duration = df.groupby('incidentType')['durationDays', 'count', 'rating'].mean().reset_index()
x = disaster_duration['incidentType'].isin(target)
disaster_duration = disaster_duration[x]

# New df for average severity
count_severity = count_2000.groupby('incidentType')['count'].mean().reset_index()
rating_severity = rating_2000.groupby('incidentType')['rating'].mean().reset_index()
severity = pd.merge(count_severity, rating_severity, on='incidentType', how='outer')
severity = pd.merge(severity, disaster_frequency, on='incidentType', how='outer')

def boxplot(data, x, y1, y2):
    sns.set_style('darkgrid')
    temp = data[x].isin(most_frequent)
    data = data[temp]
    f, axes =  plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=False)
    
    sns.boxplot(data=data, x=x, y=y1, ax=axes[0])
    axes[0].set_title('Disaster ' + y1.capitalize(), fontsize=25)
    axes[0].set_ylabel(y1.capitalize(), fontsize=15)
    axes[0].set_xlabel('Disaster Type', fontsize=15)
    
    sns.boxplot(data=data, x=x, y=y2, ax=axes[1])
    axes[1].set_title('Disaster ' + y2.capitalize(), fontsize=25)
    axes[1].set_ylabel(y2.capitalize(), fontsize=15)
    axes[1].set_xlabel('Disaster Type', fontsize=15)
    
boxplot(rating_outliers, 'incidentType', 'count', 'rating')

def line_plot(data, x, y, hue, title=None):
    sns.set_style('darkgrid')
    temp = data[hue].isin(most_frequent)
    data = data[temp]
    
    g = sns.FacetGrid(data=data, col=hue, col_wrap=2, hue=hue)
    g.map(sns.lineplot, x, y)

line_plot(data=df, x='fyDeclared', y='incidentType', hue='incidentType')


