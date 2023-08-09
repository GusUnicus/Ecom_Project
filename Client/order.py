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
            database=database#os.environ['DATABASE']
        )
    
    def write_order(self, username, cart_products):
        cursor = self.connection.cursor()
        try:
            query = f"INSERT INTO {self.table} (username, products_list) VALUES ('{username}', '{str(cart_products)}')"
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
            return
        except Exception as e:
            return False,"Error writing order: " + str(e)
      