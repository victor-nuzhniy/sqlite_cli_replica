# sqlite_cli_replica
Replica sqlite cli. Python.

# Welcome to My Sqlite
***

## Task

The task consists of two parts.
First part.
We create a class with a similar behavior than a request on the real sqlite.
All methods in the task, except run, will return an instance of my_sqlite_request.
!!!
All implemented methods name are the same in the task except:
from (we have from_);
join (we have join_);
set (we have set_).
Thats because that words are reserved in Python.


Second part.
We create the program which will be a Command Line Interface (CLI) to your MySqlite class.
We will run it with python my_sqlite_cli.py.
For that reason we create the class Interpreter and parsing part of the code.

## Description

First part.
Every method in the next list is prepairing for execution of the request (from, where,
join, order, values, set).
The "run" method is launching the script and the code executing the request. The way of
execution depends on the availability of the methods from the next list (select, insert, 
update, delete).
'Values' is used with the 'insert' method. 'Set' is used with the 'update' method.
!!!
The result of 'insert', 'update' and 'delete' methods don't print to the terminal,
their result we can see in changing csv.file. 

Second part.
Parsing part of the code split the input string into command and argument, using regular
expression. The class Interpreter we use to 'translate' in some way parsed commands to 
the class MySqliteRequest from the first part.


## Installation

First part.
To run the code we write the command 'python my_sqlite_request.py' in the terminal.
The command to perform must be wrote down in the end of the code (you can see there some).
There some example of the code to use:

request = MySqliteRequest()
request = request.from_('nba_player_data.csv')
request = request.select('name')
request = request.where('birth_date', 'December 11, 1976')
request.run()

request = MySqliteRequest()
request.insert('nba_player_data.csv')
request = request.values({'name': 'Alaa Abdelnaby', 'year_start': '1991', 'year_end': '1995',
 'position': 'F-C', 'height': '6-10', 'weight': '240', 'birth_date': "June 24, 1968", 'college': 'Duke University'})
request.run()

request = MySqliteRequest()
request = request.select('name')
request = request.from_('nba_player_data.csv')
request = request.where('name', 'Alaa Abdelnaby')
request.run()

Second part. 
To run the code we write the command 'python my_sqlite_cli.py' in the terminal.

## Usage

First part.
The command to perform must be wrote down in the end of the code (you can see there some).

Second part. 
Commands is described in the task, you need to use it similar to those in
'ruby' or 'js' examples.
Note, that if filename include such symbols as '()', you must use quotes. The same is with parameters 
and using space - you must use quotes. For example: year_start = 'June 15, 1961'.
You must use space to divide commands and parameters making requests.
For examples of input see 'example'.  

### The Core Team
Nuzhnyi Victor


<span><i>Made at <a href='https://qwasar.io'>Qwasar Silicon Valley</a></i></span>
<span><img alt='Qwasar Silicon Valley Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px'></span>
