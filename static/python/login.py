""" 
Title:About.py
Author: Nicholas Gammel

Functionality: This file is designed to control functionality of Login/Register.

Output: Session Variables for login
Date:7/23/2024
"""
from flask import Flask,render_template,request, redirect, url_for, session, flash
from itsdangerous import URLSafeTimedSerializer
from Database import *
from Graph import *
from login import *
from FeatureExtraction import *
import hashlib, re
import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer


#Controls register page functionality including validating using input and storing data inside of database
def registerFunction():
    msg=''
    #Checks that fields are filled
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'password' in request.form and 'password-again' in request.form and 'email' in request.form and 'tags' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        if 'organization' not in request.form:
            organization = "NULL"
        else:
            organization = request.form['org']
        password = request.form['password']
        password_check = request.form['password-again']
        email = request.form['email']
        tags = request.form['tags']
        #Creates database connection and executes query
        #Stores single sequence result in account
        conn = DatabaseConn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Accounts where email = %s"
        cursor.execute(query, (email,))
        account = cursor.fetchone()
        #Validates if the account exists and follows correct naming conventions
        if account:
            msg = 'Account already exists!'
        elif password != password_check:
            msg = 'Password does not match!'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', fname):
            msg = 'First name must contain only characters!'
        elif not re.match(r'[A-Za-z]+', lname):
            msg = 'Last name must contain only characters!'
        elif not fname or not lname or not organization or not password_check or not password or not email:
            msg = 'Please fill out the form!'
        else:
            #CREATES NEW ACCOUNT
            # Hash the password
            hash = password + os.getenv('SECRET_KEY')
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Insert into Database
            query = "INSERT INTO Accounts (fname, lname, password, email, organization, tags) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (fname, lname, password, email, organization, tags))
            conn.commit()
            query = "SELECT * FROM Accounts where email = %s AND password = %s"
            cursor.execute(query, (email, password,))
            account = cursor.fetchone()
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['fname']
            session['lastname'] = account['lname']
            flash('A verification email has been sent to your email address. Please verify to complete registration.', 'info')
            
        # Line To Add Blank Data into the Marker Pinning 
        #<--------------------->
            query = "INSERT INTO Water_Data.Location_Pinned (id,PinnedLocation1,PinnedLocation2,PinnedLocation3) VALUES (%s,NULL,NULL,NULL)"
            cursor.execute(query, (session['id'],))
            conn.commit()

            cursor.close()
            conn.close()

            # Redirect to map page
            return redirect(url_for('index'))
    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    flash(msg, 'danger')
    return render_template('register.html', msg=msg)

#Uses login submission to check database for matching information
def loginFunction():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #Hashes input password
        hash = password + os.getenv('SECRET_KEY')
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        #Creates database connection
        #Executes query to see if there is account with matching username and hashed password
        conn = DatabaseConn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Accounts where email = %s AND password = %s"
        cursor.execute(query, (email, password,))
        account = cursor.fetchone()
        # If account exists in database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['fname']
            session['lastname'] = account['lname']
            cursor.close()
            conn.close()
            # Redirect to map page
            referrer = request.referrer
            return redirect(referrer or url_for('index'))
        else:
            cursor.close()
            conn.close()
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    msg=''
    return render_template('index.html', msg=msg)


#Used to check session variables on each page to validate user is logged in
def checkLogin(html):
    if 'loggedin' in session:
        conn = DatabaseConn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Accounts where id = %s"
        cursor.execute(query, (session['id'],))
        account = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template(html, account=account)

'''
def send_verification_email(user_email):
    token = generate_verification_token(user_email)
    verification_url = url_for('verify_email', token=token, _external=True)
    body = f'Please verify your email by clicking this link: {verification_url}'

    # Set up MIMEText for the email
    msg = MIMEText(body, 'plain')
    msg['Subject'] = 'Email Verification'
    msg['From'] = app.config['MAIL_USERNAME']
    msg['To'] = user_email

    # Send email
    with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.sendmail(app.config['MAIL_USERNAME'], user_email, msg.as_string())
'''