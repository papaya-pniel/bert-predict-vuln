#!/usr/bin/env python
# coding: utf-8

# In[49]:


import pandas as pd
import numpy as np
import os
import json
import re


# In[50]:


from pandas.io.json import json_normalize
data = pd.read_json("data/nvdcve-1.1-2002.json")
df = pd.DataFrame(data)
df = pd.json_normalize(df['CVE_Items'])
df


# In[27]:


#extracting description from description.description_data
cve_description = []
cve_desc_index = df["cve.description.description_data"].index
for x in df["cve.description.description_data"]:
    try: 
        cve_description.append(x[0]["value"])

    except IndexError:
        cve_description.append("NO INFO")
cve_description = pd.Series(cve_description, index = cve_desc_index)
print(cve_description)


# In[32]:


#extract cvssV2 score
cvssV2_score = df["impact.baseMetricV2.cvssV2.baseScore"].dropna()
cvssV2_score_desc_index = cvssV2_score.index

cvssV2_score = cvssV2_score.mask(cvssV2_score < 3.9, 0)
cvssV2_score = cvssV2_score.mask((cvssV2_score > 3.9) & (cvssV2_score < 7.0), 1)
cvssV2_score = cvssV2_score.mask(cvssV2_score > 7.0, 2)

cvssV2_score_numeric = pd.Series(cvssV2_score, index = cvssV2_score_desc_index)


# In[30]:


# create pandas dataframe that the model can ingest
df_model = pd.DataFrame({
    'text': cve_description,
    'labels': cvssV2_score_numeric,
})


# In[34]:


# removes lines with leftover NaN values
df_model['labels'] = df_model['labels'].fillna(9)
df_model = df_model.drop(df_model[df_model['labels']==9].index)
df_model = df_model.drop(df_model[df_model['labels']==7].index)


# In[36]:


# change labels column from float to int for the model
df_model['labels'] = pd.to_numeric(df_model['labels'])
df_model['labels'] = df_model['labels'].astype(int)


# In[44]:


# drops entries with descriptions that start with "**"
df_model = df_model.drop(df_model[df_model['text'].str.contains('^\*\*', regex=True)].index)


# In[45]:


for i in df_model[df_model['text'].str.contains('(\d+\.)?(\d+\.)?(x|\*|\d+).', regex=True)].index:
    df_model.loc[i, 'text'] = re.sub('(\d+\.)?(\d+\.)?(x|\*|\d+).', '', df_model.loc[i, 'text'])


# In[51]:


# Save data frames
df.to_pickle("./nvd-df.pkl")
df_model.to_pickle("./nvd-df_4_model.pkl")


# In[52]:


from sklearn.model_selection import train_test_split
# split train and test data into 75% and 25%, respectively
train_df, eval_df = train_test_split(df_model, test_size=0.25, shuffle=True)


# In[53]:


# Save data frames
train_df.to_pickle("./nvd-train-df.pkl")
eval_df.to_pickle("./nvd-eval-df.pkl")


# In[1]:


# check there are no unexpected values and the count is roughly evenly spread out
train_df['labels'].value_counts()


# In[ ]:




