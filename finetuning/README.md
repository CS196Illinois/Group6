# Finetuning

This readme describes all the files and directories in this finetuning folder. This file will store everything **except** the actual language models. They are too large to store on GitHub. However, they can be easily generated locally by running code from the FineTuneWithCustomDataset.ipynb file. There will be instructions below. There will be folders corresponding to each model trained as we progress. These folders will contain the logs generated while training, the vocab files, and any additional logs. The training logs indicate the rouge metrics and loss over time.

## FineTuneWithCustomDataset.ipynb

The file itself contains comments on the functionality of each block of code, but I will describe its general use here. It is used to format the transcripts and summaries we generated into the required training/testing/validation files used when finetuning a pre-existing language model. It also contains the code to finetune and generate summaries with a finetuned language model. It draws upon examples from the transformers GitHub page. 

This code **NEEDS** to be run from Google Colab on a GPU. You will also find that the language models it generates take multiple GBs of storage each, so unlimited Google Drive storage with your illinois account will be your best friend. I have tried to run this code on a local jupyter environment to no avail, so that will not work either.

We will need to create another notebook that runs its own code (not from an example) later down the line. This notebook serves as a good tool to use to select out language model. We will do so by analyzing the metric logs generated from finetuning in each respective language model folder generated.

*Note: You will not be able to push the entire language model to GitHub. Just try and push the metrics.json, best_tfmr/config.json, best_tfmr/tokenizer_config.json, and best_tfmr/vocab.json, files to the branch. When needed, we can create the finetuned language model locally.*

## Transcripts_To_Format

This directory stores **most** of the custom datasets we generated. We will need to work on shortening each of the entries in them to a 1024 word capped transcript and 156 word capped summary in order to take advantage of every word. Some lecture transcripts were not included since they may have had bad data (bullet points, unusable summaries). We will need to work on converting these transcripts and summaries to usable data. 

As of right now, the files in this directory are used to generate the training/testing/validation files. Once we split these files into shorter summaries and transcripts, running some code in FineTuneWithCustomDataset.ipynb will overwrite the current files used for training/testing/validation. 

Splitting entries into smaller entries will take some manual human work (*sigh*) since it is kinda tough to do it with code. 

## Seq2Seq

This directory contains all the example code required from the transformers GitHub to finetune a summarization model. Ideally, we will write our own scripts to finetune, but these serve out purpose for now. The FineTuneWithCustomDataset.ipynb uses code from these files to finetune a specified model and create a folder containing the new finetuned language model. 

## Lecture_Transcripts

This directory contains the training/testing/validation data used when finetuning the language model. As described above, we will need to overwrite these files with the shorter transcripts/summaries to take advantage of every single word. At the moment, the code simply truncates any long text entries and moves along. 
