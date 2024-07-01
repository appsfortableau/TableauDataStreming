import pandas as pd
import numpy as np
from faker import Faker
import random
import time

import mysql.connector

fake = Faker()

num_transactions = 100000
num_products = 50
regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
states = ['New York', 'California', 'Texas', 'Florida', 'Ohio', 'North Carolina', 'Michigan', 'Washington', 'Arizona', 'Georgia', 'Tennessee', 'Indiana', 'Massachusetts', 'Missouri', 'Maryland', 'Wisconsin', 'Colorado', 'Minnesota', 'South Carolina', 'Alabama', 'Louisiana', 'Kentucky', 'Oregon', 'Oklahoma', 'Connecticut', 'Iowa', 'Mississippi', 'Arkansas', 'Utah', 'Nevada', 'Kansas', 'New Mexico', 'Nebraska', 'West Virginia', 'Idaho', 'Maine', 'New Hampshire', 'Montana', 'Rhode Island', 'Delaware', 'South Dakota', 'North Dakota', 'Vermont', 'Wyoming']
date_range = pd.date_range(start='1/1/2015', end='12/31/2024', freq='D')
start_date = date_range[0]  
last_used_date = start_date
product_ids = [f'P{str(i).zfill(4)}' for i in range(1, num_products + 1)]
products = [{'Product ID': pid, 'Product Name': fake.word(), 'Category': fake.word()} for pid in product_ids]

transactions = []
id = 0
for _ in range(num_transactions):
    id = id + 1
    transaction_id = fake.uuid4()
    timestamp = last_used_date + pd.DateOffset(seconds=random.randint(0, 86400))
    last_used_date = timestamp
    product = random.choice(products)
    product_id = product['Product ID']
    
    # Simulate decr amount for a period
    if timestamp < start_date + pd.DateOffset(days=30):
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(5.0, 100.0), 2)
    else:
        # Simulate increasing quttiity
        quantity = random.randint(5, 10)
        unit_price = round(random.uniform(5.0, 100.0), 2)
    
    total_amount = round(quantity * unit_price, 2)
    state = random.choice(states)
    
    transactions.append({
        'ID': id,
        'Transaction ID': transaction_id,
        'Timestamp': timestamp,
        'Product ID': product_id,
        'Quantity': quantity,
        'Unit Price': unit_price,
        'Total Amount': total_amount,
        'state': state, 
    })

# Convert to DataFrame
transactions_df = pd.DataFrame(transactions)
products_df = pd.DataFrame(products)

# Calculate Revenue Data
transactions_df['Date'] = transactions_df['Timestamp'].dt.date
revenue_df = transactions_df.groupby('Date').agg({'Total Amount': 'sum'}).cumsum().reset_index()
revenue_df.columns = ['Timestamp', 'Total Revenue']

# Display the first few rows of each DataFrame
transactions_df.head(), products_df.head(), revenue_df.head()

# create a table in the database mysql 
# connect to mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    password="userpassword",
    database="my_database"
)

print(mydb)
# if table does not exist, create table
mycursor = mydb.cursor()
tableName = "transactions"
mycursor.execute(f"SHOW TABLES LIKE '{tableName}'")
result = mycursor.fetchone()
if result:
    # drop the table
    # mycursor.execute(f"DROP TABLE {tableName}")
    print(f"Table {tableName} exists")
else:
    mycursor.execute(f"CREATE TABLE {tableName} (ID INT AUTO_INCREMENT PRIMARY KEY, Timestamp DATETIME, ProductID VARCHAR(255), Quantity INT, UnitPrice FLOAT, TotalAmount FLOAT, State VARCHAR(255))")
    mydb.commit()
    print(f"Table {tableName} created")

# insert data into the table batch size 
batch_size = 100
batch_count = len(transactions_df) // batch_size

for i in range(batch_count):
    start_index = i * batch_size
    end_index = (i + 1) * batch_size
    batch_df = transactions_df.iloc[start_index:end_index]

    sql = f"INSERT INTO {tableName} (Timestamp, ProductID, Quantity, UnitPrice, TotalAmount, State) VALUES (%s, %s, %s, %s, %s, %s)"
    values = []
    for index, row in batch_df.iterrows():
        timestamp = row['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        val = (timestamp, row['Product ID'], row['Quantity'], row['Unit Price'], row['Total Amount'], row['state'])
        values.append(val)

    mycursor.executemany(sql, values)
    mydb.commit()
    print(mycursor.rowcount, "records inserted.")

    time.sleep(5)




 

# print(transactions_df.head())
