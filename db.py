import sqlite3

class ChatGPTDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        
        #Creates a new table in the database with the given name and column
        #The columns parameter should be a comma-seperate string of column

        create_table_sq1 = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(create_table_sq1)
        self.conn.commit()

    def insert_record(self, table_name, columns, record): 
        
        #Insert a record to a target table with values seperate by a comma

        sq1 = f'INSERT INTO {table_name} ({columns}) VALUES ({record})'
        print(sq1)
        self.cursor.execute(sq1)
        self.conn.commit()

    def retrieve_records(self, table_name, conditions=None):

        #Retrieves all records from the specified table in the databsee
        #The conditions parameter should be a string that represents a SQ1

        select_sq1 = f"SELECT * FROM {table_name}"
        if conditions:
            select_sq1 += f" WHERE {conditions}"
        self.cursor.execute(select_sq1)
        return self.cursor.fetchall()
    
    def close(self):
        print('db closed')
        self.cursor.close()
        self.conn.close()
