# -*- coding: utf-8 -*-

"""

Created on Jul 06 10:51:18 2020



@author: Wenqing Zhong, Julian Briggs, Mehr Kaur

"""

'''

get_final_station_data(url,numofweek,station)

input: url for the turnstile website, how many weeks' data do you need, which station you want to work with

output: a csv file that includes data for one station

'''





from bs4 import BeautifulSoup

import requests

from urllib.parse import urlparse, urljoin

from itertools import islice

import pandas as pd

import os

import csv

import numpy as np





url = "http://web.mta.info/developers/turnstile.html"# the turnstile data website url



def is_valid(url):#check if the url is valid

    parsed = urlparse(url)

    return bool(parsed.netloc) and bool(parsed.scheme)



def get_all_urls(url, limit):

    #"limit" is the number of urls that you want to open, each url stores data for one week

    if(is_valid(url)==False):

        print("ERROR WITH URL INPUT")

       

    base=url

    soup = BeautifulSoup(requests.get(url).content, "html.parser")    

    urls=[]

    

    for link in islice(soup.find_all('a'),limit+37): 

        #find all internal urls in the trunstile data website

        #usually the first 37 internal urls are uesless, they don't store turnstile data so we skip them       

        href = link.attrs.get("href")   

        if(str(href).startswith("data")== True):#all internal urls that store turnstile data are in html format and they start with the word 'data'

            full=urljoin(base, href)

            urls.append(full)# store turnstile data urls        

    return urls





def get_one_csv(url,i):

    r = requests.get(url)#go to one turnstile data url(each url stores data for one week)

    

    with open('data%s.txt'%i, 'w') as file:#write the data in a text file

        try:

            file.write(r.text) #update the text file if it already exists

        except:

            return False

        

    df = pd.read_csv("data%s.txt"%i,delimiter=',')#convert the text file into a csv file

    df.to_csv('data%s.csv'%i)

    os.remove("data%s.txt"%i)

    # I tried to directly create csv files but for some reasons the format is wrong, so I used text files as intermediates 

    return





def get_all_csv(url,limit):# open 'limit' number of turnstile data urls and store data in csv files

    links=get_all_urls(url, limit)

    for i in range(len(links)):

        get_one_csv(links[i],i)        

    return len(links)





def get_station(station,linename,numofcsv): #get turnstile data of a certain station

    

    with open('%s.csv'%station, 'w',newline='') as csvfile: 

        with open('data0.csv') as head:

            headreader = csv.reader(head)  

            head= next(headreader)

            writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_NONE) 

            writer.writerow(head)

            

        for i in range(numofcsv):

            with open('data%s.csv'%i) as f_obj:

                reader = csv.reader(f_obj)  
                
                for line in reader: 
                    temp = line.spilt(",")
                    print(temp)

                    if ((station in line) and (linename in temp[4])):

                        writer.writerow(line)

    return




#method called by user
def get_final_station_data(numofweek,station, line):
    url = "http://web.mta.info/developers/turnstile.html"# the turnstile data website url
    get_final_station_data_helper(url, numofweek, station, line)
    return

#helper method
def get_final_station_data_helper(url,numofweek,station,linename):

    #input: url for the turnstile website, how many weeks' data that you need, and which station you want to work with

    numofcsv=get_all_csv(url,numofweek)

    get_station(station,linename,numofcsv)

    

    for i in range(numofcsv):

        os.remove("data%s.csv"%i)

    return

