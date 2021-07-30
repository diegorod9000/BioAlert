# BioAlert
Proof of concept - a software that tracks an individual's past interactions with others, and alerts them if they have potentially been exposed to a virus.

# Interaction_Handler

* POSTS are used to log in an interaction, giving the name of the person that the 
individual met with, and the duration of time it lasted. The date and time is recorded using datetime. Using SQLite, the script accesses (or creates) a table specific to the individual when 
a HTTP request is sent, using the .db file. The script then adds the interaction

* GET requests can either specify a person they interacted with, or collect every interaction. If a person is specified, a list consisting of tuples is returned,
each of which containing the start date, and the length of time. Otherwise, a dictionary is returned. Each "key" is a name, with its value being a list of tuples 
in the same format as the specified name. 

# Diagnosis_Handler

## Function ##

* A POST is used to log a user's diagnosis. The disease name and date of diagnosis are logged. Each person that the user has interacted with in interactions.db are given an alert in alerts.db. The alert is given a danger level of 1, signifying that the person has actually been diagnosed. Future iterations will have more danger levels, signifying that instead of directly interacting with a person diagnosed with the disease, the person getting the alert is rather at risk of secondhand infection by a degree of separation.

* A GET Request will check the user's alerts.db table, and return all of the alerts in a list of tuples containing the name, date, disease, and danger level (outdated alerts are deleted). If a user has no alerts, "safe" is returned instead.

## TODO ##

* Implement other danger levels, change method of identifying users.

# TODO Deliverables

(ordered in most likely chronoligical order)

* script that can send Requests to HTTP Handler

(Might need to wait until I have better hardware)
* method of measuring interaction length, and acquiring information to log interactions
