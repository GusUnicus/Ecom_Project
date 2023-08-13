import os, secrets, re, stripe, ssl
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash,Response,json
from firebase import Firebase
from flask_bcrypt import Bcrypt
from user import User
from order import Order
import build_mail, otp
from datetime import datetime, timedelta


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
ORDER = Order()

STRIPE_KEYS = {
    'secret_key' : os.environ['STRIPE_SECRET_KEY'], 
    'public_key' : os.environ['STRIPE_PUBLISHABLE_KEY']  
}

# Can be changed to a file with all the top passwords and save it to the same variable
TOP_20_PASSWORDS = ['guest', '123456', 'password', '12345', 'a1b2c3', '123456789', 'Password1', '1234', 'abc123', '12345678', 'qwerty', 'baseball', 'football', 'unknown', 'soccer', 'jordan23', 'iloveyou', 'monkey', 'shadow', 'g_czechout']

def set_default_session_values():
    items = connect_firebase.get_product_names()
    items = zip(list(items.keys()),list(items.values()),list(range(1,len(items)+1)))
    if 'logged_in' not in session:
        session['logged_in'] = False

def sanitize(*inputs):
    with open('genericpayload.txt','r') as f:
        data = f.read()
    result=[]
    for input in inputs:
        result.extend([element for element in data if re.search(input, element)])
    if len(result)>0:
        return False
    return True

def check_password_strength(password):
    if len(password) < 11:
        return "weak"
    if not re.search(r'[A-Z]', password):
        return "weak"
    if not re.search(r'[a-z]', password):
        return "weak"
    if not re.search(r'\d', password):
        return "weak"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "weak"
    if password in TOP_20_PASSWORDS:
        return "weak"
    return "strong"
    
def password_reset_url(email):
        reset_token = secrets.token_urlsafe(32)
        expiry_time = datetime.now() + timedelta(hours=4)# Set expiry to 4 hours from now
        expiry_time = expiry_time.timestamp()
        USER.update_reset_token(reset_token=reset_token,expiry=expiry_time,email=email)
        reset_link = request.url_root+'/reset_password/token='+reset_token+f'?email={email}'
        return reset_link


@app.after_request
def add_header(response):
    csp ="img-src 'self' data: 'unsafe-inline' *"
    response.headers['Content-Security-Policy'] = csp
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers['Access-Control-Allow-Origin'] = 'https://checkout.stripe.com/*'
    response.headers['Strict-Transport-Security'] = 'max-age=7200; includeSubDomains'
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
        search_results = zip(list(search_results.keys()),list(search_results.values()))
        return render_template('search.html',search_query=input_data,search_results=search_results,no_results=no_results)

    else:
        return 'Invalid Reqeust'


@app.route('/cart', methods=['POST'])
def receive_cart():
    cart_data = request.get_json()
    session['cart'] = cart_data
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} #redirect(url_for('create_checkout_session',cart=json.dumps(cart_data)))

@app.route('/process_view/<product_key>')
def process_view(product_key):
    return redirect( url_for('shop_single',product_key=product_key ))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailID'].replace(" ","")
        password = request.form['passwordID'].replace(" ","")
        if sanitize(email,password): # checks if it is a generic attack if so returns False
            a = USER.get_user(email)
            res,acc = a
            if res:
                if bcrypt.check_password_hash(acc[5], password):
                    session['userID'] = acc[0]
                    session['username'] = acc[1]
                    session['userEmail'] = acc[4]
                    session['logged_in'] = True
                    return redirect(url_for('generate_qr',username=session['username']))
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
    
    
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()
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
        if sanitize(f_name, l_name, username, email, pwd) and check_password_strength(password=pwd)=="strong": # checks if it is a generic attack if so returns False
            account = USER.create_user(first_name=f_name,
                                        last_name= l_name,
                                        username= username,
                                        email= email,
                                        password=bcrypt.generate_password_hash(pwd).decode('utf-8'))
    
            if account:
                secret_key = USER.generate_password()
                secret_key = otp.base64.b32encode(secret_key.encode()).decode()
                USER.update_auth_key(secret_key=secret_key,username= username)
                flash(f"Account Created.")
                return redirect(url_for('login'))
            else:
                flash(f"Account not ceated. Try again.")
                return redirect(url_for('register'))
        flash(f"Weak Password. Try again.")
        return redirect(url_for('register'))
    return render_template('signup.html')


@app.route('/qr/<username>')
def generate_qr(username):
    try:
        otp.get_qr(username=username,secret_key=USER.get_auth_key(username=username))
        return render_template('qr.html',username=username,image_path=f"temp/qr_{username}.png")
    except:
        flash("Unexpected Error! Please try again later.")
        return redirect(url_for('main'))


@app.route('/verify_mfa',methods=['GET','POST'])
def verify_mfa():
    try:
        verification_code = request.form['verification_code'].replace(" ","")
        username = request.form['username'].replace(" ","")
        _usk = USER.get_auth_key(username)
        id_valid = otp.verify(secret_key=_usk,verification_code=verification_code)
        if id_valid:
            flash(f"Welcome back {username}")
            return redirect(url_for('main'))
        else:
            flash('Invalid code! Try again.')
            return redirect(url_for('verify_mfa'))
    except Exception as e:
        flash("MFA verification code is missing or invalid. Please signup to MFA later.")
        return redirect(url_for('main'))

@app.route('/forgot_password',methods=['GET','POST'])
def password_reset():
    if request.method == 'POST':
        userEmail = request.form['emailID']
        _flag,_UNAME = USER.get_userName(email=userEmail)
        if _flag:
            reset_link = password_reset_url(userEmail)
            body = f'''
            Hello {_UNAME[0]},

            We received a request to reset your password. If you did not make this request, you can ignore this email.
            
            If the link above doesn't work, you can copy and paste the following URL into your browser:
            {reset_link}

            This link is valid for the next 4 hours. After that, you'll need to request another reset.
            
            Thank you!
            Secured eCommerce
                    '''
            build_mail.send_email(recipient_email=userEmail,subject='Secured eCommerce: Password Reset',body=body)
            flash('Password reset link sent to your email', 'info')
            return redirect(url_for('login'))
        else:
            flash('User not found!', 'info')
            return redirect(url_for('register'))
    else:
        return render_template('passwordchange.html')

@app.route('/reset_password/token=<token>', methods=['GET'])
def reset_password(token):
    if request.method == 'GET':
        email = request.args.get('email')
        return render_template('passwordreset.html',email=email)
    else:
        return "Invalid Request"
    
@app.route('/reset',methods=['POST'])
def reset():
    if request.method == 'POST':
        NewPassword = request.form['password'].replace(" ","")
        email = request.form['email'].replace(" ","")
        print(f"{NewPassword=} {email=}")
        _token,_exp = USER.get_reset_token(email=email)
        if float(_exp)>datetime.now().timestamp():
            NewPassword = bcrypt.generate_password_hash(NewPassword).decode('utf-8')
            USER.update_password(email=email,password=NewPassword)
            flash("Password Updated!")
        return redirect(url_for('login'))
    else:
        return "Invalid Request"

@app.route('/pay',methods=['GET','POST'])
def pay():
    return render_template('components/checkout.html')

@app.route('/config')
def get_public_key():
    stripe_config = {"publicKey": STRIPE_KEYS['public_key']}
    return jsonify(stripe_config)



@app.route('/create_checkout_session',methods=['GET','POST'])
def create_checkout_session():
    domain_url = request.url_root
    stripe.api_key = STRIPE_KEYS['secret_key']
    try:
        cart = session['cart']
        products = [stripe.Product.create(name=item['name']) for item in cart]
        prices = []
        for item,product in zip(cart,products):
            prices.append(stripe.Price.create(
                            product=product.id,
                            unit_amount=int(item['price'])*100,
                            currency='aud',
                            ))
   
        line_items = []
        for item,price in zip(cart,prices):
            line_items.append({"quantity":item['count'],"price":price.id})
        
        checkout_session = stripe.checkout.Session.create(
            success_url = domain_url+"success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = domain_url+"cancelled",
            payment_method_types = ['card'],
            mode = "payment",
            line_items =line_items ,
        )
        session_data = {
        'sessionId': checkout_session.id,
        }

        return jsonify(session_data)  
    except Exception as e:
        print(" Stripe Error",e)
        return jsonify(error=str(e)),403


@app.route("/success")
def success():
    ORDER.write_order(userID=session['userID'],cart_products=session['cart'])
    return render_template("components/success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("components/cancelled.html")

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile='Keys/cert.pem', keyfile='Keys/key.pem')
    app.run(host='localhost', port=5000, ssl_context=context)