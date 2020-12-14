# Intoduction

From the [National Vulnerability Database](https://nvd.nist.gov/vuln), we use the vulnerabilities to fine tune the BERT transformer model in order to predict the severity of vulnerabilities. 

We use the [Simple Transformers](https://github.com/ThilinaRajapakse/simpletransformers) library, which is based on the [Transformers](https://github.com/huggingface/transformers) library by HuggingFace. Simple Transformers lets you quickly train and evaluate Transformer models. 

# Data Feeds

You can find the data from the [NVD data-feeds](https://nvd.nist.gov/vuln/data-feeds), which can also be in the folder `data/nvdcve-1.1-200{x}.json`. 
