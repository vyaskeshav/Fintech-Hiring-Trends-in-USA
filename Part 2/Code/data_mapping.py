#!/usr/bin/env python
# coding: utf-8

# In[4]:


# import libraries
import pandas as pd
import string
import collections
import glob
import csv
import os


# In[6]:


FinalData=pd.DataFrame()
buckets = pd.read_csv('fintech_keywords.csv')
merged_banks = pd.read_csv('merged_data_all_banks.csv')

keywords_dict = {}

for index,row in buckets.iterrows():
    if buckets['Cluster'][index] in keywords_dict:
        keywords_dict[buckets['Cluster'][index]].append(buckets['Keywords'][index]) 
    else:
        keywords_dict[buckets['Cluster'][index]] = [buckets['Keywords'][index]]

if os.path.exists("FinalData.csv"):
    os.remove("FinalData.csv")
    
with open('FinalData.csv', 'w', newline='') as csvFile:
    wr = csv.writer(csvFile, dialect='excel')
    wr.writerow(['Job ID', 'Job Title', 'Bank Name','Fintech','Matched Cluster', 'Matched Words','Number of Words Matched','URL'])


# In[7]:


count = 0
for index,row in merged_banks.iterrows():
    count = count + 1
    addtocsv = [count]
    fintech_flag = 'No'
    matched_clusters = []
    matched_words = []
    job_desc = merged_banks['Job Desc'][index]
    addtocsv.append(merged_banks['Job Title'][index])
    addtocsv.append(merged_banks['Bank Name'][index])
    for cluster, keywordlist in keywords_dict.items():
        for keyword in keywordlist:
            if str(keyword).lower() in str(job_desc).lower():
                fintech_flag = 'Yes'
                if cluster not in matched_clusters:
                    matched_clusters.append(cluster)
                matched_words.append(str(keyword))
                
    addtocsv.append(fintech_flag)
    addtocsv.append(",".join(matched_clusters))
    addtocsv.append(",".join(matched_words))
    addtocsv.append(len(matched_words))
    addtocsv.append(merged_banks['URL'][index])
    with open('FinalData.csv', "a", newline='') as csvFile:
            wr = csv.writer(csvFile, dialect='excel')
            try:
                wr.writerow(addtocsv)
            except:
                continue;
csvFile.close()        


# In[ ]:




