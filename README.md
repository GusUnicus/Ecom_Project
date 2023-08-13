# Secure Programming Project
***Secure Ecommerce***,  an ecommerce webapp that is built to withstand Command Injection, SQL Injection, Insecure Direct Object References and has a secure authentication. It also has minor protections against XSS, session hijacking and overflows.

Pre-requisites to run
- Python 3.11.1
- XAMPP

##### Database configuration
Download [XAMPP](https://www.apachefriends.org/download.html)

And start both the Apache and MySQL modules. Click the Admin next to MySQL to open your database.

Make sure your url says `route=/server/databases`, here click import and select the SQL file attached.

Make sure all values match: 
1. Character set: UTF-8
2. Skip this number of queries (for SQL) starting from the first one: 0
3. Enable foreign key checks: True
4. Format: SQL
5. SQL compatibility mode: NONE
6. Do not use AUTO_INCREMENT for zero values: True
Now press **Import**

Click the database from the side menu and go to `Privileges`, create a new user account 
Username: *Anything*
Host name: ***localhost***
Password: *Anything*

Uncheck `Grant all privileges on database DATABASE_NAME`

And under `Global privileges`, check 
- SELECT
- INSERT
- UPDATE

Then press Go.

##### Webapp configuration
Once you've downloaded and unzipped the file use `pip install -r requirements.txt`

Create a Keys folder in side the client directory, this is wehre you'll be storing your keys.

Your setup should look similar to this
<pre>
├───Client
│   ├───Keys
│   ├───models
│   ├───static
│   │   ├───css
│   │   ├───images
│   │   │   └───icons
│   │   ├───js
│   │   ├───temp
│   │   └───webfonts
│   ├───templates
│   │   └───components
</pre>

Run `openssl req -x509 -newkey rsa:4096 -keyout Keys/key.pem -out Keys/cert.pem -days 365` to generate SSL certificates

There will be several `os.environ['ENVIRONMENT_VARIABLE_NAME']` either replace these with your keys if you want run it locally or create the corresponding environment variables.

Then move to the directory where app.py is located and use `python app.py` to run the app. You'll be given an IP address that if you paste it in the browser you'll be able to interact with the website. The default IP address should be `127.0.0.1:5000`.



*The qr codes generated will be removed using cron jobs/background processes.*