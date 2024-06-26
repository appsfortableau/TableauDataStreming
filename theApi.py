from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'user',
    'password': 'userpassword',
    'database': 'my_database'
}

mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    password="userpassword",
    database="my_database"
)

def get_db_connection():
    """Function to get a database connection."""
    try:
        connection = mydb
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/api/last-10-records', methods=['GET'])
def get_last_10_records():
    """Endpoint to get the last 10 records from the database."""
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    cursor = connection.cursor(dictionary=True)

    try:
        # Adjust 'table_name' to your specific table name
        query = "SELECT * FROM transactions ORDER BY ID DESC LIMIT 10"
        cursor.execute(query)
        records = cursor.fetchall()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        return jsonify(records)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch data'}), 500
# print("Server is running", get_last_10_records())
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3308)
