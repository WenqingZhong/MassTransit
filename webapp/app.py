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
    
    dateRequest = datetime.date(datetime.now())
    timeRequest = datetime.time(datetime.now())
    entries, crowdSize = get_crowds(dateRequest,timeRequest,'120')
    crowdRank = grade_crowds(crowdSize)
    northNum = str(crowdSize[0])
    northRisk = str(crowdRank[0])
    southNum = str(crowdSize[1])
    southRisk = str(crowdRank[1])
    
    #print("There are " + str(crowdSize[0]) + " people on the Northbound platform.")
    #print("The Northbound platform is at risk level " + str(crowdRank[0]) + ".")
    #print("There are " + str(crowdSize[1]) + " people on the Southbound platform.")
    #print("The Southbound platform is at risk level " + str(crowdRank[1]) + ".")
    
    #result = do_calculation(number1, number2)
    return '''
        <html>
            <body>
                <h1>Stay Subway Safe</h1>
                <h2>96th Street, now</h2>
                <p>There are {0} people on the Northbound platform.</p>
                <p>The Northbound platform is at risk level {1}.</p>
                <p>There are {2} people on the Southbound platform.</p>
                <p>The Southbound platform is at risk level {3}.</p>
            </body>
        </html>
    '''.format(northNum,northRisk,southNum,southRisk)
    #return render_template("96th.html") 
    #<p>The result is {result}</p>
#start the server
if __name__ == "__main__":
    app.run()