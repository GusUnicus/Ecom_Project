import mysql.connector
from datetime import datetime

class Order(): 
    def __init__(self):
        self.database = 'ecomproject1'
        self.table = 'orders'

    def connect_database(self,database):
        return mysql.connector.connect(
            host='localhost',#os.environ['HOST']
            user='teset',#os.environ['USER']
            password='bhdN__dhBqUI8L)5',#os.environ['DB_PASSWORD']
            database=database
        )
    
    def write_order(self, userID, cart_products):
        try:
            query = "INSERT INTO {table} (usersUid, order_items) VALUES (%s, %s)".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(userID,str(cart_products)))
                connection.commit()
            return
        except Exception as e:
            return False,"Error writing order: " + str(e)
      