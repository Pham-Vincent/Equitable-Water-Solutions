""" 
Title:About.py
Author: Nicholas Gammel

Functionality: This file is designed to control functionality of Login/Register.

Output: Session Variables for login
Date:7/23/2024
"""
from flask import Flask,render_template,request, redirect, url_for, session
from Database import *
from Graph import *
from login import *
from FeatureExtraction import *
import hashlib, re


#Controls register page functionality including validating using input and storing data inside of database
def registerFunction():
    #Checks that fields are filled
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'org' in request.form and 'password' in request.form and 'password-again' in request.form and 'email' in request.form and 'tags' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
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
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
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
            cursor.close()
            conn.close()
            # Redirect to map page
            return redirect(url_for('index'))
    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    msg=''
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