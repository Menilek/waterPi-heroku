from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def formatReadingDataForDisplay(data):
    formattedTime = data[0].strftime('%H:%M %d/%m/%Y')
    litres = data[1]
    percent = data[2]
    items = [formattedTime, litres, percent]
    return(items)

def getLastReadingFromDB():
    queryData = db.engine.execute("SELECT date_trunc('second', created_on), litres, percentage FROM Reading ORDER BY id DESC LIMIT 1").first()
    formattedData = formatReadingDataForDisplay(queryData)
    return(formattedData)

def handleError(data):
    db.session.rollback()
    db.session.add(data)
    db.session.flush()

def insertNewReadingToDB(waterData):
    reading = Reading(waterData[0], waterData[1])
    try:
        db.session.add(reading)
        db.session.commit()
        db.session.close()
    except:
        handleError(reading)

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    litres = db.Column(db.Numeric, nullable = False)
    percentage = db.Column(db.Integer, nullable = False)
    created_on = db.Column(db.DateTime, default=datetime.now, index = True)    

    def __init__(self, litres, percentage, created_on=None):
        self.litres = litres
        self.percentage = percentage
