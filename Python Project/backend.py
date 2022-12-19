### Importing the packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from IPython.display import display, HTML
import pandas as pd
import sqlite3
from sqlite3 import Error

### Global variable
filename = 'insurance.csv'

### Fetch data from the csv file
def fetch_data_from_csv(filename):
    ### Initialize values
    titles = []
    rows = []
    
    ### Reading the csv file
    with open(filename, 'r') as csv_file:
        ### Creating a csv reader object
        csv_reader = csv.reader(csv_file)
        
        ### Extracting the titles from the first row
        titles = next(csv_reader)
        
        ### Extracting each record one by one
        for each_record in csv_reader:
            rows.append(each_record)
    return titles, rows

titles, rows = fetch_data_from_csv(filename)

### Helper function to create a connection
def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)
    return conn

### Helper function to create a table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

### Helper function to execute a sql statement
def execute_sql_statement(sql_statement, conn):
    cur = conn.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()
    return rows

### Fetching age data from the csv file
def fetch_age():
    titles, rows = fetch_data_from_csv(filename)
    age_index = titles.index('age')
    age_data = []
    for each_row in rows:
        age_data.append(int(each_row[age_index]))
    return age_data

### Fetching sex data from the csv file
def fetch_sex():
    titles, rows = fetch_data_from_csv(filename)
    sex_index = titles.index('sex')
    sex_data = []
    for each_row in rows:
        sex_data.append(each_row[sex_index])
    return sex_data

### Fetching bmi data from the csv file
def fetch_bmi():
    titles, rows = fetch_data_from_csv(filename)
    bmi_index = titles.index('bmi')
    bmi_data = []
    for each_row in rows:
        bmi_data.append(float(each_row[bmi_index]))
    return bmi_data

### Fetching children data from the csv file
def fetch_children():
    titles, rows = fetch_data_from_csv(filename)
    children_index = titles.index('children')
    children_data = []
    for each_row in rows:
        children_data.append(int(each_row[children_index]))
    return children_data

### Fetching smoker data from the csv file
def fetch_smoker():
    titles, rows = fetch_data_from_csv(filename)
    smoker_index = titles.index('smoker')
    smoker_data = []
    for each_row in rows:
        smoker_data.append(each_row[smoker_index])
    return smoker_data

### Fetching region data from the csv file
def fetch_region():
    titles, rows = fetch_data_from_csv(filename)
    region_index = titles.index('region')
    region_data = []
    for each_row in rows:
        region_data.append(each_row[region_index])
    return region_data

### Fetching charges data from the csv file
def fetch_charges():
    titles, rows = fetch_data_from_csv(filename)
    charges_index = titles.index('charges')
    charges_data = []
    for each_row in rows:
        charges_data.append(float(each_row[charges_index]))
    return charges_data

### Insert data into Customer table
def insert_into_customer(conn, values):
    sql = "INSERT INTO Customer(CustomerID, Age, Sex, Smoker, BMI, Children, Charges, RegionID) VALUES(?, ?, ?, ?, ?, ?, ?, ?);"
    cur = conn.cursor()
    cur.execute(sql, values)
    return cur.lastrowid

### Create Customer Table
def create_customer_table(conn):
    ### Create Table - Customer
    create_customer = """CREATE TABLE Customer(
            CustomerID Integer not null primary key,
            Age integer not null, 
            Sex Text not null, 
            Smoker Text not null,
            BMI Real not null,
            Children integer not null,
            Charges Real not null,
            RegionID integer not null,
            FOREIGN KEY(RegionID) REFERENCES Region(RegionID));
            """
    with conn:
        create_table(conn, create_customer)
    
    ### Fetch all the values
    age_data = fetch_age()
    sex_data = fetch_sex()
    bmi_data = fetch_bmi()
    children_data = fetch_children()
    smoker_data = fetch_smoker()
    region_data = fetch_region()
    charges_data = fetch_charges()
    
    region_data_to_id_dict = dict()
    unique_regions = list(set(region_data))
    for region in unique_regions:
        if region not in region_data_to_id_dict:
            region_data_to_id_dict[region] = unique_regions.index(region) + 1
    
    ### Insert data into Customer
    for index in range(len(age_data)):
        row_values = (index + 1, age_data[index], sex_data[index], smoker_data[index], bmi_data[index], children_data[index], charges_data[index], region_data_to_id_dict[region_data[index]])
        insert_into_customer(conn, row_values)
    
    ### Save the data
    conn.commit()

### Insert data into Region table
def insert_into_region(conn, values):
    sql = "INSERT INTO Region(RegionID, Region) VALUES(?, ?);"
    cur = conn.cursor()
    cur.execute(sql, values)
    return cur.lastrowid

### Create Region table
def create_region_table(conn):
    ### Create Table - Region
    create_region = """CREATE TABLE Region(
            RegionID Integer not null primary key,
            Region Text not null);
            """
    with conn:
        create_table(conn, create_region)
        
    ### Fetch all the values
    region_data = fetch_region()
    
    region_data_to_id_dict = dict()
    unique_regions = list(set(region_data))
    for region in unique_regions:
        if region not in region_data_to_id_dict:
            region_data_to_id_dict[region] = unique_regions.index(region) + 1
    
    new_region = list(region_data_to_id_dict.keys())
    new_region_ids = list(region_data_to_id_dict.values())
    
    ### Insert data into Region
    for index in range(len(new_region)):
        row_values = (new_region_ids[index], new_region[index])
        insert_into_region(conn, row_values)
    
    ### Save the data
    conn.commit()    
        
        
### Functions to be called in analysis.py    
def setup_database():
    ### Create a connection for the normalized database and create Customer, TitleDetails table
    normalized_connection = create_connection('normalized.db', True)
    create_region_table(normalized_connection)
    create_customer_table(normalized_connection)
    normalized_connection.close()
    
### Fetch data for analysis
def fetch_customer_data():
    normalized_connection = create_connection('normalized.db', False)
    data = pd.read_sql_query("SELECT * FROM Customer", normalized_connection)
    normalized_connection.close()
    return data
    
### Function to return Charges, Smoker, Sex data
def fetch_charges_smoker_sex_data():
    normalized_connection = create_connection('normalized.db', False)
    charges_smoker_sex_data = pd.read_sql_query("SELECT Charges, Smoker, Sex FROM Customer", normalized_connection)
    normalized_connection.close()
    return charges_smoker_sex_data

### Function to return Age, Sex data
def fetch_age_sex_data():
    normalized_connection = create_connection('normalized.db', False)
    age_sex_data = pd.read_sql_query("SELECT Age, Sex FROM Customer", normalized_connection)
    normalized_connection.close()
    return age_sex_data

### Function to return Smokers per each Region
def fetch_smokers_region_data():
    normalized_connection = create_connection('normalized.db', False)
    smokers_region_data = pd.read_sql_query("""select 
                                               Rg.Region, 
                                               count(ct.CustomerID) Number_of_Smokers
                                               from Customer ct 
                                               join Region Rg
                                               on ct.RegionId = Rg.RegionId
                                               where ct.Smoker = 'yes'
                                               group by Rg.Region
                                               order by count(ct.CustomerID)""", normalized_connection)
    normalized_connection.close()
    return smokers_region_data

### Function to return Customers per each Region
def fetch_customers_region_data():
    normalized_connection = create_connection('normalized.db', False)
    customers_region_data = pd.read_sql_query("""select 
                                                 Rg.Region, 
                                                 count(ct.CustomerID) Number_of_Customers
                                                 from Customer ct 
                                                 join Region Rg
                                                 on ct.RegionId = Rg.RegionId
                                                 group by Rg.Region
                                                 order by count(ct.CustomerID)""", normalized_connection)
    normalized_connection.close()
    return customers_region_data

def fetch_age_count_data():
    normalized_connection = create_connection('normalized.db', False)
    age_count_data = pd.read_sql_query("""select 
                                                 case
                                                WHEN Age BETWEEN 18 AND 30 THEN '18-30'
                                                WHEN Age BETWEEN 31 AND 40 THEN '31-40'
                                                WHEN Age BETWEEN 41 AND 50 THEN '41-50'
                                                WHEN Age BETWEEN 51 AND 60 THEN '51-60'
                                                WHEN Age BETWEEN 61 AND 70 THEN '61-70'
                                                end as Age_Range, 
                                                 count(*) Number_of_Customers
                                                 from Customer
                                                 group by Age_Range 
                                                 """, normalized_connection)
    normalized_connection.close()
    return age_count_data

def fetch_age_and_smoker_data():
    normalized_connection = create_connection('normalized.db', False)
    age_and_smoker_data = pd.read_sql_query("""select 
                                                 case
                                                WHEN Age BETWEEN 18 AND 30 THEN '18-30'
                                                WHEN Age BETWEEN 31 AND 40 THEN '31-40'
                                                WHEN Age BETWEEN 41 AND 50 THEN '41-50'
                                                WHEN Age BETWEEN 51 AND 60 THEN '51-60'
                                                WHEN Age BETWEEN 61 AND 70 THEN '61-70'
                                                end as Age_Range, 
                                                 count(*) Number_of_Customers
                                                 from Customer
                                                 where Smoker = 'yes'
                                                 group by Age_Range 
                                                 """, normalized_connection)
    normalized_connection.close()
    return age_and_smoker_data

def fetch_age_data():
    normalized_connection = create_connection('normalized.db', False)
    age_data = pd.read_sql_query("""select 
                                        Age
                                        from Customer
                                                 
                                        """, normalized_connection)
    normalized_connection.close()
    return age_data

def fetch_age_charges_data():
    normalized_connection = create_connection('normalized.db', False)
    age_charges_data = pd.read_sql_query("""select 
                                                 case
                                                WHEN Age BETWEEN 18 AND 30 THEN '18-30'
                                                WHEN Age BETWEEN 31 AND 40 THEN '31-40'
                                                WHEN Age BETWEEN 41 AND 50 THEN '41-50'
                                                WHEN Age BETWEEN 51 AND 60 THEN '51-60'
                                                WHEN Age BETWEEN 61 AND 70 THEN '61-70'
                                                end as Age_Range, 
                                                 avg(Charges) Mean_Charges
                                                 from Customer
                                                 group by Age_Range 
                                                 """, normalized_connection)
    normalized_connection.close()
    return age_charges_data

def fetch_region_charges_data():
    normalized_connection = create_connection('normalized.db', False)
    region_charges_data = pd.read_sql_query("""select 
                                               Rg.Region, 
                                               avg(ct.Charges) Mean_Charges
                                               from Customer ct 
                                               join Region Rg
                                               on ct.RegionId = Rg.RegionId
                                               group by Rg.Region
                                                
                                                 """, normalized_connection)
    normalized_connection.close()
    return region_charges_data

def fetch_bmi_sex_data():
    normalized_connection = create_connection('normalized.db', False)
    bmi_sex_data = pd.read_sql_query("""select 
                                        bmi,sex 
                                        from customer
                                                 """, normalized_connection)
    normalized_connection.close()
    return bmi_sex_data

def fetch_correlation_data():
    normalized_connection = create_connection('normalized.db', False)
    correlation_data = pd.read_sql_query("""select 
                                        age,bmi,children,charges 
                                        from customer
                                                 """, normalized_connection)
    normalized_connection.close()
    return correlation_data
