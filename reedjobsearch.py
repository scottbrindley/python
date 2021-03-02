from ReedJobDescription import scrapeJobDescription

def lambda_handler(event, context):
    
    print("INFO: Starting Red job search")
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    @title
    Reed Job Search
    
    @prerequisites
    reed API project interface should be installed by running "pip install reed"
    boto3 interface should be installed by running "pip install boto3"
    you will need a Reed publisher id, which you can get from https://www.reed.co.uk/developers/Jobseeker
    
    @author
    Scott Brindley
    
    @date
    05/11/20
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    # this module will be used to pull back job searches from Reed API
    from reed import ReedClient
    client = ReedClient(api_key="0b580c80-65a7-4128-a175-759a790665ef")
    # needed for interaction with aws s3 bucket
    import boto3
    from datetime import datetime
    import json
    
    
    """
    keywords - This is the parameter for your search query. By default terms are ANDed.
    resultsToTake - maximum number of results to return (the default is 100)
    employerId - id of employer posting job
    employerProfileId - profile id of employer posting job
    locationName - the location of the job
    distanceFromLocation - distance from location name in miles (default is 10)
    permanent - true/false
    contract - true/false
    temp - true/false
    partTime - true/false
    fullTime - true/false
    minimumSalary - lowest possible salary e.g. 20000
    maximumSalary - highest possible salary e.g. 30000
    postedByRecruitmentAgency - true/false
    postedByDirectEmployer - true/false
    graduate - true/false
    """
    params = {
        'keywords' : "data engineer",
        'locationName' : "London",
        'minimumSalary': 30000,
        'resultsToTake': 5
    }
    
    
    # retrieve jobs using desired parameters from Reed API
    response = client.search(**params)
    # full job description is not provided by Reed API
    # therefore we must go and scrape it directly from the website
    for joburl in response:    
        joburl["FullJobDescription"] =  scrapeJobDescription(joburl["jobUrl"])
        
        
    
    # write to s3
    cli = boto3.client('s3')
    serializedMyData = json.dumps(response)
    fileName = 'ReedJobSearch_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.json'
    cli.put_object(Body=serializedMyData , Bucket='ibi-dev-bucket', Key=fileName)

    
    print("INFO: Completed Red job search")
