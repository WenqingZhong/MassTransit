# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:51:18 2020

@author: Wenqing Zhong
"""
'''
get_final_station_data(url,numofweek,station)
input: url for the turnstile website, how many weeks' data do you need, which station you want to work with
output: a csv file that includes data for one station, AND a text file with all line names

get_one_line(stationname,linename)
input: station name,line name. Must call get_final_station_data() before calling this function
You can check stationname_line_names.txt to get a line name
output: a csv file that includes data for one line, and a text file with all SCP names

get_one_SCP(linename,SCPname)
input: line name,SCP name. Must callget_one_line() before calling this function
You can check linename_SCP_names.txt to get a SCP name 
output: a csv file that includes data for one SCP
'''


from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
from itertools import islice
import pandas as pd
import os
import csv



url = "http://web.mta.info/developers/turnstile.html"# the turnstile data website url

def is_valid(url):#check if the url is valid
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_urls(url, limit):
    #"limit" is the number of turnstile data urls that you want to open, each url stores data for one week
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
    # I tried to directly create csv files but for some reasons the format is wrong, so I use text files as intermediates 
    return


def get_all_csv(url,limit):# open 'limit' number of turnstile data urls and store data in csv files
    links=get_all_urls(url, limit)
    for i in range(len(links)):
        get_one_csv(links[i],i)        
    return len(links)


def get_station(station,numofcsv): #get turnstile data of a certain station
    
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
                    if station in line:
                        writer.writerow(line)
    return

def get_linenames(station):
    name= "LINENAME"
    position=-1
    allnames=[]
    linenames={}
    
    with open('%s.csv'%station, 'r') as csvfile:
        reader = csv.reader(csvfile) 
        head=next(reader)       
        for item in head:
            position=position+1
            if name in item:
                break
        
        for row in reader:
            allnames.append(row[position])       
        csvfile.seek(0)
        
        for i in range(len(allnames)):
            try:
                linenames[allnames[i]].append(i+2)
            except KeyError:
                linenames[allnames[i]] = [i+2]
    
    keys= list(linenames.keys())
    with open('%s _line_names.txt'%station, 'w') as file: 
        try:
            file.write(str(keys))  
        except:
            return False              
    return linenames

def get_SCPs(linename):
    name= "SCP"
    position=-1
    allnames=[]
    SCPnames={}
    
    with open('%s.csv'%linename, 'r') as csvfile:
        reader = csv.reader(csvfile) 
        head=next(reader)       
        for item in head:
            position=position+1
            if name in item:
                break
        
        for row in reader:
            allnames.append(row[position])       
        csvfile.seek(0)
        
        for i in range(len(allnames)):
            try:
                SCPnames[str(allnames[i])].append(i+1)
            except KeyError:
                SCPnames[str(allnames[i])] = [i+1]
    
    keys= list(SCPnames.keys())
    with open('%s _SCP_names.txt'%linename, 'w') as file:        
        file.write(str(keys))                
    return SCPnames

#method called by user
def get_final_station_data(numofweek,station):
    url = "http://web.mta.info/developers/turnstile.html"# the turnstile data website url
    get_final_station_data_helper(url, numofweek, station)
    return

#helper method
def get_final_station_data_helper(url,numofweek,station):
    #input: url for the turnstile website, how many weeks' data that you need, and which station you want to work with
    numofcsv=get_all_csv(url,numofweek)
    get_station(station,numofcsv)
    get_linenames(station)
    
    for i in range(numofcsv):
        os.remove("data%s.csv"%i)
        
    return

def get_one_line(stationname,linename):
    
     alllinenames=get_linenames(stationname)
     
     with open('%s.csv'%stationname,'r') as stationfile:
        reader = csv.reader(stationfile) 
        head=next(reader)
        with open('%s.csv'%linename, 'w',newline='') as csvfile:
             writer = csv.writer(csvfile,quoting=csv.QUOTE_NONE)
             writer.writerow(head)
             n=alllinenames.get(linename)
             count=0
             for row in reader:
                    count=count+1
                    if(count in n):
                        try:
                            writer.writerow(row)
                        except:
                            return False               
        stationfile.seek(0) 
        
        get_SCPs(linename)            
        return
    
def get_one_SCP(linename,SCPname):
    
     allSCPs=get_SCPs(linename)
     print(allSCPs)
     
     with open('%s.csv'%linename,'r') as linefile:
        reader = csv.reader(linefile) 
        head=next(reader)
        with open('%s.csv'%SCPname, 'w',newline='') as csvfile:
             writer = csv.writer(csvfile,quoting=csv.QUOTE_NONE)
             writer.writerow(head)
             n= allSCPs.get(SCPname)
             count=0
             for row in reader:
                    count=count+1
                    if(count in n):
                        try:
                            writer.writerow(row)
                        except:
                            return False               
        linefile.seek(0)             
        return


#get_final_station_data(url,3,"96 ST")
#eg. get "96 ST" station's data for the last 3 weeks

#get_one_line("96 ST","BC")
#ef. get line"BC" in "96 ST"

#get_one_SCP("BC","01-00-00")
