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
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException
import re
import pandas as pd
from datetime import datetime
import traceback

bannerClicked = False
driver = webdriver.Chrome()
driver.implicitly_wait(30)
url = "https://www.indeed.co.uk/jobs?q=Data+engineer+analyst&l=london"
driver.get(url)
# print page content to see if underlying code looks like Javascript. If so then we need to use selenium driver
# print(page.content)
# print entire contents of html that web driver has pulled back
# driver.page_source

soup = BeautifulSoup(driver.page_source, 'html.parser')
container = soup.find("td", id="resultsCol")
#print(container)

# import keywords from txt file
keywords = []
keyword_pairs = []
with open(r'C:\Users\scott\Documents\Python\data\tech_key_words.txt', 'r') as f:
    reader = f.readlines() 
    for row in reader:
       # strip carriage return from end of each line
        tech_word = row.rstrip().split(" ")
        if len(tech_word) == 2:            
            keyword_pairs.append((tech_word[0], tech_word[1]))
        else:
            keywords.append(tech_word[0])            

# these lists will store the keywords found in each job listing
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
        if bannerClicked == False:
            # there is a banner that hovers over the link on the Indeed page which makes link unclickable, so click on this banner first to get rid of it
            try:
                e = driver.find_element_by_xpath('//button[text()="Dismiss"]')
            except (NoSuchElementException):
                print("Dismiss cookie button not loaded by website. Ignore this and continue ")
                bannerClicked = True
                continue
            if e is not None:
                print("Try to click on Dismiss button")
                e.click()
                bannerClicked = True
            
        # now click on job click
        job_link = driver.find_element_by_id(id3_)       
        try:                      
            job_link.click()           
        # if link click fails, then skip to next job listing            
        except (ElementNotInteractableException, ElementClickInterceptedException):           
            print("Cannot click on the link. Dumping the exception stack for debugging...")
            traceback.print_exc()
            continue
    # job hyperlink cannot be opened, so skip to next job
    else:
        print("Cannot find job details on web page")
        continue

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
                
        # now do the same for technologies with more than one word. zip will create list of word 1 + word 2
        for x in zip(job_desc2, job_desc2[1:]):
            for y in keyword_pairs:
                # convert list to lowercase
                x_lowercase = [xx.lower() for xx in x]
                # conver to tuple to allow list comparison
                if y == tuple(x_lowercase):
                    #print(x)
                    JobName.append(job_title.text)
                    # convert tuple to string
                    Keyword.append(''.join(x))

    else:
        print("Cannot find job details on web page")
        
# close the selenium web browser        
driver.quit()
    
# Dataframe processing expensive, so do data manipulation in lists first
data_tuples = list(zip(JobName,Keyword))  
df = pd.DataFrame(data_tuples, columns=['Job Title','keyword'])
df = df.drop_duplicates()

# add datestamp
df["ExtractDate"] = datetime.today().strftime("%d/%m/%Y")
df["ExtractTime"] = datetime.today().strftime("%H:%M:%S")

# export to csv
df.to_csv(r"C:\Users\scott\Documents\Python\data\job_tracker.csv", mode="a", header=False, index=False)   

# summarise
dfBar = pd.read_csv(r"C:\Users\scott\Documents\Python\data\job_tracker.csv")
dfBar["Technology"].str.lower().value_counts()


