# Mayors

French mayors database and analysis

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites

What packages you need to install to run the application

```
- sqlalchemy	- unidecode
- numpy			- re
- bs4			- fuzzywuzzy
- requests		- pandas 
- csv 			- matplotlib
```


## Running the app

You will type commands in your terminal with the following format :
``` 
python3 app.py -f <function> -a <argument>
```


#### Functions 

Choose one of the 4 functions :

* `init_database` 
	* takes no argument
	* creates a new files for the database, or resets it if you want to start populating the database with new conditions

* `populate`
	* arguments : 
		- any valid postal code (ex : 91190)
		- any valid department code (ex : 92)
		- the name of a city (ex : Paris)
	* populates the empty base you just initialized

* `display`
	* arguments :
		- any valid postal code (ex : 91190)
		- any valid department code (ex : 92)
		- the name of a city (ex : Paris)		
	* prints the data in your terminal

* `analyse`
	* arguments :
		- city_map : draws a map of your requested cities, with the color of their party
		- pop_per_party : prints in the terminal the distribution of parties in the database 
		-
		-


Look at an example :

```
python3 app.py -f init_database
python3 app.py -f populate -a 92
python3 app.py -f display -a 92
python3 app.py -f display -a Antony
python3 app.py -f analyse -a 
```

## Output

The folder `export` contains a CSV file for the database you just built