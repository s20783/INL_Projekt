# -*- coding: utf-8 -*-
"""INL_Michał_Ostrowski_s20783.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18PuO0boLkWVFnQq1qEJcvcBSVXwL6fhg
"""

!pip install wandb -qqq
!pip install -q simpletransformers
!pip install requests
!pip install sacremoses
import wandb
import pandas as pd
import sklearn
wandb.login()

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from simpletransformers.classification import ClassificationModel, ClassificationArgs
from google.colab import drive
import os
drive.mount('/content/drive')
os.chdir('/content/drive/My Drive/')

df = pd.read_csv("daneINL.csv", encoding="ISO-8859-1")

def preprocess_file():
  a = df[df.iloc[:, 0] != df.iloc[:, 1]]
  tekst = a.iloc[:, 0].tolist() + a.iloc[:, 1].tolist()
  label = [0] * len(a) + [1] * len(a)
  new_df = pd.DataFrame({'Tekst': tekst, 'Label': label})
  return new_df

df = preprocess_file()
print(df)

train_ratio = 0.75
dev_ratio = 0.15
test_ratio = 0.1

train_df, temp_df = train_test_split(df, test_size=(1 - train_ratio), random_state=32)
eval_df, test_df = train_test_split(temp_df, test_size=test_ratio/(test_ratio + dev_ratio), random_state=32)

model_type = "herbert"
model_name = "allegro/herbert-base-cased"
# model_type = "distilbert"
# model_name = "distilbert-base-uncased"

train_args = {
    'evaluate_during_training': True,
    'num_train_epochs': 4,
    'save_eval_checkpoints': False,
    'train_batch_size': 8,
    'eval_batch_size': 8,
    'overwrite_output_dir': True,
    'wandb_project': "INL_projekt_s20783",
}

model = ClassificationModel(
    model_type,
    model_name,
    use_cuda=False,
    cuda_device=0,
    num_labels=2,
    args=train_args
)

model.train_model(train_df, eval_df=eval_df)
result, model_outputs, wrong_predictions = model.eval_model(test_df)
print(result)


dev_predictions, dev_raw_outputs = model.predict(eval_df.iloc[:,0].tolist())
dev_f1 = f1_score(eval_df.iloc[:,1].tolist(), dev_predictions)
dev_accuracy = accuracy_score(eval_df.iloc[:,1].tolist(), dev_predictions)

print("F1-Score:", dev_f1)
print("Accuracy:", dev_accuracy)


test_predictions, test_raw_outputs = model.predict(test_df.iloc[:,0].tolist())
test_f1 = f1_score(test_df.iloc[:,1].tolist(), test_predictions)
test_accuracy = accuracy_score(test_df.iloc[:,1].tolist(), test_predictions)

print("Test F1-Score:", test_f1)
print("Test Accuracy:", test_accuracy)