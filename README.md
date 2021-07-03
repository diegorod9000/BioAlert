# BioAlert
Proof of concept - a software that tracks an individual's past interactions with others, and alerts them if they have potentially been exposed to a virus.

# Initial Version
The current iteration consists of a Python script that can accept GET and POST requests. 

* POSTS are used to log in an interaction, giving the name of the person that the 
individual met with, and the duration of time it lasted. The date and time is recorded using datetime. Using SQLite, the script accesses (or creates) a table specific to the individual when 
a HTTP request is sent, using the .db file. The script then adds the interaction

* GET requests can either specify a person they interacted with, or collect every interaction. If a person is specified, a list consisting of tuples is returned,
each of which containing the start date, and the length of time. Otherwise, a dictionary is returned. Each "key" is a name, with its value being a list of tuples 
in the same format as the specified name. 

# TODO Deliverables

(ordered in most likely chronoligical order)

* script that can send Requests to HTTP Handler
* methiod of logging positive diagnosis
* method of alerting users of a potential contamination

(Might need to wait until I have better hardware)
* method of measuring interaction length, and acquiring information to log interactions
