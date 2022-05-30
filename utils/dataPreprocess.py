import pandas as pd
import numpy as np
import os

def process():
    df_ner = pd.read_csv('ner_tag.csv', header=None) 
    df_ner.columns = ['word', 'tag', 'intent']
    
    df_intent = pd.read_csv('./models/intent/Intent_train_data.csv', header=None) 
    df_intent.columns = ['sentence', 'intent', 'intent_info']
    df_intent = df_intent.drop_duplicates()
    
    result = pd.DataFrame({0:[np.nan], 1:[np.nan], 'tag':[np.nan]})
    sentence = []
    
    for intent in df_intent:
        
    
    
    return df_intent