from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request as ur
import pandas as pd
import time
import math
import os

exception = []

#Web Scraping - American Express Bank
driver = webdriver.Chrome("C:/chromedriver.exe")
amex_joblistings  = []
url = 'https://jobs.americanexpress.com/jobs?page=1'
driver.get(url)
time.sleep(2)
body = driver.find_element_by_tag_name("body").get_attribute('innerHTML')
soup = BeautifulSoup(body, "html.parser")
pgno = soup.find(class_="mat-paginator-range-label").get_text()
last_page = math.ceil(int(pgno[10:])/10)+1

for i in range(1,last_page):
   url = 'https://jobs.americanexpress.com/jobs?page='+str(i)
   driver.get(url)
   time.sleep(2)
   body = driver.find_element_by_tag_name("body").get_attribute('innerHTML')
   soup = BeautifulSoup(body, "html.parser")
   links=soup.find_all(class_="job-title-link")
   for link in links:
       amex_joblistings.append("https://jobs.americanexpress.com"+link.get('href'))

driver.quit()
       
df_amexbank=pd.DataFrame()

for url in amex_joblistings:
   try:
       response = ur.urlopen(url)
       html_doc = response.read()
       soup = BeautifulSoup(html_doc, 'lxml')
       data = soup.find(class_="jibe-job-description job-description").get_text()
       job_title = soup.find(class_="job-title").get_text()
       location = soup.find(id = "label-job-location").get_text()
       location = location.rstrip()
       location = location.replace("Locations:", "")
       location = location.replace("Multiple Locations:", "")
       category = soup.find(class_ = "job-category ").get_text() + ", " + soup.find(class_ = "job-category last-child ").get_text()
       category = category.rstrip()
       category = category.replace("Categories:", "")
       df_amexbank=df_amexbank.append({'Institution':'American Express','URL':url,'Description':data,'Job Title':job_title,'Location':location, 'Job Category':category}, ignore_index=True)
   except:
       exception.append(url)
       continue;              

if os.path.exists("amexRaw.csv"):
    os.remove("amexRaw.csv")
  
export_csv = df_amexbank.to_csv("amexRaw.csv", index = None, header=True) 



#Web Scraping - US Bank
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request as ur
import pandas as pd
import time
import math
import os

exception = []

driver = webdriver.Chrome("C:/chromedriver.exe")
usbank_joblistings  = []
url = 'https://usbank.taleo.net/careersection/10000/jobsearch.ftl?lang=en'
driver.get(url)
time.sleep(1)
body = driver.find_element_by_tag_name("body").get_attribute('innerHTML')
soup = BeautifulSoup(body, "html.parser")
last_page = soup.find(id="currentPageInfo").get_text()
last_page = math.ceil(int(last_page.split("of ",1)[1]) / int(25))

ittr = "first"
for i in range(0,last_page):
   try:
       if ittr == "first":
           url = 'https://usbank.taleo.net/careersection/10000/jobsearch.ftl?lang=en'
           driver.get(url)
           ittr = "second"
       else:
           driver.find_element_by_id('next').click()
       time.sleep(1)
       body = driver.find_element_by_tag_name("body").get_attribute('innerHTML')
       soup = BeautifulSoup(body, "html.parser")
       for job in soup.find_all(class_="multiline-data-container"):
           temp = job.find('a')
           usbank_joblistings.append("https://usbank.taleo.net"+temp.get('href'))
   except:
       print("except")
       continue;

 
   
df_usbank=pd.DataFrame()

for url in usbank_joblistings:
   try:
       driver.get(url)
       time.sleep(2)
       body = driver.find_element_by_tag_name("body").get_attribute('innerHTML')
       soup = BeautifulSoup(body, "html.parser")
       data = soup.find(id="requisitionDescriptionInterface.ID1476.row1").get_text() + soup.find(id="requisitionDescriptionInterface.ID1536.row1").get_text()
       job_title = soup.find(id="requisitionDescriptionInterface.reqTitleLinkAction.row1").get_text()
       location = soup.find(id = "requisitionDescriptionInterface.ID1677.row1").get_text()
       category = soup.find(id = "requisitionDescriptionInterface.ID1633.row1").get_text()
       df_usbank=df_usbank.append({'Institution':'US Bank','URL':url,'Description':data,'Job Title':job_title,'Location':location, 'Job Category':category}, ignore_index=True)
   except:
       exception.append(url)
       continue; 

if os.path.exists("USBankRaw.csv"):
    os.remove("USBankRaw.csv") 

driver.quit()    
export_csv = df_usbank.to_csv("USBankRaw.csv", index = None, header=True) 
       