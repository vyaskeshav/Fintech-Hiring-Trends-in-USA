#!/usr/bin/env python
# coding: utf-8

# # PART 1: Understanding the keywords that are frequently used in Fintech:

# In[ ]:


# list of libraries
import string
import collections
import glob
import os
import codecs
import csv

# The Natural Language Toolkit- is a suite of libraries and programs for symbolic and statistical natural language
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

# Extracting metadata and structured text content from documents
from tika import parser

# TextRank implementation
from textrank4zh import TextRank4Keyword

# Pandas and SkitLearn libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

#Global variables:
#Get default stopwords from nltk
default_stopwords = stopwords.words('english')
lemmatizer = nltk.stem.WordNetLemmatizer()


# In[ ]:


# Adding Custom stopwords
stopwords_filepath = 'custom_stopwords.txt'
stopwords_file = codecs.open(stopwords_filepath, 'r', 'utf-8')
custom_stopwords = list(stopwords_file.read().splitlines())
stopwords_file.close()
all_stopwords = default_stopwords + custom_stopwords


# In[ ]:


#Functions to clean data:
#Function removes stop words, punctuation
def clean_tokens(tokens):
    """ Lowercases, takes out punct and stopwords and short strings """
    return [token.lower() for token in tokens if (token not in string.punctuation) and 
                   (token.lower() not in all_stopwords) and len(token) > 2]

#Function to remove plurals
def lemmatize(tokens):
    """ Removes plurals """
    return [lemmatizer.lemmatize(token) for token in tokens]

#Function to create ngram, bigram, trigram
def count_ngrams(tokens,n):
    n_grams = ngrams(tokens, n)
    ngram_freq = collections.Counter(n_grams)
    ngram_freq = ngram_freq.most_common(100)
    return ngram_freq

#Function to create dictionary of words and frequencies:
def ngram_to_dict(ngram_freq):
    l = []
    for t in ngram_freq:
        l.append((' '.join(t[0]),t[1]))
    return dict(l)


# In[ ]:


#Function to merge all the PDF input files:
#Remove if there is any file saved
fp = open("MergedFile.txt","a+",encoding='utf8')  
fp.close()
if os.path.exists("MergedFile.txt"):
    os.remove("MergedFile.txt")

fp = open("MergedFile.txt","a+",encoding='utf8')    
pdf_files = sorted(glob.glob('*.pdf'))
for f in pdf_files:
    raw = parser.from_file(f)
    fp.write(raw['content'])
    
fp.close()


# In[ ]:


#Create tokens from the data dscription:
input_file = 'MergedFile.txt'
fp = codecs.open(input_file, 'r', 'utf-8')
tokens = word_tokenize(fp.read())
fp.close()


# In[ ]:


word_dict = {}
bigram_dict = {}
trigram_dict = {}
ngram_dict = {}
tokenized_doc = []

clean = clean_tokens(tokens)
lem = lemmatize(clean)
tokenized_doc.append(lem)

# count word and ngram frequency
word_freq = count_ngrams(lem, 1)
bigram_freq = count_ngrams(lem, 2)
trigram_freq = count_ngrams(lem, 3)
ngram_freq = word_freq + bigram_freq + trigram_freq

unsorted_dict = ngram_to_dict(ngram_freq)


# In[ ]:


# final Dictionary of sorted words:
sorted_dict = sorted(unsorted_dict.items(),key=lambda x: x[1], reverse=True)  # By Value Backwards 
sorted_dict = sorted_dict[0:100]


# In[ ]:


#Creating CSV file:

if os.path.exists("ds1.csv"):
    os.remove("ds1.csv")
    
csvData= [['Word', 'Score']]

for word, frequency in sorted_dict:
    csvData.append([word,frequency])
    
with open('ds1.csv', 'w', newline='',encoding='utf8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)

csvFile.close()


# ## TextRank

# In[ ]:


#Analyse the data to extract keywords 
fp = codecs.open(input_file, 'r', 'utf-8')
tr4w = TextRank4Keyword()
tr4w.analyze(text=fp.read(),lower=True, window=3, pagerank_config={'alpha':0.85})

df=pd.DataFrame()
for item in tr4w.get_keywords(100, word_min_len=2):
    df=df.append({'Word':item.word,'Score':item.weight},ignore_index=True)
    
#Extract the top 100 keywords from the analysed data based on weights:

df=df.nlargest(100,columns=['Score'])

if os.path.exists("ds3.csv"):
    os.remove("ds3.csv")
    
columnsTitles = ['Word', 'Score']
df = df.reindex(columns=columnsTitles)
  
#Create the CSV:
df.to_csv('ds3.csv',index=False)


# ## TF-IDF

# In[ ]:


#Function for TF-IDF:

def dummy_fun(doc):
    return doc

tfidf = TfidfVectorizer(analyzer='word', stop_words='english', ngram_range=(1,3),tokenizer=dummy_fun,
    preprocessor=dummy_fun,token_pattern=None, use_idf=True)
response = tfidf.fit_transform(tokenized_doc)
weights = np.asarray(response.mean(axis=0)).ravel().tolist()
weights_df = pd.DataFrame({'Word': tfidf.get_feature_names(), 'Score': weights})
weights_df.sort_values(by='Score', ascending=False).head(100)

if os.path.exists("ds2.csv"):
    os.remove("ds2.csv")
  
#Create CSV file:
export_csv = weights_df.sort_values(by='Score', ascending=False).head(100).to_csv("ds2.csv", index = None, header=True) 

