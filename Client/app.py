import os, secrets
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash,Response
from firebase import Firebase
import stripe
from flask_bcrypt import Bcrypt
from user import User
from cart import Cart
from order import Order
import build_mail
from datetime import datetime, timedelta
import otp

import os, secrets
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash,Response
from firebase import Firebase
import stripe
from flask_bcrypt import Bcrypt
from user import User
from cart import Cart
from order import Order
import build_mail
from datetime import datetime, timedelta
import otp


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
bcrypt = Bcrypt(app)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
connect_firebase = Firebase()
products = connect_firebase.get_all_products()

USER = User()

STRIPE_KEYS = {
    'secret_key' : os.environ['STRIPE_SECRET_KEY'], 
    'public_key' : os.environ['STRIPE_PUBLISHABLE_KEY'], 
}

# pw_hash = bcrypt.generate_password_hash('hunter2')
#print(f"{pw_hash=}")

def set_default_session_values():
    items = connect_firebase.get_product_names()
    items = zip(list(items.keys()),list(items.values()),list(range(1,len(items)+1)))
    if 'logged_in' not in session:
        session['logged_in'] = False

def sanitize(*inputs):
    with open('genericpayload.txt','r') as f:
        data = f.read()
    for input in inputs:
        if input in data:
            return False
    return True
    

@app.after_request
def add_header(response):
    csp = {
        'default-src': "'self' data:",
        'img-src': "'self' data: *",
        'style-src': "'self' https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bulma@0.9.0/css/bulma.min.css",
        #'font-src': "'self' https://fonts.googleapis.com/css2", 
        'script-src': "'self' https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js", 
        # Add other CSP directives as needed
    }
    csp_header = '; '.join([f"{key} {value}" for key, value in csp.items()])
    csp ="img-src 'self' data: 'unsafe-inline' *"#https://collectionapi.metmuseum.org https://cdna.lystit.com https://designerdresshireaustralia.com.au https://www.dior.com https://www.prada.com;"
    response.headers['Content-Security-Policy'] = csp
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
   
    return response

@app.route('/',methods=['GET','POST'])
def main():
    set_default_session_values()
    if 'username' in session:
        username = session['username']
        return render_template('homepage.html', username=username, product_data=products)
    else:
        return render_template('homepage.html', product_data=products)

@app.route('/shop')
def shop():
    product_keys = list(products.keys())
    product_values = list(products.values())
    return render_template('shop.html',products=zip(product_keys,product_values))
    
@app.route('/shop-single')
def shop_single():
    product_key = request.args.get("product_key")
    product = connect_firebase.get_product(product_key)
    return render_template('shop-single.html', product=product)

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        input_data = request.form['input'].replace(" ","")
        no_results = True
        product_names = connect_firebase.get_product_names().items()
        result = []
        
        for id,name in product_names:
            if input_data.lower() in  name.lower():
                result.append(id)
        if len(result)<1:
            no_results = True
        else:
            no_results = False
        search_results = {}
        
        for id in result:
            search_results[id] = connect_firebase.get_product(id)
        #print(f"{search_results=}")
        
        search_results = zip(list(search_results.keys()),list(search_results.values()))
        return render_template('search.html',search_query=input_data,search_results=search_results,no_results=no_results)

    else:
        return 'Invalid Reqeust'


@app.route('/cart', methods=['POST'])
def receive_cart():
    cart_data = request.get_json()
    return jsonify(cart_data)

@app.route('/process_view/<product_key>')
def process_view(product_key):
    return redirect( url_for('shop_single',product_key=product_key ))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailID'].replace(" ","")
        password = request.form['passwordID'].replace(" ","")
        if sanitize(email,password): # checks if it is a generic attack if so returns False
            res,acc = USER.get_user(email)
            if res:
                if bcrypt.check_password_hash(acc[-2], password):
                    session['username'] = acc[1 ]
                    session['logged_in'] = True
                    return redirect(url_for('main'))
                else:
                    flash("Invalid credentials. Please try again.")
                    return render_template('login.html')
            flash("Account doesn't exist","error")
            return render_template('login.html')
        return render_template('login.html')
    elif request.method == 'GET':
        return render_template('login.html')
    else:
        return "Method not allowed"
    

@app.route('/shop')
def shop():
    product_keys = list(products.keys())
    product_values = list(products.values())
    return render_template('shop.html',products=zip(product_keys,product_values))
    
@app.route('/shop-single')
def shop_single():
    product_key = request.args.get("product_key")
    product = connect_firebase.get_product(product_key)
    return render_template('shop-single.html', product=product)

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        input_data = request.form['input'].replace(" ","")
        no_results = True
        product_names = connect_firebase.get_product_names().items()
        result = []
        
        for id,name in product_names:
            if input_data.lower() in  name.lower():
                result.append(id)
        if len(result)<1:
            no_results = True
        else:
            no_results = False
        search_results = {}
        
        for id in result:
            search_results[id] = connect_firebase.get_product(id)
        #print(f"{search_results=}")
        
        search_results = zip(list(search_results.keys()),list(search_results.values()))
        return render_template('search.html',search_query=input_data,search_results=search_results,no_results=no_results)

    else:
        return 'Invalid Reqeust'


@app.route('/cart', methods=['POST'])
def receive_cart():
    cart_data = request.get_json()
    return jsonify(cart_data)

@app.route('/process_view/<product_key>')
def process_view(product_key):
    return redirect( url_for('shop_single',product_key=product_key ))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailID'].replace(" ","")
        password = request.form['passwordID'].replace(" ","")
        sanitize(email,password) # checks if it is a generic attack if so returns False
        res,acc = USER.get_user(email)
        #print(res[0])
        #print(res[-2],res)
        if res:
            if bcrypt.check_password_hash(acc[-2], password):
                session['username'] = acc[1 ]
                session['logged_in'] = True
                return redirect(url_for('main'))
            else:
                flash("Invalid credentials. Please try again.")
                return render_template('login.html')
        flash("Account doesn't exist","error")
        return render_template('login.html')
    elif request.method == 'GET':
        return render_template('login.html')
    else:
        return "Method not allowed"
    

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('Logged out successfully', 'success')
    return redirect(url_for('main'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        f_name = request.form['fName'].replace(" ","")
        l_name = request.form['lName'].replace(" ","")
        username = request.form['usernameID'].replace(" ","")
        email = request.form['emailID'].replace(" ","")
        pwd = request.form['passwordID'].replace(" ","")
        sanitize(f_name, l_name, username, email, pwd) # checks if it is a generic attack if so returns False
        account = USER.create_user(first_name=f_name,
                                 last_name= l_name,
                                 username= username,
                                 email= email,
                                 password=bcrypt.generate_password_hash(pwd).decode('utf-8'))
        # flash
        #print(f"{account=}")
        # user = User(email)
        if account[0]:
            flash(f"Account Created. Hello {account[1][2]}")
            print(f"{account[1][2]=}")
        # unique_url = password_reset_url(user)
        # if account_status[0]:
        #     # session['username'] = username
        #     return redirect(url_for('login'))
        # password = db.generate_password()
        # mail_body = f'''
        #             You randomly generated password {account[-2]}.

        #             Click this to reset password: {unique_url}
        #             '''
        #print('Request:')
        #print(f"{request.environ['wsgi.url_scheme']=}")
        #print(f"{request.url_root=}")
        #print(f"{request.endpoint=}")
        #print(f"{f_name=} {l_name=} {username=} {email=}")
        
        # build_mail.send_email(email,'Password reset',mail_body)
        # user = User('a','a')
        # send_password_reset_email(user)
            return redirect(url_for('login'))
        else:
            flash(f"Account not ceated. Try again.")
            return redirect(url_for('register'))
        
    return render_template('signup.html')

@app.route('/test')
def test():
    try:
        un = 'Test'
        generate_qr(un)
    #print(qrimg)
        return render_template('qr.html',username=un,image_path=f"temp/qr_{un}.png")
    except Exception as e:
        print("Error",str(e))
        return str(e)
    
user = {}
@app.route('/qr/<username>')
def generate_qr(username):
    print(f"generate qr : {username=}")
    secret_key = USER.generate_password()
    print(f"generate qr : {secret_key=}")
    res = USER.add_auth_key(secret_key=secret_key,username=username)
    print(f"generate qr : {res=}")
    if not res[0]:
        print(f"generate qr : {otp.base64.b32encode(secret_key.encode()).decode()=}")
        user['sk']=otp.base64.b32encode(secret_key.encode()).decode()
        with open('update_later.txt','a') as f:
            f.write(f"{username} {otp.base64.b32encode(secret_key.encode()).decode()}\n")
    print(f"generate qr : Exit if")
    otp.get_qr(username=username,secret_key=secret_key)
    print(f"generate qr : completed")
    return 

@app.route('/verify_mfa',methods=['GET','POST'])
def verify_mfa():
    print(f"verify_mfa : started")
    try:
        print(f"verify_mfa : entered try block")
        verification_code = request.form['verification_code'].replace(" ","")
        username = request.form['username'].replace(" ","")
        print(f"verify_mfa : {verification_code=}") #working
        _usk = USER.get_auth_key(username)
        id_valid = otp.verify(secret_key=_usk,verification_code=verification_code)
        print(f"verify_mfa : {id_valid=}")
        if id_valid:
            flash("Code Matched")
            os.remove(f'static/temp/qr_{username}.png')
            return redirect(url_for('login'))
        else:
            flash('Invalid code! Try again.')
            return redirect(url_for('verify_mfa'))
    except Exception as e:
        flash("MFA verification code is missing or invalid. Please signup to MFA later.")
        return redirect(url_for('login'))

def password_reset_url(user):
        user.reset_token(secrets.token_urlsafe(32))
        user.token_expiry(datetime.utcnow() + timedelta(hours=1))  # Set expiry to 1 hour
        reset_link = f"{request.url_root}reset_password?token={user.reset_token}"
        print(reset_link)
        return reset_link

@app.route('/reset/<token>', methods=['GET','POST'])
def reset_password(token):
    if request.method == 'POST':
        username = request.form['username'].replace(" ","")

        # Generate a reset token
        reset_token = secrets.token_urlsafe(32)

        # Update the user's reset token in the database
        # db_cursor.execute('UPDATE users SET reset_token = ? WHERE username = ?', (reset_token, username))
        # db_conn.commit()

        # Send reset instructions (e.g., via email)
        flash('Password reset link sent to your email', 'info')
        return redirect(url_for('login'))

    return redirect(url_for('login'))


@app.route('/pay',methods=['GET','POST'])
def pay():
    return render_template('components/checkout.html')

@app.route('/config')
def get_public_key():
    stripe_config = {"publicKey": STRIPE_KEYS['public_key']}
    return jsonify(stripe_config)

@app.route('/create_checkout_session')
def checkout():
    domain_url = request.url_root
    stripe.api_key = STRIPE_KEYS['secret_key']

    try:
        product = stripe.Product.create(
        name='T-shirt',
        description='Comfortable cotton t-shirt',
        images=['https://example.com/t-shirt.png'],
        )

        price = stripe.Price.create(
        product=product.id,
        unit_amount=2000,
        currency='aud',
        )
        checkout_session = stripe.checkout.Session.create(
            success_url = domain_url+"success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = domain_url+"cancelled",
            payment_method_types = ['card'],
            mode = "payment",
            line_items = [
                {
                    # "name":"Item1",
                    "quantity":1,
                    # "currency":"aud",
                    # "amount":2000,
                    "price":price.id,
                }
            ]
        )
        return jsonify({"sessionId":checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)),403

if __name__ == '__main__':
    app.run(debug=True)