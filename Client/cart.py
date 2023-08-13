import mysql.connector
from user import User

class Cart(): 
    def __init__(self):
        self.database = 'ecomproject1'
        self.table = 'cart'

    def connect_database(self,database):
        return mysql.connector.connect(
            host='localhost',#os.environ['HOST']
            user='teset',#os.environ['USER']
            password='bhdN__dhBqUI8L)5',#os.environ['DB_PASSWORD']
            database=database
        )
    
    def create_cart(self, username):
        try:
            query =f"INSERT INTO {self.table} (username) VALUES (?)"
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query, (username))
                connection.commit()
        except Exception as e:
            return False,"Error creating cart: " + str(e)

    
    def get_cart(self, username):
        try:
            query = f"SELECT products_list FROM {self.table} WHERE usersUid = '{username}'"
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
            if result:
                return result
            else:
                self.login_logger(username)
                return result
        except Exception as e:
            return False,"Error getting cart: " + str(e)
  

    def write_cart(self, userID, cart_products):  
        try:
            query = "UPDATE {table} SET product_list = (%s) WHERE usersUid = (%s);".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query, (str(cart_products), userID))
                connection.commit()
            print('Written')
        except Exception as e:
            print('Failed to write')
            return False,"Error writing cart: " + str(e)
