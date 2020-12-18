# Intoduction

From the [National Vulnerability Database](https://nvd.nist.gov/vuln), we use software/hardware vulnerabilities to tune the BERT transformer model in order to predict the severity of said vulnerabilities.

We use the [Simple Transformers](https://github.com/ThilinaRajapakse/simpletransformers) library, which is based on the [Transformers](https://github.com/huggingface/transformers) library by HuggingFace. Simple Transformers lets you quickly train and evaluate Transformer models. We also have a wrapper to classify the different vulnerabilities.

# Data Feeds

You can find the data from the [NVD data-feeds](https://nvd.nist.gov/vuln/data-feeds) in the folder `data/nvdcve-1.1-200{x}.json`. 


# Cleaning the data 

By manipulating the description of the data, and removing some of the entries themselves, you can increase the accuracy of the model (which is trained on the decriptions of software/hardware vulnerabilities). 

Entries were dropped from the data frame that have NaN values as a description. There are three different states of CVE records: reserved, disputed and rejected, which were all removed. 

**RESERVED**
: A CVE Record is marked as "RESERVED" when it has been reserved for use by a CVE Numbering Authority (CNA) or security researcher, but the details of it are not yet populated. 

**DISPUTED**
: When one party disagrees with another party's assertion that a particular issue in software is a vulnerability, a CVE Record assigned to that issue may be designated as being "DISPUTED".

**REJECT**
: A CVE Record listed as "REJECT" is a CVE Record that is not accepted as a CVE Record. The reason a CVE Record is marked REJECT will most often be stated in the description of the CVE Record.

For that reason, data entried with the above label have been removed. and can be seen through the following line of code in the notebook: 

```
df_model = df_model.drop(df_model[df_model['text'].str.contains('^\*\*', regex=True)].index)
```

Around 80% of the data has version numbers in the descriptions, which we removed to make it easier for the algorithm to spot differences between descriptions for different severity levels. You can see this being done in the following code in the notebook: 

``` 
for i in df_model[df_model['text'].str.contains('(\d+\.)?(\d+\.)?(x|\*|\d+).', regex=True)].index:
    df_model.loc[i, 'text'] = re.sub('(\d+\.)?(\d+\.)?(x|\*|\d+).', '', df_model.loc[i, 'text']) 
``` 

# The Classification Model

The aim of this classification Model is to classify a description of a CVE from NVD into one of 3 classes: low, medium, or high. A transformer-based multi-class text classification model typically consists of a transformer model with a classification layer on top of it: in our instance we have chosen to use the [BERT transformer](https://en.wikipedia.org/wiki/BERT_(language_model)#:~:text=Bidirectional%20Encoder%20Representations%20from%20Transformers,and%20his%20colleagues%20from%20Google.) The classification layer has 3 output neurons, corresponding to each of the three classes (low, medium, and high vulnerabilities).

To create a `ClassificationModel`, the `model_type` and `model_name` variables must be specified. However, you can select any one of the model types from the [supported models](https://simpletransformers.ai/docs/classification-specifics/). See the [Simple Transformers](https://simpletransformers.ai/docs/classification-models/#classificationmodel) for extensive documentation. 

Once you have your data prepared, to create and train the model only the following lines of code are requires: 

```
# Create a ClassificationModel
model = ClassificationModel(
    'bert',
    'bert-base-cased',
    num_labels=3,
    args=model_args, 
    use_cuda=True,
) 

# Train the model
model.train_model(train_df)

```

The parameter `num_labels=3` is used for our multi-class classification. If you are using GPU then you can set `use_cuda=True`, otherwise set to `False`. 

