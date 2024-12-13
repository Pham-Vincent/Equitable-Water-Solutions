""" 
Title:About.py
Author: Nicholas Gammel

Functionality: This file is designed to control functionality of Login/Register.

Output: Session Variables for login
Date:7/23/2024
"""
from pathlib import Path
import os
from flask import (
    Flask, 
    render_template,
    request, 
    redirect, 
    url_for, 
    session, 
    flash
)
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from dotenv import load_dotenv
import hashlib, re
import smtplib
from email.mime.text import MIMEText

from chatbot.scripts import find_project_root, find_env_file
from .Database import DatabaseConn

SERVER = False

# Change File path depending on Device - SERVER PATH
if SERVER:
    load_dotenv('/home/bitnami/htdocs/static/env/.env')
else:
    # Find and load the .env file dynamically
    load_dotenv(find_env_file(find_project_root(Path(__file__))))

# Initialize the token serializer
serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

def verify_email(token):
    try:
        # Decode the token
        email = serializer.loads(token, salt='email-verify', max_age=3600)  # token valid for 1 hour
    except SignatureExpired:
        flash('The verification link has expired. Please register again.', 'danger')
        return redirect(url_for('register'))

    # Mark the email as verified in the database
    conn = DatabaseConn()
    cursor = conn.cursor()
    query = "UPDATE Accounts SET confirmed = 1 WHERE email = %s"
    cursor.execute(query, (email,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Your email has been verified. You can now log in.', 'success')
    return redirect(url_for('login'))


def send_verification_email(user_email, fname, lname):
    # Generate the verification token
    token = serializer.dumps(user_email, salt='email-verify')

    # Generate verification link
    verification_link = url_for('emailVer', token=token, _external=True)
    verification_link = verification_link.replace('http://localhost:5000', 'https://saltcast.io')
    
    # Prepare email content
    message = f"Hello {fname} {lname},\n\nPlease verify your email by clicking the link below:\n{verification_link}\n\nThank you!"
    msg = MIMEText(message)
    
    # Set email subject and recipients
    msg['Subject'] = "Please Verify Your Email"
    msg['From'] = "waterequitable@gmail.com"
    msg['To'] = user_email

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login("waterequitable@gmail.com", os.getenv('EMAIL_KEY'))
        smtp_server.sendmail("waterequitable@gmail.com", [user_email], msg.as_string())



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
            send_verification_email(email, fname, lname)
            flash('A verification email has been sent. Please check your inbox to verify your email.', 'info')
            
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