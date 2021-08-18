import boto3
import codecs
import csv
import pandas as pd
import json

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Adzuna_Jobs")
lambda_ = boto3.client('lambda')

def upload_jobs(event):
    print('INFO: Beginning upload of Job keys to Dynamo DB')
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    resp = s3.get_object(Bucket=bucket, Key=filename)
    for row in csv.DictReader(codecs.getreader("utf-8")(resp["Body"])):
        #print(row['title'] + ' - ' + row['adref'])
        table.put_item(
            Item = {
                "title": row["title"],
                "adref": row["adref"]
            }
        )

#def download_jobs():
#    print('INFO: Beginning download of Job keys')
#    resp = table.scan(Limit=2)
#    jobs = resp["Items"]
#    return pd.DataFrame(jobs)

def keep_todays_jobs(event):
    global df_todays_jobs
    global df_jobs, df_prev
    print('INFO: Keeping job ads that have yet to be ingested')
    
    # get jobs that have been loaded today
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    resp = s3.get_object(Bucket=bucket, Key=filename)
    df_jobs = pd.read_csv(resp.get("Body"))
    
    # get list of job keys that we have processed in the past
    resp = table.scan(Limit=500)
    jobs = resp["Items"]
    df_prev = pd.DataFrame(jobs)
    
    # discard the jobs that we have already processed
    df_common = df_jobs.merge(df_prev, on=["adref"])
    df_todays_jobs = df_jobs[~df_jobs["adref"].isin(df_common["adref"])]
    #print(df_todays_jobs["adref"])
    
    
def lambda_handler(event, context):
    #upload_jobs(event)
    keep_todays_jobs(event)
    send_to_nlp()
 
def send_to_nlp():   
    global input_params
    # drop null descriptions
    df_tmp = df_todays_jobs.dropna(subset=['full_description'])
    # only keep the columns required by NLP processing
    df_out = df_tmp[["adref", "full_description"]]
    # convert payload to json
    js = df_out.to_json()
    
    # create parameter file
    input_params = {
        'TransactionID': 1,
        'Jobs': js
    }
    
    response = lambda_.invoke(
        FunctionName = 'arn:aws:lambda:eu-west-2:712339158037:function:AdzunaNLP',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(input_params)
    )
    
    # process payload information from the response
    response_payload =  json.load(response['Payload'])
    print("INFO: Status = " + str(response["StatusCode"]))
    print(response_payload)
    print("INFO: Rows loaded = " + str(response_payload["rows_loaded"]))


###################################################################################
# USED FOR TESTING IN SPYDER ONLY
# THIS IS A COPY OF THE LAMBDA TEST EVENT
'''
event = {
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "eu-west-2",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "adzuna",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::example-bucket"
        },
        "object": {
          "key": "AdzunaJobSearch_20210527081258.csv",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}
lambda_handler(event, 0)
'''
###################################################################################