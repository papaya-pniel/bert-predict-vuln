#!/usr/bin/env python
# coding: utf-8

# In[28]:

# load eval_df 
import pandas as pd
eval_df = pd.read_pickle("./nvd-eval-df.pkl")


# In[24]:


from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual, Button, Layout
from random import randrange
from IPython.utils import io
from IPython.display import display, Markdown
import ipywidgets as widgets

#Supress default INFO logging 
import logging 
logger = logging.getLogger() 
logger.setLevel(logging.CRITICAL)

button = widgets.Button(description='Press Me To Start Predicting Vulnerabilities...', layout=Layout(width='90%', height='100px'), button_style='info')
out = widgets.Output()

def check_prediction_matches_real(prediction_vuln_level, actual_vuln_level): 
    if prediction_vuln_level == actual_vuln_level: 
        print("The prediction value matches the actual value!")
    else:
        print("The prediction does NOT match the actual value. The prediction is: " + str(prediction_vuln_level) + ", but the actual level is: " + str(actual_vuln_level))

def on_button_clicked(_):
      # "linking function with output"
      with out:
          # what happens when we press the button
            # variables
            rand_entry = eval_df.sample(1)
            rand_description = rand_entry['text'].iloc[0]
            with io.capture_output() as captured:
                prediction_vuln_level = model.predict([rand_description])[0][0]
            actual_vuln_level = rand_entry['labels'].iloc[0]

            # print description
            print("We have randomly picked the vulnerability: " + df.iloc[rand_entry.index[0]]["CVE_data_meta.ID"])
            
            # check if prediction of vuln matches actual vuln
            check_prediction_matches_real(prediction_vuln_level, actual_vuln_level)
          
        
# linking button and function together using a button's method
button.on_click(on_button_clicked)

# displaying button and its output together
widgets.VBox([button,out])
display(widgets.VBox([button,out]))


# In[ ]:




