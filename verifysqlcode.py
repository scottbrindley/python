import pymysql.cursors

# rds settings
rds_host  = "ibi.cas7lp1zmi7e.eu-west-2.rds.amazonaws.com"
name = "admin"
password = "aw$ib10112"
db_name = "sys"
conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# setup variables
cursor = conn.cursor()
response = {}


def mark_submission(q, result):
    # if question 1 has been answered by the user
    if q == 1:
        answer=[]
        answer.append({'colour': 'green', 'num_of_people': 1})
        answer.append({'colour': 'purple', 'num_of_people': 1})
        answer.append({'colour': 'white', 'num_of_people': 1})
        answer.append({'colour': 'red', 'num_of_people': 2})        
    # check the user's answer matches the correct answer    
    if result == answer:
        "Pass"
    else:
        "Fail"    
    return result == answer

def lambda_handler(event, context):
    sql = event['queryStringParameters']['sqlString']
    q = event['queryStringParameters']['question']
    try:
        if cursor.execute(sql) == 0:
            raise ValueError("Your statement returned no rows")
        result = cursor.fetchall()    
        # mark the user's submission
        score = mark_submission(q, result)
        response['body'] = result
        response['score'] = score
        response['status'] = 200
        response['message'] = "Status OK"
    
    except Exception as e:
        print("Error: " + str(e))
        response['body'] = "-"
        response['score'] = "-"
        response['status'] = 404
        response['message'] = "Error: " + str(e)
        
    return response

sql = "select colour, count(*) as num_of_people from sys.test group by colour order by num_of_people, colour"     
q=1
inputEvent = {"queryStringParameters": {"sqlString": sql, "question": q}}
out = lambda_handler(inputEvent, 1)

