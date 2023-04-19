import pyodbc

# Set up the connection parameters
driver = 'ODBC Driver 18 for SQL Server'
server = 'tcp:<server_name>'
database = '<database_name>'
username = '<username>'
password = '<password>'

# Connect to the database
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
cnxn = pyodbc.connect(connection_string)

# Create a cursor object
cursor = cnxn.cursor()

# Execute a SQL query
query = "SELECT * FROM my_table"
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)
    
# Close the cursor and connection
cursor.close()
cnxn.close()
