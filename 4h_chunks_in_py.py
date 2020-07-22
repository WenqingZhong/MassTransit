"""
Created on Mon Jul 13 14:11:06 2020

@author: Wenqing Zhong

entries_exits_in_4h_chunks(filename,continuous)

input:datafile, does the datafile have continuous dates
      eg.files from sort_by_week_day are not continuous, so call entries_exits_in_4h_chunks(filename,False)

output:print entries and exits in 4h chunks

"""



import csv
from datetime import datetime,timedelta 
import os

def find_column(name,head):    
    position=-1
    for item in head:
        position=position+1
        if name in item:
            break
    return position

def sort_by_date(filename):
    with open('%s.csv'%filename, 'r') as csvfile:
         reader = csv.reader(csvfile)
         head=next(reader) 
         dateidx=find_column("DATE",head)
         timeidx=find_column("TIME",head)
         times=[]
         date={}
         
         count=1
         for row in reader:
            try:
                date[str(row[dateidx])].append(count)
               
            except KeyError:
                date[str(row[dateidx])] = [count]
            times.append(row[timeidx])
            count=count+1
            
         csvfile.seek(0)  
         
                 
         dates=list(date.keys())        
         dates.sort(key = lambda date: datetime.strptime(date, '%m/%d/%Y'))
         times = list(dict.fromkeys(times))
         
         with open ('%s dates_sorted.csv'%filename, 'w',newline='') as sortedfile:
             writer = csv.writer(sortedfile,quoting=csv.QUOTE_NONE)
             writer.writerow(head)
             for i in range(len(dates)):
                 c=date.get(dates[i]) 
                 rownum=-1               
                 for row in reader:
                     rownum= rownum+1
                     if(rownum in c):
                         try:
                             writer.writerow(row)
                         except:
                             return False                              
                 csvfile.seek(0)            
    return times


def cal_ent_exi(filename,starttime,endtime):
     
     sort_by_date(filename)
     totalent={}
     totalexit={}
     timechunks={}
     
     with open('%s dates_sorted.csv'%filename,'r') as stationfile:
        reader = csv.reader(stationfile) 
        head=next(reader)
        dateidx=find_column("DATE",head)
        entindex=find_column("ENTRIES",head)
        exitindex=find_column("EXITS",head)
        timeidx=find_column("TIME",head)
        
        count=1
        for row in reader:
             try:
                 timechunks[str(row[timeidx])].append([count,row[dateidx]])
             except KeyError:
                 timechunks[str(row[timeidx])] = [[count,row[dateidx]]]
             count=count+1
        stationfile.seek(0)     
    
        s= timechunks.get(starttime)             
        e= timechunks.get(endtime)
                         
        lis = [line.split(",") for line in stationfile] 
        if(str(starttime)!="00:00:00" and str(endtime)!="00:00:00"):  
                
                 one_day_time(s,e,totalent,totalexit,lis,dateidx,entindex,exitindex)
                         
        elif(str(endtime)=="00:00:00"):
                 two_days_time2(s,e,totalent,totalexit,lis,dateidx,entindex,exitindex)
                 
        elif(str(starttime)=="00:00:00"):
                 two_days_time1(s,e,totalent,totalexit,lis,dateidx,entindex,exitindex)
                 
        stationfile.seek(0)
        return totalent, totalexit
    
    
def deal_with_data_error(s,e,j, days):
    s_date = datetime.strptime(s[j][1], '%m/%d/%Y')
    e_date = datetime.strptime(e[j][1], '%m/%d/%Y')
    news=[]
    newe=[]
    
    target_day=max(s_date,e_date)
    #print(target_day)
    for i in range(len(s)):
        if (datetime.strptime(s[i][1],'%m/%d/%Y') == target_day):
            for j in range(i,len(s)):
                news.append(s[j])
    for i in range(len(e)):
        if (datetime.strptime(e[i][1],'%m/%d/%Y') == target_day):
            for j in range(i,len(e)):
                newe.append(e[j])
    if(days==2):           
       newe.insert(0,newe[0])
    if(days==-2): 
       newe.pop(0)
       news.pop(len(news)-1)
    return news, newe
    
def two_days_time1(s,e,totalent,totalexit,lis,dateidx,entindex,exitindex):   
     for j in range(len(s)):
         if(s[j][1]==e[j+1][1]):
             totalent [lis[s[j][0]][dateidx]] = int(lis[e[j+1][0]][entindex])-int(lis[s[j][0]][entindex] )
             totalexit [lis[s[j][0]][dateidx]] = int(lis[e[j+1][0]][exitindex])-int(lis[s[j][0]][exitindex] )
         else:
             news, newe= deal_with_data_error(s,e,j,2)
             two_days_time1(news, newe,totalent,totalexit,lis,dateidx,entindex,exitindex)
                    
             return totalent,totalexit
         
def two_days_time2(s,e,totalent,totalexit,lis,dateidx,entindex,exitindex):   
     for i in range(len(s)):
         sday=datetime.strptime(s[i][1], '%m/%d/%Y')
         eday=datetime.strptime(e[i][1], '%m/%d/%Y')
         if(sday==eday-timedelta(days=1)):
             totalent [lis[s[i][0]][dateidx]] = int(lis[e[i][0]][entindex])-int(lis[s[i][0]][entindex] )
             totalexit [lis[s[i][0]][dateidx]] = int(lis[e[i][0]][exitindex])-int(lis[s[i][0]][exitindex] )
         else:
             news, newe= deal_with_data_error(s,e,i,-2)
             two_days_time2(news, newe,totalent,totalexit,lis,dateidx,entindex,exitindex)
                    
             return totalent,totalexit
         
def one_day_time(s,e,totalent,totalexit,lis,dateidx,entindex,exitindex):   
     for i in range(len(s)):
         if(s[i][1]==e[i][1]):
             totalent [lis[s[i][0]][dateidx]] = int(lis[e[i][0]][entindex])-int(lis[s[i][0]][entindex] )
             totalexit [lis[s[i][0]][dateidx]] = int(lis[e[i][0]][exitindex])-int(lis[s[i][0]][exitindex] )
         else:
             news, newe= deal_with_data_error(s,e,i,1)
             one_day_time(news, newe,totalent,totalexit,lis,dateidx,entindex,exitindex)
                    
             return totalent,totalexit
         
    
def get_all_entries_exits(filename,starttime,endtime):
    ent, exi= cal_ent_exi(filename,starttime,endtime)
    totalent=0
    totalexit=0
    length=min(len(ent),len(exi))
    
    for i in range(length):
        totalent=totalent+list(ent.values())[i]
        totalexit=totalexit+list(exi.values())[i]
       
    print ( "from ", starttime, "to ", endtime, "ent:",totalent)
    print ( "from ", starttime, "to ", endtime, "exit:",totalexit)
        
    return 

def entries_exits_in_4h_chunks(filename,continuous):
    time=sort_by_date(filename)
    if(continuous==True):
        for i in range(len(time)-1):
            get_all_entries_exits(filename,time[i],time[i+1]) 
        get_all_entries_exits(filename,time[len(time)-1],time[0]) 
    else:   
        for i in range(len(time)-1): 
            if(str(time[i])!=("20:00:00")):            
                get_all_entries_exits(filename,time[i],time[i+1])  
                       
        if(str(time[len(time)-1])!=("20:00:00")):
            get_all_entries_exits(filename,time[len(time)-1],time[0]) 
            
    os.remove('%s dates_sorted.csv'%filename)
    return
        
    
#sort_by_date("01-00-00")
#cal_ent_exi("01-00-00","20:00:00","00:00:00")
#get_all_entries_exits("01-00-00-Mon","16:00:00","20:00:00")
entries_exits_in_4h_chunks("01-00-00-Mon",True)
    
