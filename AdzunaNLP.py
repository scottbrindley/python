import pandas as pd
import re
import json
#pip install nltk
#nltk.download('words')
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import nltk
import pandas as pd
import collections


def lambda_handler(event, context):
    global df
    # Read the data payload and convert to dataframe
    #x = pd.read_json(e vent['Jobs'])
    #recs = event['Jobs']
    #df = pd.DataFrame(recs)
    print(event['Jobs'])
    df = pd.DataFrame(eval(event['Jobs']))
 
 
    #print(productName)
    print("Now returning to parent process")
    
    #4 Format and return the result
    return {
        'rows_loaded': 33
    }
 

######################################################################################################################################################################
# USED FOR TESTING IN SPYDER ONLY
# THIS IS A COPY OF THE LAMBDA TEST EVENT
'''
event = {
  "TransactionID": 1,
  "Jobs": {
    "adref": {
      "4": "eyJhbGciOiJIUzI1NiJ9.eyJpIjoiMjE1NjMyNTUxNiIsInMiOiI3bVVTUHNPLTZ4R2l5SFZXM3QyVFZBIn0.S3m-UnMhummT2vHWMKH5Haex1nBZOtmk5Vt5WX2_4Q0",
      "5": "eyJhbGciOiJIUzI1NiJ9.eyJzIjoiN21VU1BzTy02eEdpeUhWVzN0MlRWQSIsImkiOiIyMTM3ODUwMzYzIn0.WqDHO5-pP0cCU_HtBDUQumaaf0RrU5OEqNlBYSF2FXE"
    },
    "full_description": {
      "4": "Are you a Data Engineer with strong Azure or AWS experience? If the answer is yes, this large Financial Services organisation is looking for you...\nYou will help build out a new data platform, the foundations of which have been built and need fleshing out. The platform is in the Microsoft stack, including Azure, with a whole host of other technology utilised to help advance it as the company moves their data into a future state.\nYour responsibilities will include:\n\nManage data pipelines\nDrive Automation through effective metadata management\nLearning and using modern data preparation, integration and AI-enabled metadata management tools and techniques:\n\nTracking data consumption patterns\nPerforming intelligent sampling and caching\nMonitoring schema changes\n\nRecommending or sometimes even automating existing and future integration flows\nCollaborate across departments with data science teams and with business (data) analysts in refining their data requirements for various data and analytics initiatives and their data consumption requirements\nEducate and train\nParticipate in ensuring compliance and governance during data use\nBe a data and analytics evangelist\n\nYou should have a good mix of the following skills and experience (and I appreciate this list is lengthy):\n\nExperience with advanced analytics tools for object-oriented/object function scripting using languages such as R, Python, Java\nStrong ability to design, build and manage data pipelines for data structures encompassing data transformation, data models, schemas, metadata and workload management\nExperience with popular database programming languages including SQL, PL/SQL, others for relational databases and certifications on upcoming NoSQL/Hadoop oriented databases like MongoDB, Cassandra, others for non-relational databases\nExperience in working with large, heterogeneous datasets in building and optimizing data pipelines, pipeline architectures and integrated datasets using traditional data integration technologies\nExperience in working with and optimizing existing ETL processes and data integration and data preparation flows and helping to move them in production\nExperience in working with both open-source and commercial message queuing technologies such as Kafka, JMS, Azure Service Bus and others, stream data integration and analytics technologies such as Data Bricks and others\nExperience working with popular data discovery, analytics and BI software tools like Tableau, Qlik, PowerBI\nExperience in working with data science teams in refining and optimizing data science and machine learning models and algorithms\nDemonstrated success in working with large, heterogeneous datasets to extract business value using popular data preparation tools such as Trifacta, Paxata, Unifi\nBasic experience in working with data governance/data quality and data security teams\nDemonstrated ability to work across multiple deployment environments including cloud, on-premises and hybrid, multiple operating systems\nAdept in agile methodologies and capable of applying DevOps and increasingly DataOps principles to data pipelines\n\nTo be considered for the role click the 'apply' button or for more information about this and other opportunities please contact James Perry on 07 3339 5611 or email: jperry@paxus.com.au and quote the above job reference number. \nPaxus values diversity and welcomes applications from Indigenous Australians, people from diverse cultural and linguistic backgrounds and people living with a disability. If you require an adjustment to the recruitment process please contact me on the above contact details.",
      "5": "The Role\n As a Data Engineer you will be implementing foundational, robust and production ready data platforms to enable business data-discovery, self-service, AI/ML functions across a range of client types and industries, allowing them to do more with their data. You will be working with databases, data lakes, data warehouses, data transformation (Python & SQL) and enabling AI/ML.\n \nThis role is for you if you have:\n\nA passion for data! \nFocused data experience working with SQL and/or NoSQL solutions.\nSolid exposure to Software Engineering practises.\nAbility to analyse business scenarios and associated data landscape to derive potential opportunities.\nStrong foundation in Python and SQL.\nKafka experience is highly desirable.\nWorking knowledge of APIs.\nPrinciple knowledge of the different relational database platforms and modern data storage techniques.\nKnowledge of the different aspects of data environments.\nUnderstanding of the data lifecycle management process.\nExperience with version management systems (such as Git).\nWorking knowledge of AWS or another cloud platform\nGreat communication skills, an ability to work closely with customers, developers and engineers and the confidence to present ideas in open forums.\nContinuous improvement mindset.\nA STEM qualification is highly desirable (although experience counts!) and/or industry certifications.\nBackground in professional services/consulting is highly desirable\n\n \nWhat qualities should all applicants have?\nWe are looking for ambitious, passionate Data Engineers that can hit the ground running in a fast-paced, complex environment. You will be able to build relationships with clients based on integrity and will have a no failed project ethos. You will bring a strong passion for data, a 'can do' attitude and have your client's best interests at the forefront of your mind when implementing data-driven solutions.\n \n \n \nAt Randstad, we are passionate about providing equal employment opportunities and embracing diversity to the benefit of all. We actively encourage applications from any background."
    }
  }
}
lambda_handler(event, 0)
'''
######################################################################################################################################################################