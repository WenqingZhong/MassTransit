# -*- coding: utf-8 -*-
"""
Created on Thurs Aug 13 2020
@author: Mehr Kaur
"""

#import statements
from algorithm import get_crowds, grade_crowds
from datetime import date,time, datetime
from flask import Flask, render_template

#Flask app variable
app = Flask(__name__)

#static route
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/96th")
def f96th():
    
    #dateRequest = date(datetime.now())
    #timeRequest = time(datetime.now())
    #entries, crowdSize = get_crowds(dateRequest,timeRequest,'120')
    #crowdRank = grade_crowds(crowdSize)
    #result = str(crowdSize[0])
    
    #print("There are " + str(crowdSize[0]) + " people on the Northbound platform.")
    #print("The Northbound platform is at risk level " + str(crowdRank[0]) + ".")
    #print("There are " + str(crowdSize[1]) + " people on the Southbound platform.")
    #print("The Southbound platform is at risk level " + str(crowdRank[1]) + ".")
    
    #result = do_calculation(number1, number2)
    #return '''
        #<html>
            #<body>
                #<h1>Stay Subway Safe</h1>
                #<p>There are {result} people on the Northbound platform.</p>
            #</body>
        #</html>
    #'''.format(result=result)
    return render_template("96th.html") 
    #<p>The result is {result}</p>
#start the server
if __name__ == "__main__":
    app.run()