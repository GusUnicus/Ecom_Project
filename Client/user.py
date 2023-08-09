import mysql.connector
import uuid, secrets, string
from datetime import datetime

class User():

 
    def __init__(self):
        self.database = 'ecomproject1'
        self.table = 'users'

    def connect_database(self,database):
        return mysql.connector.connect(
            host='localhost',
            user='teset',
            password='bhdN__dhBqUI8L)5',
            database=database
        )

    def get_data(self):
        try:
            query = 'SELECT * FROM {table};'.format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
                return data
        except Exception as e:
            return "Error :" + str(e)

    def create_user(self,first_name, last_name, username, email,password):
            try:
                data = {
                    'usersUid':self.generate_secure_uuid(),
                    'usersName':username,
                    'first_name': first_name,
                    'last_name':last_name,
                    'usersEmail':email,
                    'usersPwd':password,
                    
                }
                query = "INSERT INTO {table} (usersUid, usersName, first_name, last_name, usersEmail, usersPwd) VALUES (%s, %s, %s, %s, %s, %s);".format(table=self.table)
                with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                    cursor.execute(query,data['usersUid'],data['usersName'],data['first_name'],data['last_name'],data['usersEmail'],data['usersPwd'])
                    connection.commit() 
                    return True,self.get_user(email)
            except Exception as e:
                return False,"Error creating user: " + str(e)
    
    def get_user(self,email):
        try:
            query = "SELECT * FROM {table} WHERE usersEmail = %s;".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,email)
                result = cursor.fetchone()
            if result:
                return True,result
            else:
                self.login_logger(email)
                return False,result
        except Exception as e:
            return "Error logging in: " + str(e)
        
    def get_email(self, username):
        try:
            query = "SELECT email FROM {table} WHERE usersName = '%s';".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,username)
                result = cursor.fetchone()
            if result:
                return True,result
            else:
                self.login_logger(username)
                return False,result
        except Exception as e:
            return False,str(e)
        
    
    def update_password(self, username, password):
        try:
            if self.get_email(username)[0]:
                query = "UPDATE {table} SET usersPwd = '{password}' WHERE usersName = %s;".format(table=self.table)
                with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                    cursor.execute(query,username)
                    connection.commit()
                return
            else:
                return False, "User not found"
        except Exception as e:
            return False, str(e)
        
    def get_auth_key(self, username):
        try:
            query = "SELECT authSecretKey  FROM {table} WHERE usersName = %s;".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,username)
                result = cursor.fetchone()
            if result:
                return result
            else:
                self.login_logger(username)
                return result
        except Exception as e:
            return False, str(e)
        
    def add_auth_key(self,secret_key,username):
        try:
            if self.get_email(username)[0]:
                query = "UPDATE {table} SET authSecretKey = %s WHERE usersName = %s;".format(table=self.table)
                with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                    cursor.execute(query,secret_key,username)
                    connection.commit()
                return True,username
            else:
                return False, "User not found"
        except Exception as e:
            return False, str(e)
        
    def update_auth_key(self, new_secret_key, username):
        try:
            if self.get_email(username):
                query = "UPDATE {table} SET authSecretKey = %s WHERE usersName = %s;".format(table=self.table)
                with self.connect_database() as connection, connection.cursor() as cursor:
                    cursor.execute(query,'',username)
                    connection.commit()
                return True, username
            else:
                return False, "User not found"
        except Exception as e:
            return False, str(e)

    def get_reset_token(self, username):
        try:
            query = "SELECT resetToken  FROM {table} WHERE usersName = %s;".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,username)
                result = cursor.fetchone()
            if result:
                return result
            else:
                self.login_logger(username)
                return result
        except Exception as e:
            return False, str(e)
    
    def match_reset_token(self, username, secret_key):
        try:
            query = "SELECT resetToken  FROM {table} WHERE usersName = %s;".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,username)
                result = cursor.fetchone()
            if result == secret_key:
                return True
            elif result != secret_key:
                return False
        except Exception as e:
            return False, str(e)
    
    def delete_reset_token(self, username):
        resetToken = ""
        try:
            query = "UPDATE {table} SET resetToken  = %s WHERE usersName = %s;".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,resetToken,username)
                connection.commit()
            return
        except Exception as e:
            return False,str(e)

        
    def generate_secure_uuid(self):
        random_string = secrets.token_hex(16)
        return str(uuid.UUID(random_string))

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(15))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break
        return password
    
    def login_logger(self,email):
        with open('acount_logs.txt','a') as f:
            f.write(f"{datetime.now()} : {email} doesn't exist in system.\n")
        return
    
    




