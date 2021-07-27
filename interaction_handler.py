import sys
import os
import sqlite3
from datetime import datetime, timedelta

interactions_db = 'interactions.db'
def request_handler(request):
    
    if not 'host' in request['form']:
        return 'who is the host?'
    with sqlite3.connect(interactions_db) as c:
        
        #Connect to database specific to the user
        c.execute(
            f"""CREATE TABLE IF NOT EXISTS {request['form']['host']} (interaction text, start timestamp, end timestamp);""")
        
        #Get current date and clear dates that are too old
        currentTime = datetime.now()
        dateEdge = currentTime - timedelta(days = 20)
        
        c.execute(f'''DELETE FROM {request['form']['host']} WHERE end<= ?;''', (dateEdge,))
        
        ####POST REQUEST####
        if request['method'] == 'POST':
            if not 'name' in request['form']:
                return  'name of interaction unknown'
            
            
            if not('duration' in request['form'] and 'name' in request['form']):
                return 'missing parameters'
            
            #Subtract duration from current time to get the start time
            startTime = currentTime - timedelta(milliseconds=int(request['form']['duration']))
            
            #For some reason timestamps don't work unless I do the ? method
            c.execute(
                f'''INSERT into {request['form']['host']} VALUES ("{request['form']['name']}",?,?);''', (startTime, currentTime))
            
            print(currentTime)
            return startTime
            
        
        ####GET REQUEST####
        elif request['method'] == 'GET':
            
            # If a name is specified, get all interaction with that person. 
            if 'name' in request['form']:
                
                starts = c.execute(
                    f'''SELECT start FROM {request['form']['host']} WHERE interaction = "{request['form']['name']}" ORDER by start ASC;''').fetchall()
                ends = c.execute(
                    f'''SELECT end FROM {request['form']['host']} WHERE interaction = "{request['form']['name']}" ORDER by start ASC;''').fetchall()
                
                output = []
                
                for i in range(len(starts)):
                    start = datetime.strptime(starts[i][0], '%Y-%m-%d %H:%M:%S.%f')
                    end = datetime.strptime(ends[i][0], '%Y-%m-%d %H:%M:%S.%f')
                    duration = end - start
                    output.append((str(start), str(duration)))        
                return output
            
            # if no name specified get all interactions
            else:
                names = c.execute(f'''SELECT interaction FROM {request['form']['host']} ORDER by start ASC;''').fetchall()
                starts = c.execute(f'''SELECT start FROM {request['form']['host']} ORDER by start ASC;''').fetchall()
                ends = c.execute(f'''SELECT end FROM {request['form']['host']}  ORDER by start ASC;''').fetchall()
                output = {}
                for i in range(len(starts)):
                    name = names[i][0]
                    if not name in output:
                        output[name] = []
                    start = datetime.strptime(starts[i][0], '%Y-%m-%d %H:%M:%S.%f')
                    end = datetime.strptime(ends[i][0], '%Y-%m-%d %H:%M:%S.%f')
                    duration = end - start
                    output[name].append((str(start), str(duration)))
                return output
            
        else:
            return "Invalid method"


request = {
    'method': 'POST',
    'form': {
        'host': 'Diego',
        'name': 'berndo',
        'duration': '12345'
    }
}


print(request_handler(request))
