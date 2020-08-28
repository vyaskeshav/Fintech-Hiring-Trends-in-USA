import string
import collections
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
import csv
# set nlp variables
english_stops = stopwords.words('english')
lemmatizer = nltk.stem.WordNetLemmatizer()

#Functions to clean data:
#Function removes stop words, punctuation
def clean_tokens(tokens):
    """ Lowercases, takes out punct and stopwords and short strings """
    return [token.lower() for token in tokens if (token not in string.punctuation) and 
                   (token.lower() not in english_stops) and len(token) > 2]

#Function to remove plurals
def lemmatize(tokens):
    """ Removes plurals """
    return [lemmatizer.lemmatize(token) for token in tokens]

#Function to create ngram, bigram, trigram
def count_ngrams(tokens,n):
    n_grams = ngrams(tokens, n)
    ngram_freq = collections.Counter(n_grams)
    ngram_freq = ngram_freq.most_common()
    return ngram_freq

#Function to create dictionary of words and frequencies:
def ngram_to_dict(ngram_freq):
    l = []
    for t in ngram_freq:
        l.append((' '.join(t[0]),t[1]))
    return dict(l)


jobCategories = []
finalDataCSV = pd.read_csv("FinalData.csv", encoding="ISO-8859-1")
jobCategories = finalDataCSV['Job Category'][:]
tokens = nltk.word_tokenize(str(jobCategories))
clean = clean_tokens(tokens)
lem = lemmatize(clean)

bigram_dict = {}
trigram_dict = {}
quadgram_dict = {}


bigram_freq = count_ngrams(lem, 2)
trigram_freq = count_ngrams(lem, 3)
quad_freq = count_ngrams(lem, 4)
ngram_freq =  bigram_freq + trigram_freq + quad_freq

unsorted_dict = ngram_to_dict(ngram_freq)
sorted_dict = sorted(unsorted_dict.items(),key=lambda x: x[1], reverse=True) 

tfidf = TfidfVectorizer(analyzer='word', stop_words='english', ngram_range=(2,3))
response = tfidf.fit_transform(jobCategories)
weights = np.asarray(response.mean(axis=0)).ravel().tolist()
weights_df = pd.DataFrame({'Word': tfidf.get_feature_names(), 'Score': weights})
weights_df = weights_df.sort_values(by='Score', ascending=False)
print(weights_df)

x = 0
mydict = {}
for keyword in weights_df.sort_values(by='Score', ascending=False).ix[:,0]:
    for index,row in finalDataCSV.iterrows():
        x += finalDataCSV.loc[index,'1':'100'].sum() if (keyword in str(finalDataCSV['Job Category'][index]).lower()) else 0
        
    mydict[keyword] = x
    
sorted_dict = sorted(mydict.items(),key=lambda x: x[1], reverse=True)

if os.path.exists("jobcatgraph.csv"):
    os.remove("jobcatgraph.csv")
    
csvData= [['Job Category', 'Fintech Score']]

for jobtitle, fintechscore in sorted_dict:
    csvData.append([jobtitle,fintechscore])
    
with open('jobcatgraph.csv', 'w', newline='',encoding='utf8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)

csvFile.close()