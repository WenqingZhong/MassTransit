# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 17:46:35 2020

@author: Wenqing Zhong
"""
import csv
import datetime
'''
  first use CSV.DATA.py to get data for one station/one line/one SCP, than use 'sort_all_days' to get data for each week day
  input:station name
  output: 7 csv files, each file includes data for one week day
'''
def get_week_days(filename):
    
    name="DATE"
    position=-1
    date=[]
    week=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    days={}
    
    
    with open('%s.csv'%filename,'r') as stationfile:
        reader = csv.reader(stationfile) 
        head=next(reader)       
        for item in head:
            position=position+1
            if name in item:
                break
        #find which column stores date         
        for row in reader:
            date.append(datetime.datetime.strptime(row[position], '%m/%d/%Y').strftime("%a"))
            #change dates to week days
        stationfile.seek(0)
                                    
        for i in range(len(week)):
            for j in range(len(date)):
                if(date[j] == week[i]):
                    try:
                        days[week[i]].append(j+1)
                    except KeyError:
                        days[week[i]] = [j+1]                        
        return days   
     #'days' is a dictionary with week days as keys and csv line numbers as values

def sort_one_day(stationname,days,k):
    
    #create a csv file for one week day
    keys= list(days.keys())    
    with open('%s.csv'%stationname,'r') as stationfile:
        reader = csv.reader(stationfile) 
        head=next(reader)
        count=0
        with open('%s.csv'%keys[k], 'w',newline='') as csvfile:
            writer = csv.writer(csvfile,quoting=csv.QUOTE_NONE)
            writer.writerow(head)
            c=days.get(keys[k])
            for row in reader:
                count=count+1
                if(count in c):
                    try:
                        writer.writerow(row)
                    except:
                        return False               
        stationfile.seek(0)    
    return
 
def sort_all_days(stationname):
    #create csv files for all week days
    days=get_week_days(stationname)
    for i in range(len(list(days.keys()))):
        sort_one_day(stationname,days,i)    
    return
      
#sort_all_days("01-00-00")#this is a file that only includes data for 01-00-00 SCP, for how to get the file please go to CSV.DATA.py

