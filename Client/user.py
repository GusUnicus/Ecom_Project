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
                query = "INSERT INTO {table}(`usersUid`, `usersName`, `first_name`, `last_name`, `usersEmail`, `usersPwd`) VALUES ((%s), (%s), (%s), (%s), (%s), (%s));".format(table=self.table)
                with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                    cursor.execute(query,(data['usersUid'],data['usersName'],data['first_name'],data['last_name'],data['usersEmail'],data['usersPwd']))
                    connection.commit() 
                return True
            except Exception as e:
                return False,"Error creating user: " + str(e)
    
    def get_user(self,email):
        try:
            query = "SELECT * FROM {table} WHERE (`usersEmail`) = ((%s));".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(email,))
                result = cursor.fetchone()
            if result:
                return True,result
            else:
                self.login_logger(email)
                return False,result
        except Exception as e:
            return "Error logging in: " + str(e)
    
    def get_userName(self,email):
        try:
            query = "SELECT usersName FROM {table} WHERE (`usersEmail`) = ((%s));".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(email,))
                result = cursor.fetchone()
            if result:
                return True,result
            else:
                self.login_logger(email)
                return False,result
        except Exception as e:
            return "Error logging in: " + str(e)   
    
    def get_userID(self,email):
        try:
            query = "SELECT usersUid  FROM {table} WHERE (`usersEmail`) = ((%s));".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(email,))
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
            query = "SELECT usersEmail FROM {table} WHERE usersName = ((%s));".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(username,))
                result = cursor.fetchone()
            if result:
                return True,result
            else:
                self.login_logger(username)
                return False,result
        except Exception as e:
            return False,str(e)
        
    def update_password(self, email, password):
        try:
            query = "UPDATE {table} SET usersPwd = (%s) WHERE usersEmail = (%s);".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(password,email))
                connection.commit()
            self.update_reset_token(reset_token=None,email=email,expiry=None)
            return
        except Exception as e:
            return False, str(e)
        
    def get_auth_key(self, username):
        try:
            query = "SELECT authSecretKey  FROM {table} WHERE usersName = (%s);".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(username,))
                result = cursor.fetchone()
            if result:
                return result[0]
            else:
                self.login_logger(username)
                return result
        except Exception as e:
            return False, str(e)
        
        
    def update_auth_key(self, secret_key, username):
        try:
            query = "UPDATE {table} SET authSecretKey = (%s) WHERE usersName = (%s);".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(secret_key,username))
                connection.commit()
            return True,self.get_auth_key(username)
            
        except Exception as e:
            return False, str(e)

    def get_reset_token(self, email):
        try:
            query = "SELECT resetToken,token_expiry  FROM {table} WHERE usersEmail = (%s);".format(table=self.table)
            with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                cursor.execute(query,(email,))
                result = cursor.fetchone()
            if result:
                return result
            else:
                self.login_logger(email)
                return result
        except Exception as e:
            return False, str(e)
        
    def update_reset_token(self, reset_token, email, expiry):
        try:
            if self.get_email(email):
                query = "UPDATE {table} SET resetToken  = (%s), token_expiry =(%s) WHERE usersEmail  = (%s);".format(table=self.table)
                with self.connect_database(self.database) as connection, connection.cursor() as cursor:
                    cursor.execute(query,(reset_token,expiry,email))
                    connection.commit()
                return True, email
            else:
                return False, "User not found"
        except Exception as e:
            return False, str(e)
        
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
    
    




