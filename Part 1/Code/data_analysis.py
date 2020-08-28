
# coding: utf-8

# In[40]:


# import data analysis & viz libraries
import pandas as pd


# In[41]:


# import nlp libraries
import string
import collections
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
import glob
from nltk.tokenize import word_tokenize
import csv


# In[3]:


# set nlp variables
english_stops = stopwords.words('english')
lemmatizer = nltk.stem.WordNetLemmatizer()


# In[4]:


# create nlp functions

def clean_tokens(tokens):
    """ Lowercases, takes out punct and stopwords and short strings """
    return [token.lower() for token in tokens if (token not in string.punctuation) and 
                   (token.lower() not in english_stops) and len(token) > 2]

def lemmatize(tokens):
    """ Removes plurals """
    return [lemmatizer.lemmatize(token) for token in tokens]

def count_ngrams(tokens,n):
    n_grams = ngrams(tokens, n)
    ngram_freq = collections.Counter(n_grams)
    ngram_freq = ngram_freq.most_common()
    return ngram_freq

def ngram_to_dict(ngram_freq):
    l = []
    for t in ngram_freq:
        l.append((' '.join(t[0]),t[1]))
    return dict(l)


# In[5]:


word_dict = {}
bigram_dict = {}
trigram_dict = {}
ngram_dict = {}


# In[35]:


with open('FinalData.csv', "a") as csvFile:
    wr = csv.writer(csvFile, dialect='excel')


# In[36]:


FinalData=pd.DataFrame()
csv_2a2b2c = sorted(glob.glob('ds*.csv'))

job_desc = pd.read_csv('MergedBanks.csv')
csv_2a2b2c


# In[37]:


for index,row in job_desc.iterrows():
    for listID,csvpath in enumerate(csv_2a2b2c):
        csv_file=pd.read_csv(csvpath)
        #listtoadd = [job_desc['Institution'][index].encode('utf-8') , listID, job_desc['URL'][index].encode('utf-8'),job_desc['Job Category'][index].encode('utf-8'),job_desc['Job Title'][index].encode('utf-8')]
        #listtoadd = [str(job_desc['Institution'][index],'utf-8') , listID, str(job_desc['URL'][index],'utf-8'),str(job_desc['Job Category'][index],'utf-8'),str(job_desc['Job Title'][index],'utf-8')]
        listtoadd = [job_desc['Institution'][index] , listID, job_desc['URL'][index], job_desc['Job Category'][index],job_desc['Job Title'][index],job_desc['Location'][index]]
        #listtoadd = [unicode(job_desc['Institution'][index]) , listID, unicode(job_desc['URL'][index]), unicode(job_desc['Job Category'][index]),unicode(job_desc['Job Title'][index])]
        for i in range(0,100):
            keyword = csv_file['Word'][i]
            tokens_list = word_tokenize(job_desc['Description'][index])
            clean = clean_tokens(tokens_list)
            lem = lemmatize(clean)
            word_freq = ngram_to_dict(count_ngrams(lem, 1))
            bigram_freq = ngram_to_dict(count_ngrams(lem, 2))
            #trigram_freq = count_ngrams(lem, 3)
            x = word_freq[keyword] if (keyword in word_freq.keys()) else 0 + bigram_freq[keyword] if (keyword in bigram_freq.keys()) else 0
            #print(str(x) +" " + keyword + " in Job" + str(index))
            
            listtoadd.append(x)
            
        with open('FinalData.csv', "a") as csvFile:
            wr = csv.writer(csvFile, dialect='excel')
            try:
                wr.writerow(listtoadd)
            except:
                continue;
        #print(listtoadd)
csvFile.close()  

