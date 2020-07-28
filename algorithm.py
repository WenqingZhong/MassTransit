"""
@author: Mehr Kaur, Raayan Mohtashemi
"""


from datetime import datetime
import numpy as np
import os
import sys
sys.path.insert(0, os.path.abspath(r'/Users/mehrkaur/Documents/projects/subway/MassTransit/'))
from get_station_csv import get_final_station_data
from sort_by_week_day import sort_all_days
from h4_chunks_in_py import entries_exits_in_4h_chunks
from train_info_from_schedule import single_frequency
from entries_exits import get_entry_exit_given_hour


#stop_id is 120 for 96th Street, 117 for 116th Street - both on the 1 line
def get_crowds(date,time,stop_id):
    requestedDay = date.weekday()
    weekDays = ("Mon","Tue","Wed","Thu","Fri","Sat","Sun")
    stops_path = r'/Users/mehrkaur/Documents/projects/subway/MassTransit/google_transit/stop_times.txt'
    trips_path = r'/Users/mehrkaur/Documents/projects/subway/MassTransit/google_transit/trips.txt'
    #stop_id = "117" #HARDCODED for 96th, our pilot
    
    #train schedule is recorded only between 6 am ('06') and 11 pm ('23') to make room for cleaning
    #also, time needs to be formatted to have 2 digits
    hourINT = time.hour
    if (hourINT < 6):
        hour = "06"
    elif (hourINT > 23):
        hour = "23"
    elif (hourINT < 10):
        hour = "0" + str(hourINT)
    else:
        hour = str(hourINT)

    #train schedule data is split into weekday, Saturday, Sunday
    if(requestedDay <= 4):
        day_type = "Weekday"
    elif(requestedDay == 5):
        day_type = "Saturday"
    else:
        day_type = "Sunday"

    northTrains = single_frequency(stops_path,trips_path,stop_id,hour,day_type,"Northbound")
    southTrains = single_frequency(stops_path,trips_path,stop_id,hour,day_type,"Southbound")
    trainsPerPlatform = np.array([northTrains, southTrains])
    mins = str(time.minute)
    if(len(mins) == 1):
        mins = "0" + mins

    time_input = hour + ":" + mins

    #our turnstile data is available from 06:00 - 20:59
    #we already account for 06:00 bound above, we need to now account for 20:59 bound here.
    if(hourINT > 20):
        time_input = "20:59"
        
    totalEntries = 0
    totalExits = 0 #throw-away value
    predictedCrowds = np.array([0,0]) #HARDCODED 2 platforms, 2 crowd predictions.

    if(requestedDay <= 4): #is a work day
        sumCrowds = np.array([0,0]) #HARDCODED for 96
        for i in range (0,5):
            filename = weekDays[i] + ".csv"
            path = r"/Users/mehrkaur/Documents/projects/subway/MassTransit/" + filename
            totalEntries, totalExits = get_entry_exit_given_hour(path,time_input) 
            entriesPerPlatform = totalEntries / 2 #HARDCODED, num. platforms at 96th and 116th

            tempCrowds = entriesPerPlatform / trainsPerPlatform
            sumCrowds = sumCrowds + tempCrowds

        predictedCrowds = sumCrowds / 5 #avg over 5 work days

    else: #is weekend
        filename = weekDays[requestedDay] + ".csv"
        path = r"/Users/mehrkaur/Documents/projects/subway/MassTransit/" + filename
        totalEntries, totalExits = get_entry_exit_given_hour(path,time_input)
        entriesPerPlatform = totalEntries / 2 #HARDCODED, num. platforms at 96th and 116th

        predictedCrowds = entriesPerPlatform / trainsPerPlatform
    
    return totalEntries, predictedCrowds

def grade_crowds(predictedCrowds):
    platformDensities = np.array([0,0])
    platform_length = 510
    platform_width = 12.5
    platform_size = (platform_length * platform_width) / 2 #assume half the platform is unusable space (walls, stairs, etc)
    if (predictedCrowds.size != 0):
        #length = len(predictedCrowds)
        platformDensities = np.array([0,0]) #HARDCODED, 2 platforms = 2 elements
        for i in range(0,predictedCrowds.size):
            if predictedCrowds[i]: 
                density = platform_size / predictedCrowds[i] #square feet per person
            else: density = 0
            platformDensities[i] = density
    else: platformDensities = predictedCrowds

    platformGrades = np.array(["0","0"]) #0 represents no data
    green = 64 #at least 8 feet per person in all directions
    yellow = 36 #at least 6 feet (CDC recommendation) 
    orange = 16 #at least 4 feet 
    if (platformDensities.size != 0):
        #length = len(platformDensities)
        platformGrades = np.array([0,0])
        for i in range(0,platformDensities.size):
            if platformDensities[i]:
                if(platformDensities[i] >= green):
                    platformGrades[i] = 4
                elif(platformDensities[i] >= yellow):
                    platformGrades[i] = 3
                elif(platformDensities[i] >= orange):
                    platformGrades[i] = 2
                else:
                    platformGrades[i] = 1

            else:
                platformGrades[i] = 0
    return platformGrades
                