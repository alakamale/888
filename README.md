# 888
This algorithm is a CRUD made in python that has the purpose of the four basic operations (creation, access, updating and destruction of data) used in relational databases (RDBMS).

## Requirements
You will need to install the library below:
- tabulate==0.8.9
- pytz==2021.1
- mysql_connector_repackaged==0.3.1
- unicode_slugify==0.1.3
- You will need to instal MySQL.
        
## Operation
## Home screen
When initializing the code, the first screen that is presented is the selection menu screen below:

On this screen we can execute the 4 basic commands of a CRUD (Create, Read, Update and Delete).

## Option 1
Selecting option 1, we can insert a new record in our database.

## Option 2
Selecting option 2, we can read all parameters table.
- Presentation of the complete database.

## Option 3
Selecting option 3, we can update our base records.

## Option 4:
Selecting option 4, we can delete a record in our database (Selection Table working)


## NOTE
- Need to update USER , HOST and PASSWORD for MySQL DB in data_management.py file

        self.password = 'root'                      # Need to update running locally
        self.user = 'root'                          # Need to update running locally
        self.host = 'localhost'                     # Need to update running locally
 
 - Sample output filee located at : sample/Sample_Output.txt
 - Things pending for implementation, 
1. Delete entries with foreign key
2. Search with FILTERS
3. Active results for different tables
4. Unit Test
5. CLI Help
  
