# ECE356_Course_Project
This repo includes the work for ECE356 Internet Traffic course project (Group 20)
## Table of contents
* [General info](#general-info)
* [Deliverables](#deliverables)
* [CLI Setup](#cli-setup)
* [Data Mining Setup](#data-mining-setup)

## General info
This project is a database client application for Internet Service Provider (ISP) network administrators using the Unicauca Network Flows Dataset, which is obtained from https://www.kaggle.com/jsrojas/labeled-network-traffic-flows-114-applications. 
	
## Deliverables
1. `Internet_Traffic_ER_Model.pdf` is the ER Model for the project
2. `load_data.sql` loads all data from the source dataset to a table
3. `create_er.sql` creates the relational schema for the ER model and load data from the table created by running `load_data.sql`
4. `client_app.py` is the main file for the CLI
5. `create_account.py` is the untility file that allows user to create an account before using the CLI
6. `create_account.sql` creates a table that stores all registered user account
7. `handle_command.py` is the utility file that handles commands entered by user
8. `map_file.py` stores some useful dictionaries and lists to be used by `handle_command.py`
9. `data_mining.py` is the main file for the data mining exercise
10. `data_mining.sql` has the queries needed to perform data mining exercise
11. `Report.pdf` contains detailed information about this project, including design, implementation, test plan, data mining, etc.
12. `Video Demo.mp4` is a brief video demo that introduces the project
	
## CLI Setup
1.  Before running this project, user needs to run `load_data.sql` and `create_er.sql` to populate the data tables
2.  User needs to run `create_account.sql` to create a user account table
2.  To run this project, run `python3 client_app.py`.
3.  Then the user will be promoted to register a user account with appropriate privilege.
4.  Once registered successfully, user needs to enter the user name and password again to login
5.  Once logged in, user can start enter commands
6.  User can exit the CLI by entering `exit` to the ternimal
## Data Mining Setup
1.  To run the data mining exercise, run `python3 data_mining.py`
2.  It will generate a plot which shows how usage frequency of web services evolves during different hours of a day

