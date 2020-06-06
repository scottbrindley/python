"""
@title
Indeed keyword finder

@description
Parse the Indeed website for keywords as defined within the script
Count the number of times each keyword occurs in the search engine result set
Current job search is for "Data Engineer" in London

@author
Scott

@date
14/05/20
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
import re
import time
import pandas as pd
from datetime import datetime
import csv

driver = webdriver.Chrome()
driver.implicitly_wait(30)
url = "https://www.indeed.co.uk/jobs?q=Data+engineer+analyst&l=london"
driver.get(url)
# print page content to see if underlying code looks like Javascript. If so then we need to use selenium driver
# print(page.content)

soup = BeautifulSoup(driver.page_source, 'html.parser')
container = soup.find("td", id="resultsCol")
#print(container)
# import keywords
keywords = []
with open(r'C:\Users\scott\Documents\Python\data\tech_key_words.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        keywords.append(row[0])
        
JobName, Keyword = [],[]  

# loop through each job card returned by web page search
jobs = container.find_all("div", class_="jobsearch-SerpJobCard unifiedRow row result clickcard")
for j in jobs:
    a_ref = j.find("a", class_="jobtitle turnstileLink")  
    # search the string representation of the job hyperlink for the link id
    id1_ = re.search('id="\S*"', str(a_ref))
    if id1_ is not None:
        #print(id1_.group())
        id2_ = re.search('"(.*?)"', id1_.group()).group()
        id3_ = id2_.replace('"', "")
        print("Parsing element", id3_, "...")
    
    # click on job link, which brings up a new box on Indeed
    job_link = driver.find_element_by_id(id3_)
    try:
        job_link.click()
    except ElementNotInteractableException:
        print("Cannot click on the link")

    # time.sleep(5)
    # sometimes web load is not quick enough for Python, so the job click is missed.
    # if this happens, wait until the job click brings up the box
    try:
         element_present = EC.presence_of_element_located((By.ID, 'vjs-desc'))
         WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print("Timed out while waiting for page to load")
    
    # now the job box should have loaded, we can go and find the specific job details
    soup_lev2 = BeautifulSoup(driver.page_source, 'html.parser')  
    job_desc = soup_lev2.find("div", id="vjs-desc")    
    # each job box should have a conistent id name, but sometimes this isn't the case (not sure why, some html thing)
    if job_desc is not None:
        job_title = soup_lev2.find("div", id="vjs-jobtitle")
        print("    ", job_title.text)        
        # split the words into a list and remove all special characters 
        job_desc2 = re.sub(r'\W+', ' ', job_desc.text).split(' ')                
        # loop through each word in job description. If a word matches the keyword list, then add it
        for word in job_desc2:
            if word.lower() in keywords:
                JobName.append(job_title.text)
                Keyword.append(word)
    else:
        print("Cannot find job details on web page")
        
    
data_tuples = list(zip(JobName,Keyword))  
df = pd.DataFrame(data_tuples, columns=['Job Title','keyword'])
df = df.drop_duplicates()

# add datestamp
df["ExtractDate"] = datetime.today().strftime("%d/%m/%Y")
df["ExtractTime"] = datetime.today().strftime("%H:%M:%S")

# export to csv
df.to_csv(r"C:\Users\scott\Documents\Python\data\job_tracker.csv", mode="a", header=False, index=False)   
