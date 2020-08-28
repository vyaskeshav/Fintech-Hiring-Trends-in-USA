import pandas as pd
import csv    

finalDataCSV = pd.read_csv("FinalData.csv",encoding = "ISO-8859-1")


amex_fintech=0
us_fintech = 0
amex_total = 0
us_total = 0

for index,row in finalDataCSV.iterrows():
    if ('american express' in str(finalDataCSV['Institution'][index]).lower()):
        amex_fintech += finalDataCSV.loc[index,'1':'100'].sum()  
        amex_total += 1
    elif ('us bank' in str(finalDataCSV['Institution'][index]).lower()):
        us_fintech += finalDataCSV.loc[index,'1':'100'].sum()
        us_total += 1
        
        
avg_amex=amex_fintech/amex_total
avg_us=us_fintech/us_total

mydict = {}

mydict['American Express'] = avg_amex
mydict['US Bank'] = avg_us
sorted_dict = sorted(mydict.items(),key=lambda x: x[1], reverse=True)

csvData= [['Institution', 'Fintech Score']]

for institution, fintechscore in sorted_dict:
   csvData.append([institution,fintechscore])

with open('bankcomparisons.csv', 'w', newline='',encoding='utf8') as csvFile:
   writer = csv.writer(csvFile)
   writer.writerows(csvData)

csvFile.close()
    
