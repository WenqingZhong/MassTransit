import numpy as np
import pandas as pd

def get_file(path):                     #creates a dataframe from a single station turnstile csv file
    df=pd.read_csv(path)
    return df


def get_scps(df):                            #creates one dataframe per unique turnstile
    #need to get each individual scp
    scp_array=np.unique(df['SCP'])
    df_list=[]
    for scp in scp_array:
        df_list.append(df[df['SCP']==scp])
    return df_list                            #returns list with one dataframe per unique turnstile


def get_entries_exits(df):  #gets the difference between adjacent entry and exit rows, then merges back into one dataframe
    scps=get_scps(df)
    for item in scps:
        entries=np.diff(item['ENTRIES'])
        entries=np.append(entries,0)           #make the entries array the same length as the dataframe column
        item['ENTRIES']=entries
        exits=np.diff(item[item.columns[11]])
        exits=np.append(exits,0)
        item[item.columns[11]]=exits
    entries_exits=pd.concat(scps,sort=False)     #concatenate into one dataframe to make adding entries/exits easier
    return entries_exits


def get_correct_turnstiles_given_hour(df,time_input):   #get the turnstile entries and exits corresponding to given hour
    entries_exits=get_entries_exits(df)
    hour=time_input[:2]
    compare_time=hour+':00:00'
    #get the unique times
    times_array=np.unique(np.array(entries_exits['TIME']))
    if (compare_time in times_array):
        correct_turnstiles=entries_exits[entries_exits['TIME']==compare_time]
        return correct_turnstiles                   #return a dataframe with only the corresponding entries/exits
    else:
        i=0
        for i in range(3):
            hour=int(hour)
            if (hour==0):
                hour=24
            hour-=1
            if (hour<10):
                hour=str(hour)
                hour='0'+hour
            hour=str(hour)
            compare_time=hour+':00:00'
            if (compare_time in times_array):
                correct_turnstiles=entries_exits[entries_exits['TIME']==compare_time]
                return correct_turnstiles           #return a dataframe with only the corresponding entries/exits
            i+=1

#master function to define all inputs - time_input should be 24 hr hh:mm           
def get_entry_exit_given_hour(path,time_input):       #sum the number of entries and exits for all scps over given hour
    df=get_file(path)                                 #create dataframe from csv file
    correct_turnstiles=get_correct_turnstiles_given_hour(df,time_input) #call nested functions
    num_entries=np.sum(np.array(correct_turnstiles['ENTRIES']))/4       #divide by 4, assuming uniform arrival rate
    num_exits=np.sum(np.array(correct_turnstiles[correct_turnstiles.columns[11]]))/4
    return num_entries,num_exits                    #this is the final return value, one entry and one exit value