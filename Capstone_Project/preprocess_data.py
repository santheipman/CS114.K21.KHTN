# -*- coding: utf-8 -*-
from underthesea import word_tokenize
import re
import VietnameseTextNormalizer as nm
import pandas as pd
import numpy as np


"""Load stop word list"""
file = open('vietnamese-stopwords.txt')
stop_words = file.readlines()
file.close()

stop_words = set([word.strip('\n') for word in stop_words])
stop_words


"""Function to remove consecutive duplicates: nhaaaa -> nha"""
def removeConsecutiveDuplicates(S): 
    S = list(S.rstrip()) 
    
    n = len(S)  
    
    if (n < 2) : 
        return S[0]
           
    j = 0
       
    for i in range(n):  
        if (S[j] != S[i]): 
            j += 1
            S[j] = S[i]  
      
    j += 1
    S = S[:j]
    return "".join(S)


"""Function to preprocessing the data"""
def preprocessing(s, show_stepbystep=False):
    if show_stepbystep:
        print("original:")
        print(s)
        print()
    
    # remove 'Xem thêm'
    s = re.sub('Xem thêm', '', s)
    if show_stepbystep:
        print("remove xt:")
        print(s)
        print()

    # convert to lower case
    s = s.lower()
    if show_stepbystep:
        print("lowercase:")
        print(s)
        print()
    
    # normalize Vietnamese
    s = nm.ASRNormalize(s)
    if show_stepbystep:
        print("normalized Vietnamese:")
        print(s)
        print()
        
    # remove urls
    s = re.sub(r'http\S+', '', s)
    if show_stepbystep:
        print('remove urls:')
        print(s)
        print()
    
    # remove email address
    s = re.sub(r'\S*@\S*\s?', '', s)
    if show_stepbystep:
        print('remove email addresses:')
        print(s)
        print()
    
    # split into words
    tokens = word_tokenize(s)
    if show_stepbystep:
        print('tokenize:')
        print(tokens)
        print()
    
    # remove punctuation and number
    words = [word for word in tokens if re.sub(r"\s+", "", word).isalpha()]
    if show_stepbystep:
        print('remove punctuation:')
        print(words)
        print()
    
    # filter out stop words
    words = [word for word in words if not word in stop_words]
    if show_stepbystep:
        print('remove stop words:')
        print(words)
        print()
    
    # remove consecutive duplicates character
    words = [removeConsecutiveDuplicates(word) for word in words]
    if show_stepbystep:
        print('remove consecutive duplicates character:')
        print(words)
        print()
        
    # remove single character
    words = [word for word in words if len(word)>1]
    if show_stepbystep:
        print('remove single character:')
        print(words)
        print()
    
    return words
    
    
"""Load raw data"""
k13 = pd.read_csv("k13/posts_1594221437_1.csv", header=None)
k14 = pd.read_csv("k14/posts_1594216235_1.csv", header=None)

to = pd.concat([k13, k14], ignore_index=True)


"""Preprocess the data"""
to[1] = [preprocessing(to.iloc[i][0]) for i in range(to.shape[0])]
to[2] = [' '.join(to.iloc[i][1]) for i in range(to.shape[0])]

# drop duplicates
to = to.drop_duplicates(ignore_index=True, subset=2)
