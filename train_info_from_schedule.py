"""
Instructions for running the below code: Go to the following website: http://web.mta.info/developers/developer-data-terms.html#data
Accept the terms and conditions, and you will get to a new page with data feeds. Scroll to the Static Data Feeds, and under GTFS, click on and download the link titled 'New York City Transit Subway'. This zip file will have three useful files:
1) stops.txt will list the stop_id for every station on the line. Use this to come up with the appropriate stop_id.
2) stop_times.txt lists the time each scheduled trip is set to stop at each stop in the system. Use the path to this file as stops_path in the below code.
3) trips.txt lists the route_id that corresponds to each trip. Use the path to this file as trips_path in the below code.
"""


import numpy as np
import pandas as pd

#get all scheduled stops at a station with given stop_id, split by direction
def get_station_schedule(stops_path,trips_path,stop_id):
    master_schedule=pd.read_csv(stops_path,delimiter=',')        #read the txt file with all stops at all stations
    trips_df=pd.read_csv(trips_path,delimiter=',')               #read the txt file with that matches trip_id to route_id
    #match each stop at each station with a route_id using conditional join via trip_id
    master_schedule=master_schedule.join(trips_df.set_index('trip_id'),on='trip_id')    
    single_station_sched_N=master_schedule[master_schedule['stop_id']==stop_id+'N'] #get northbound schedule
    single_station_sched_S=master_schedule[master_schedule['stop_id']==stop_id+'S'] #get southbound schedule
    return [single_station_sched_N, single_station_sched_S] #return both schedules for a specific stop

def sort_by_day(df):         #separate a schedule (df) by class of day (Sunday, Weekday, or Saturday trip)
    sunday_trips=[]          #empty lists
    weekday_trips=[]
    saturday_trips=[]
    for entry in df['trip_id']:       #go through each trip_id and append it to its respective list
        if ('Sunday' in entry):
            sunday_trips.append(entry)
        elif ('Weekday' in entry):
            weekday_trips.append(entry)
        elif ('Saturday' in entry):
            saturday_trips.append(entry)
    sunday_schedule=df[df['trip_id'].isin(sunday_trips)]   #keep only the entries with trip_id in each respective list
    weekday_schedule=df[df['trip_id'].isin(weekday_trips)]
    saturday_schedule=df[df['trip_id'].isin(saturday_trips)]
    trips={}                                #create empty dictionary
    trips['Sunday']=sunday_schedule         #add in Sunday trips
    trips['Weekday']=weekday_schedule       #add in Weekday trips
    trips['Saturday']=saturday_schedule     #add in Saturday trips
    return trips                            #get all trips by day

def get_all_schedules_by_day(stops_path,trips_path,stop_id):
    schedules=[sort_by_day(item) for item in get_station_schedule(stops_path,trips_path,stop_id)]
    return schedules

def get_day_schedules_by_direction(stops_path,trips_path,stop_id):         #call this function
    all_schedules=get_all_schedules_by_day(stops_path,trips_path,stop_id)
    northbound,southbound=all_schedules[0],all_schedules[1]
    sunday_north=northbound['Sunday']
    weekday_north=northbound['Weekday']
    saturday_north=northbound['Saturday']
    sunday_south=southbound['Sunday']
    weekday_south=southbound['Weekday']
    saturday_south=southbound['Saturday']
    return [sunday_north,sunday_south,weekday_north,weekday_south,saturday_north,saturday_south]

def get_arrivals_per_hour(source):     #use a single dataframe as input
    ind=source.index
    source['hour_of_day']=''
    for item in ind:
        if (source['arrival_time'][item][:2]>='00' and source['arrival_time'][item][:2]<='05'):
            source=source.drop([item])         #remove the service from hours 00-05, and 24
        elif (source['arrival_time'][item][:2]>='24'):
            source=source.drop([item])
        else:                                  #bucket each arrival time by hour
            source['hour_of_day'][item]=source['arrival_time'][item][:2]
    hours,frequencies=np.unique(source['hour_of_day'],return_counts=True)
    return hours,frequencies

def all_frequencies(stops_path,trips_path,stop_id):    #get all frequencies for all hours
    the_schedules=get_day_schedules_by_direction(stops_path,trips_path,stop_id)
    results=[get_arrivals_per_hour(df) for df in the_schedules]
    buckets={}
    buckets['Sunday']={"Northbound":results[0],"Southbound":results[1]}
    buckets['Weekday']={"Northbound":results[2],"Southbound":results[3]}
    buckets['Saturday']={"Northbound":results[4],"Southbound":results[5]}
    return buckets

#stop_id should be a str with only numbers, no letters to indicate direction
#day_type should be: 'Sunday', 'Weekday', or 'Saturday'
#direction should be: 'Northbound' or 'Southbound'
#hour should: 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, or 23
def single_frequency(stops_path,trips_path,stop_id,hour,day_type,direction):
    results=all_frequencies(stops_path,trips_path,stop_id)
    desired_array=np.array(results[day_type][direction][0])
    hour_index=np.where(desired_array==hour)
    frequency=results[day_type][direction][1][hour_index]
    return frequency[0]