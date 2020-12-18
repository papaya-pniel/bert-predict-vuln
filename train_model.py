#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
# Load train and test data frames
train_df = pd.read_pickle("./nvd-train-df.pkl")
eval_df = pd.read_pickle("./nvd-eval-df.pkl")


# In[3]:


# install the simpletransformers and pytorch library to train the model
get_ipython().system(' pip install simpletransformers')
get_ipython().system(' pip install torchvision ')


# In[4]:


from simpletransformers.classification import ClassificationModel, ClassificationArgs
import logging
import torch
import torchvision

# set logggin messages
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

# Optional model configuration
model_args = ClassificationArgs(num_train_epochs=1)


# In[6]:


# Create a ClassificationModel
model = ClassificationModel(
    'bert',
    'bert-base-cased',
    num_labels=3,
    args=model_args, 
#     args={'reprocess_input_data': True}, 
    use_cuda=False,
) 

# Train the model
model.train_model(train_df)


# In[12]:


# once the model runs, it is saved in "./outputs", so you can load the model from there without having to train again
model = ClassificationModel(
    "bert",
    "./outputs",
    num_labels=3,
    use_cuda=False
)


# In[8]:


# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_df[:6000])


# In[13]:


# Make predictions with the model
predictions, raw_outputs = model.predict(['INSERT_A_DESCRIPTION_FROM_eval_df'])


# In[7]:


# check accuracy of model
len(wrong_predictions)/len(eval_df[:6000])*100


# In[ ]:




