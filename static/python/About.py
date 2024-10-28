""" 
Title:About.py
Author: Nicholas Gammel

Functionality: This file is designed to control functionality of the About Us page.

Output: About Us Page & Contact Us Email
Date:7/23/2024
"""
from flask import Flask,render_template,request, session
from Database import *
from login import *
from About import *
from FeatureExtraction import *
import os
import re
import smtplib
from email.mime.text import MIMEText

# Controls loading the about us page and checks requests for the contact us part of the page
def aboutusFunction():
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'email' in request.form:
        firstname = request.form['fname']
        lastname = request.form['lname']
        #Add Email Input Check
        email = request.form['email']
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
           return render_template('aboutUs.html')
        
        message = request.form['message']
        contactusFunction(firstname, lastname, email, message)
        #return success message - For Now Reloads page
    if 'loggedin' in session:
        conn = DatabaseConn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Accounts where id = %s"
        cursor.execute(query, (session['id'],))
        account = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('aboutUs.html', account=account)
    return render_template('aboutUs.html')


#Function to send email to company email with information given from the contact us section of the about us page
def contactusFunction(fname, lname, email, message):
    #Email Sent from sender
    sender = "waterequitable@gmail.com"

    #Email Received by receiver - NO RECEIVER ATM
    #Change Receivers
    receivers = ["waterequitable@gmail.com",]
    #Change Receivers

    msg = MIMEText(message)
    #Sets up subject line of email
    msg['Subject'] = email + ' , ' + fname + ' , ' + lname
    #Sets up sender
    msg['From'] = sender
    #Sets up Receiver
    msg['To'] = ', '.join(receivers)
    #Connects to Sender email via smtp library and sends email to receiver
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        #
        smtp_server.login(sender, os.getenv('EMAIL_KEY'))
        smtp_server.sendmail(sender, receivers, msg.as_string())
