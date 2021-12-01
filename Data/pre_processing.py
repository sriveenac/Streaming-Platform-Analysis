#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[ ]:


netflix = pd.read_csv('Data/netflix_titles.csv')
netflix['platform'] = 'netflix'
prime = pd.read_csv('Data/amazon_prime_titles.csv')
prime['platform'] = 'prime'
disney = pd.read_csv('Data/disney_plus_titles.csv')
disney['platform'] = 'disney'
hulu = pd.read_csv('Data/hulu_titles.csv')
hulu['platform'] = 'hulu'
all = pd.concat([netflix,prime,disney,hulu])


# In[ ]:


#more clean up for rating and duration
cond=all['rating'].str.contains("Season|min",na=False)
all.loc[cond, ['rating', 'duration']] = all.loc[cond, [ 'duration','rating']].values 
all['rating']=all['rating'].fillna('NOT RATED')
#all['rating']=all['rating'].fillna(np.nan)

all['rating']=all['rating'].replace(['TV-MA','R','18+','AGES_18_','NC-17','16+','16','AGES_16_'],[18]*8)
all['rating']=all['rating'].replace(['13+','TV-14','PG-13'],[13]*3)
all['rating']=all['rating'].replace(['ALL_AGES','ALL','G','TV-G','TV-Y'],[0]*5)
all['rating']=all['rating'].replace(['PG','TV-PG','7+','TV-Y7','TV-Y7-FV'],[7]*5)
all['rating']=all['rating'].replace(['UR','NR','UNRATED','NOT RATED','NOT_RATE','TV-NR','nan'],['NOT RATED']*7)


# In[ ]:


# Data clean up
all.duration = all.duration.str.split(' ')
def get_val(x,y = 'Seasons'):
    if isinstance(x,float):
        pass
      elif x[1] == y or x[1] == y[:-1]:
        return x[0]
all["num_seasons"] = all.duration.apply(lambda x: get_val(x, 'Seasons'))
all["length"] = all.duration.apply(lambda x: get_val(x, 'mins') )
all = all.fillna(value=np.nan)
all.duration = all.duration.astype(str)
all.length = all.length.astype(float)
all.num_seasons = all.num_seasons.astype(float)


# In[ ]:


master = all.loc[:,['show_id', 'type', 'title','release_year','rating','duration','listed_in','description','platform']]
master = master.dropna()
master = master[master.platform != 'hulu']
country = all[~all.platform.isin(['prime', 'hulu'])] # analyze the countries
added = all[~all.platform.isin(['prime'])] # when things are being added


# In[ ]:


all.to_csv('all_data_processed.csv')
master.to_csv('master_processed.csv')
country.to_csv('country_analyis_processed.csv')
added.to_csv('release_year_analysis_processed.csv')

