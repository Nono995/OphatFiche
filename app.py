from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = '19a1b30827aa432b92328dc4f2187420'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            #hash = password + app.secret_key
            #hash = hashlib.sha1(hash.encode())
            #password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for logged in users
@app.route('/login/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/login/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))

@app.route('/login/savepatient', methods = ['POST', 'GET'])
def patient():
    msg=''
    if request.method == 'POST':
        cfiche = request.form['codeFiche']
        nom = request.form['Nom']
        prenom = request.form['Prenom']
        telephone = request.form['Tel']
        email = request.form['Email']
        dateNaiss = request.form['DteNaiss']
        sexe = request.form.getlist(['Sexe'])
        profession = request.form['Profession']

        GFamilial = request.form.getlist('GlauFamilial[]')
        siGFamilial = request.form.getlist('SIGlauFamilial[]')
        ceciFamilial = request.form.getlist('CecitFamilial[]')
        antecedent = request.form.getlist('Antecedent[]')

        medSystem = request.form['MedSytem']
        actdOpht = request.form['ActdOpht']

        acuiteV = request.form['AcuiteVisuel']
        motilite = request.form.getlist('Motilite[]')
        biomiscropie = request.form['Biomiscropie']
        tonovaleur = request.form['TonoValeur']
        tonoHmesure = request.form['TonoHMesure']
        tonoTytono = request.form['TonoTypeTono']
        tonopressionibl = request.form['TonoPressionCible']

        gionioscopieD = request.form.getlist('GionoD[]')
        gionioscopieG = request.form.getlist('GionoG[]')

        vertCupDiscD = request.form['VertCupDiscD']
        vertCupDiscG = request.form['VertCupDiscG']
        anrD = request.form['ANRD']
        anrG = request.form['ANRG']
        polePostD = request.form['PolePostD']
        polePostG = request.form['PolePostG']

        atroperiD = request.form('AtroPeriD[]')
        atroperiG = request.form('AtroPeriG[]')

        hemoragieD = request.form('HemoragieD[]')
        hemoagieG = request.form('HemoragieG[]')

        perimdD = request.form['PeriMdD']
        perimdG = request.form['PeriMdG']

        peripsdD = request.form['PeriPsdD']
        peripsdG = request.form['PeriPsdG']

        periIndexD = request.form['PeriIndexD']
        periIndexG = request.form['PeriIndexG']

        octRnflD = request.form['OCTRNFLD']
        octRnflG = request.form['OCTRNFLG']

        octVertcdD = request.form['OctVcdD']
        octVertcdG = request.form['OctVcdG']

        octCupvolumeD = request.form['OctCupD']
        octCupvolumeG = request.form['OctCupG']

        macularD = request.form['MacularD']
        macularG = request.form['MacularG']

        macularthD = request.form['MacularthD']
        macularthG = request.form['MacularthG']

        classifiMillsD = request.form['ClassifMillsD']
        classifiMillsG = request.form['ClassifMillsG']
        diagnosticD = request.form['DiagnosticD']
        diagnosticG = request.form['DiagnosticG']

        diagnosticGlaucomaD = request.form('niveau[]')



    return render_template('profile.html', msg=msg)

if __name__ == '__main__':
    app.run()
