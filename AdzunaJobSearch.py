"""
Use Adzuna API to retrieve job ads

See for more detail interacting with Adzuna API
https://developer.adzuna.com/activedocs#!/adzuna/version

Packages have been linked up to a public ARN, see below
https://github.com/keithrozario/Klayers
"""

import requests
import boto3
from pandas import json_normalize 
from datetime import datetime
from io import StringIO
from bs4 import BeautifulSoup



def lambda_handler(event, context):
    print("INFO: Adzuna Job Search commencing")
    get_jobs()

#Adzuna API truncates job description, so we need to use BeautifulSoup to scrape the full description
 #from the webpage (luckily the webpage is provided as a field in the API return)
def get_full_description(url):   
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")    
    #url will either contain ***/land/*** or ***/detail/*** 
    #land we can't scrape as it's a splash page before loading up the main page. Therefore we have to set description to null
    if '/land' in url:
        description=''
    else:
        description = soup.find(class_='adp-body mx-4 mb-4 text-sm md:mx-0 md:text-base md:mb-0').text
    return description.strip()


def get_jobs():
    response = requests.get(
    'https://api.adzuna.com/v1/api/jobs/au/search/1',
    params={'app_id': '635dffa7', 
            'app_key': 'c4cad92c067bd30499bf18b5bf7ce92f',            
            'results_per_page': '100', #pretty sure 50 is the max anyway, but set to 100 for good measure
            'what': 'data engineer',
            'where':'brisbane',
            'what_exclude': 'architect civil electircal ambassador'}
    )
    
    if response:
        print("INFO: API call success")
    else:
        print('INFO: API call failed')
    
    #convert ouput from API to a dataframe
    json_response = response.json()
    df = json_normalize(json_response, 'results')
    n = df["adref"].nunique()
    print(f"Number of unique values: {n}")
    
    #reorder fields
    df1 = df[[ 'title',
              'adref',         
              'created',         
              'description',
              'company.display_name',
              'location.display_name',
              'contract_type',
              'salary_max',
              'salary_min',
               'redirect_url'
              ]]
    
    #rename fields
    df1.rename(columns = {'company.display_name':'company', 'location.display_name':'location',}, inplace = True)
    
    #remove hyperlinks
    df1['title'].replace('<[\/]*strong>', '', regex=True, inplace=True)
    df1['description'].replace('<[\/]*strong>', '', regex=True, inplace=True)
    
    #extract date from timestamp field
    df1['create_dt'] = df1['created'].str[:10]
    df1.drop('created', axis=1, inplace=True)
    
    #scrape full job description directly from webpage
    df1["full_description"] = df1["redirect_url"].apply(get_full_description)
    
    #write to aws s3 bucket as a csv file
    #aws credentials need to be configured if running locally. Use "aws configure"
    s3 = boto3.resource('s3')
    csv_buffer = StringIO()
    df1.to_csv(csv_buffer)
    filename = 'AdzunaJobSearch_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.csv'
    bucket = 'adzuna'
    s3.Object(bucket, filename).put(Body=csv_buffer.getvalue())    
  
    
    print("INFO: Adzuna Job Search complete")
    
if __name__ == "__main__":
    lambda_handler(0,0)
    
    
    
    
    
    
    