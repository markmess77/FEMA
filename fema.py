# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 17:58:03 2019

@author: markm
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Creating dataframe
df = pd.read_csv(r'DisasterDeclarationsSummaries.csv')

# Determining disaster type frequency
disaster_frequency = df.groupby('incidentType')['disasterNumber'].nunique().reset_index()
disaster_frequency = disaster_frequency.sort_values(ascending=False, by='disasterNumber')

most_frequent = disaster_frequency.head(n=6)
most_frequent = most_frequent['incidentType']

# Renaming column
disaster_frequency.rename(columns = {'disasterNumber': 'frequency'}, inplace = True) 

# Dropping columns to prapre for filtered dataframe
df = df.drop(['ihProgramDeclared', 'iaProgramDeclared',
       'paProgramDeclared', 'hmProgramDeclared', 'declarationDate','disasterType',
       'disasterCloseOutDate','declaredCountyArea', 'placeCode', 'hash', 'lastRefresh'], axis=1)

# Storing duration of each event in days
df['incidentBeginDate'] = pd.to_datetime(df['incidentBeginDate'])
df['incidentEndDate'] = pd.to_datetime(df['incidentEndDate'])
df['durationDays'] = (df['incidentEndDate'] - df['incidentBeginDate']).dt.days

# Grouping by number of disasterNumber occurrences to indicate magnitude
df = df.groupby(list(df.columns)).size().reset_index().rename(columns={0:'count'})

# Creating custom rating for intensity
df['durationDays'] += df['durationDays'].eq(0) # converting 0's to 1's
df['rating'] = df['count'] / abs(df['durationDays']) # better remove negatives  or take absolute value?

# Creating new df excluding outliers
df_outliers = df[(np.abs(stats.zscore(df['rating'])) < 3)]
df_outliers = df[(np.abs(stats.zscore(df['count'])) < 3)]

# Finding total count/rating by year of all disaster types
df['count'] = pd.to_numeric(df['count'])
years_total = df.groupby(['fyDeclared', 'incidentType'])['count', 'rating'].sum().reset_index()

# New df only for diaster after 1980
after_1980 = years_total['fyDeclared'] >= 1980
after_1980 = years_total[after_1980]

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
    
boxplot(df_outliers, 'incidentType', 'count', 'rating')

def line_plot(data, x, y, hue, title=None):
    sns.set_style('darkgrid')
    temp = data[hue].isin(most_frequent)
    data = data[temp]
    
    g = sns.FacetGrid(data=data, col=hue, col_wrap=2, hue=hue)
    g.map(sns.lineplot, x, y)

line_plot(data=after_1980, x='fyDeclared', y='rating', hue='incidentType')


