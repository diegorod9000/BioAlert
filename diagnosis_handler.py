import sys
import os
import sqlite3
from datetime import datetime, timedelta

interactions_db = 'interactions.db'
alerts_db = 'alerts.db'

def request_handler(request):
    ####GET####
    if request['method'] == 'GET':
        with sqlite3.connect(alerts_db) as c:
            
            c.execute(
                f"""CREATE TABLE IF NOT EXISTS {request['form']['host']} (contaminant text, disease text, date timestamp, priority int);""")
            
            #Gets list of all people who may have contaminated the user 
            contaminants = c.execute(f'''SELECT name from {request['form']['host']}''').fetchall()
            
            if len(contaminants) == 0:
                return "Safe"
            diseases = c.execute(f'''SELECT disease from {request['form']['host']}''').fetchall()
            dates = c.execute(f'''SELECT date from {request['form']['host']}''').fetchall()
            danger_levels = c.execute(f'''SELECT priority from {request['form']['host']}''').fetchall()
            
            output = []
                
            for i in range(len(contaminants)):
                date = datetime.strptime(dates[i][0], '%Y-%m-%d %H:%M:%S.%f')
                danger = int(danger_levels[i][0])
                output.append(contaminants[i][0], diseases[i][0], date, danger) 
            return output
            
    ####POST####
    elif request['method'] == 'POST':
        #puts the user's name on the alerts of everyone who has interacted with them, and recursively does it with a lower priority
        # TODO: Add recursive calls
        numcontacts = 0
        now = datetime.now()
        disease = request['form']['disease']
        hosts = set()
        with sqlite3.connect(interactions_db) as c:
            c.execute(
                f"""CREATE TABLE IF NOT EXISTS {request['form']['host']} (interaction text, start timestamp, end timestamp);""")
            
            hosts_raw = c.execute(f'''SELECT interaction FROM {request['form']['host']};''').fetchall()
            for interaction in hosts_raw:
                hosts.add(interaction[0])
                
        with sqlite3.connect(alerts_db) as c:
            for name in hosts:
                c.execute(
                    f"""CREATE TABLE IF NOT EXISTS {name} (contaminant text, disease text, date timestamp, priority int);""")
                c.execute(
                    f'''INSERT into {name} VALUES ("{request['form']['name']}",?,?);''', (disease,now,1))
        
        
    else:
        return "Invalid method"
