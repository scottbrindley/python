# -*- coding: utf-8 -*-
"""
@title
Kayak Flight Trawler

@description
Trawl Kayak website and export results to csv for a given fight search
The following flight is used as an example:
    London -> Brisbane    
    Outbound 12/01/21
    Return 26/01/21

@author
Scott
"""
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
url = "https://www.kayak.co.uk/flights/LON-BNE/2021-01-12/2021-01-26/2adults?sort=bestflight_a"
driver.get(url)
#soup = BeautifulSoup(driver.page_source, 'lxml')
soup = BeautifulSoup(driver.page_source, "html.parser")
# print out contents of text returned by BeautifulSoup object
# print(soup.find(id='searchResultsList'))
# get last element of a list
# x = departure[1]

allFlights = []
# find the box containing all the flight results
container = soup.find(id='searchResultsList')
# the box will contain multiple entries, each one tagged by resultInner
wrapper = container.find_all("div", class_="resultInner")
# we need to loop through each one fo these results and strip out the flight details
for w in wrapper:
    flightResult = []  
    print("new result...")
    # strip the departure times for outbound and return
    departure = w.find_all("span", class_="depart-time base-time")  
    for d in departure:
        print(d.text)
        flightResult.append(d.text.strip())       
    # strip the arrival times for outbound and return
    arrival = w.find_all("span", class_="arrival-time base-time")  
    for a in arrival:
        print(a.text)
        flightResult.append(a.text.strip())   
    # strip the airline for for outbound and return flights  
    airlineSection = w.find_all("div", class_="section times")
    for s in airlineSection:
        airline = s.find("div", class_="bottom")
        print(airline.text.strip()) #strip away leading and trailing carriage returns
        flightResult.append(airline.text.strip())
    # strip the price of the flight    
    price = w.find_all("span", class_="price-text")[-1] # get the last price in the list (ignore the others)
    print(price.text)
    flightResult.append(price.text.strip()) 
    # add result to our flught list
    allFlights.append(flightResult)    

# close the selenium web browser        
#driver.quit()
    
# store results in a dataframe, to allow easy export to csv
df = pd.DataFrame(allFlights,columns=['outboundDepartureTime','returnDepartureTime', 'outboundArrivalTime', 
                                      'returnArrivalTime', 'outboundAirline', 'returnAirline', 'price'])
# add datestamp
df["ExtractDate"] = datetime.today().strftime("%d/%m/%Y")
df["ExtractTime"] = datetime.today().strftime("%H:%M:%S")

# sort by cheapest price
df.sort_values(by=["price"], inplace=True)

# write top 10 results to csv. No need to export header, or index
df.head(10).to_csv(r"C:\Users\scott\Documents\Python\data\flight_tracker.csv", mode="a", header=False, index=False)   

        
        
        

        
        
        
        
        
        
        
        
