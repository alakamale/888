import datetime
import pytz
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
from ..lib.core import CoreOps as Core
from ..models.events import Events
from ..models.selection import Selection
from ..models.sports import Sports


###############################################################################################################
# Database connection
###############################################################################################################
class DataManager:

    def __init__(self):
        # Fill in the connection fields below
        self.password = 'root'                      # Need to update running locally
        self.user = 'root'                          # Need to update running locally
        self.host = 'localhost'                     # Need to update running locally
        self.db = 'League'
        self.sports_tab = 'Sports'
        self.events_tab = 'Events'
        self.selection_tab = 'Selection'
        self.db_Connection()
        self.create_database()
        self.create_tables()

    def db_Connection(self):
        # Trying to connect to MySQL database
        try:
            self.db_connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
            print("\nConnection to the database made!!")
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print("ERROR : Database does not exist.")
                exit(1)
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("ERROR : Username or password is wrong.")
                exit(1)
            else:
                print(error)
                exit(1)
        self.cursor = self.db_connection.cursor()

    def create_database(self):

        # Creating a database
        create_db_sql = "CREATE DATABASE IF NOT EXISTS {}".format(self.db)
        self.cursor.execute(create_db_sql)
        # Selecting our base
        use_db_sql = "use League".format(self.db)
        self.cursor.execute(use_db_sql)

    def create_tables(self):
        # Creating our table with some parameters
        self.create_sports_table()
        self.create_events_table()
        self.create_selection_table()

    def create_sports_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Sports (sport_Name VARCHAR(128) NOT NULL, sport_Slug varchar(128) NOT NULL,"
            " sport_Active boolean DEFAULT false, PRIMARY KEY(sport_Name));")

    def create_events_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Events (event_Name VARCHAR(128) NOT NULL, event_Slug varchar(128) NOT NULL,"
            " event_Active boolean DEFAULT false,event_Type enum(\"preplay\", \"inplay\") DEFAULT NULL,sport_Name VARCHAR(50),"
            " event_Status enum(\"Pending\", \"Started\", \"Ended\", \"Cancelled\") DEFAULT NULL,"
            " event_Scheduled_Start DATETIME,event_Actual_Start DATETIME DEFAULT NULL,PRIMARY KEY(event_Name),"
            " CONSTRAINT event_key FOREIGN KEY (sport_Name) REFERENCES Sports(sport_Name)ON DELETE SET NULL ON UPDATE CASCADE);")

    def create_selection_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Selection (selection_Name VARCHAR(128) NOT NULL, event_Name VARCHAR(128),"
            " selection_price DECIMAL(9,2), selection_Active boolean DEFAULT false,"
            " selection_Outcome enum(\"Unsettled\", \"Void\", \"Lose\", \"Win\") DEFAULT NULL,"
            " PRIMARY KEY(selection_Name),FOREIGN KEY (event_Name) REFERENCES Events(event_Name));")

    def add_a_sport(self):
        Sports.name, Sports.slug, Sports.active = Core.get_sport_data()

        # Performing data entry in our database
        sql = "INSERT INTO Sports (sport_Name, sport_Slug, sport_Active) " \
              "VALUES ('{}','{}',{})".format(Sports.name, Sports.slug, Sports.active)

        try:
            self.cursor.execute(sql)
            # self.db_connection.commit()
        except mysql.connector.Error as err:
            print("ERROR: {}".format(err))
            return False

    def add_a_event(self, sport_name):
        Events.name, Events.slug, Events.active, Events.event_type, Events.status, Events.scheduled_Start, Events.actual_Start = Core.get_event_data()
        # Performing data entry in our database
        sql = "INSERT INTO Events (event_Name, event_Slug, event_Active, event_Type, sport_Name, event_Status, event_Scheduled_Start, event_Actual_Start) " \
              "VALUES ('{}','{}',{},'{}','{}','{}','{}','{}')".format(Events.name, Events.slug, Events.active,
                                                                      Events.event_type, sport_name, Events.status,
                                                                      Events.scheduled_Start, Events.actual_Start)
        try:
            self.cursor.execute(sql)
            # self.db_connection.commit()
        except mysql.connector.Error as err:
            print("ERROR: {}".format(err))
            return False

    def add_a_selection(self, event_name):
        Selection.Name, Selection.event_Name, Selection.price, Selection.active, Selection.outcome = Core.get_selection_data(
            event_name)
        # Performing data entry in our database
        sql = "INSERT INTO Selection(selection_Name, event_Name, selection_price, selection_Active, selection_Outcome) " \
              "VALUES('{}','{}',{}, {}, '{}')".format(Selection.Name, Selection.event_Name, Selection.price,
                                                      Selection.active, Selection.outcome)
        try:
            self.cursor.execute(sql)
        except mysql.connector.Error as err:
            print("ERROR: {}".format(err))
            return False

    def commit_data(self):
        try:
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print("ERROR: {}".format(err))
            return False
        print("MESSAGE : SQL Query execute successfully.")

    def exit_menu(self):
        print("LOG : Closing DataBase connection.")
        self.cursor.close()
        self.db_connection.close()
        exit(0)

    def get_id(self, table_name, feild_name):
        sql = "SELECT {} FROM {}".format(feild_name, table_name)
        id_lst = self.sql_select_query(sql)

        # Validation if the read_data variable returns blank
        if id_lst == []:
            print("MESSAGE: Database is empty")
        else:
            return Core.name_selection(id_lst)

    def display_data(self, table_name, header_lst):
        sql = "SELECT * FROM {}".format(table_name)
        try:
            self.cursor.execute(sql)
            tab_results = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("ERROR: {}".format(err))
            return False

        print(tabulate(tab_results, headers=header_lst, tablefmt='psql'))
        pass

    def sql_execute_query(self, sql):
        try:
            self.cursor.execute(sql)
        except mysql.connector.Error as err:
            print("ERROR: {}".format(err))
            return False


    def sql_select_query(self, sql):
        try:
            self.cursor.execute(sql)
            data_lst = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("ERROR: {}".format(err))
            return False
        return data_lst

    def update_sport_tab_feild(self, table_name, primary_key):
        sports_hdr_lst = ['Sport Name', 'Slug', 'Active']
        new_table_dict = {}

        sql_fetch = "SELECT * FROM {} WHERE sport_Name='{}'".format(table_name, primary_key)
        data = self.sql_select_query(sql_fetch)
        if not data:
            print("ERROR : Sorry, Incorrect response.")
            return 1

        new_table_dict = Core.select_feild_to_update(table_name, sports_hdr_lst, data)

        sql_update = "UPDATE {} SET sport_Slug= '{}', sport_Active= '{}' WHERE sport_Name = '{}'".format(table_name, new_table_dict['Slug'], new_table_dict['Active'], primary_key)
        self.sql_execute_query(sql_update)
        self.commit_data()


    def update_event_tab_feild(self, table_name, primary_key):
        events_hdr_lst = ['Event Name', 'Slug', 'Active', 'Type', 'Sport Name', 'Event Status', 'Schedule Start', 'Actual Start']
        new_table_dict = {}

        sql_fetch = "SELECT * FROM {} WHERE event_Name='{}'".format(table_name, primary_key)
        data = self.sql_select_query(sql_fetch)
        if not data:
            print("ERROR : Sorry, Incorrect response.")
            return 1

        new_table_dict = Core.select_feild_to_update(table_name, events_hdr_lst, data)

        sql_update = "UPDATE {} SET event_Slug = '{}', event_Active = '{}', " \
                                    "event_Type = '{}', event_Status = '{}', " \
                                    "event_Scheduled_Start = '{}' WHERE event_Name = '{}'".format(
                                    table_name, new_table_dict['Slug'],new_table_dict['Active'],new_table_dict['Type'],
                                    new_table_dict['Event Status'], new_table_dict['Schedule Start'],
                                    primary_key)
        self.sql_execute_query(sql_update)

        if new_table_dict['Event Status'] == "Started" and not new_table_dict['Actual Start']:
            dt = datetime.datetime.now(pytz.timezone('UTC')).strftime("%Y-%m-%d %H:%M")
            sql_update = "UPDATE {} SET event_Actual_Start = '{}' WHERE event_Name = '{}'".format(table_name, dt, primary_key)
            self.sql_execute_query(sql_update)
        self.commit_data()

    def update_selection_tab_feild(self, table_name, primary_key):
        selection_hdr_lst = ['Selection Name', 'Event Name', 'Price', 'Active', 'Outcome']
        new_table_dict = {}

        sql_fetch = "SELECT * FROM {} WHERE selection_Name='{}'".format(table_name, primary_key)
        data = self.sql_select_query(sql_fetch)
        if not data:
            print("ERROR : Sorry, Incorrect response.")
            return 1

        new_table_dict = Core.select_feild_to_update(table_name, selection_hdr_lst, data)

        sql_update = "UPDATE {} SET selection_price = {}, selection_Active = '{}', selection_Outcome = '{}' WHERE selection_Name = '{}'".\
                        format(table_name, float(new_table_dict['Price']), new_table_dict['Active'], new_table_dict['Outcome'], primary_key)

        self.sql_execute_query(sql_update)
        self.commit_data()

    def delete_tab_feild(self, table_name, primary_key):
        if table_name == "Sports":
            key_feild = "sport_Name"
        elif table_name == "Events":
            key_feild = "event_Name"
        else:
            key_feild = "selection_Name"

        sql_delete = "DELETE FROM {} WHERE {}='{}'".format(table_name, key_feild, primary_key)
        self.sql_execute_query(sql_delete)
        self.commit_data()
