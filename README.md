# SaltCast Prototype Website

## Authors: Nicholas Gammel, Vincent Pham, William Lamuth

### Special Thanks For Creating and Integrating Chatbot: Spencer Presley

## Build Instructions

### Step 1: pip install -r requirements.txt
While in the home directory, run the following command in the console to install the python libraries from the requirements.txt.

### Step 2: Create .env file
Create a .env file located accordingly:
static/env/.env

Fill with the following information:
DB_HOST
DB_USER
DB_PASS
DB_NAME

MAP_KEY

SECRET_KEY

EMAIL_KEY

CHATBOT_URL

OPENAI_API_KEY

Notes: 
DB_HOST - Database host
DB_USER - Database username
DB_PASS - Database password
DB_NAME - Database name
We used AWS Database to store our data, and MySQL Workbench to access our database.

MAP_KEY - Google maps API Key

SECRET_KEY - Key used for Hashing passwords, can be anything, as long it is secure and secret

EMAIL_KEY - Created Gmail to send and receive emails, this key is used for program to access Gmail account

CHATBOT_URL - Proxy server for chatbot requests (Ask Spencer Presley for more information)

OPENAI_API_KEY - API key for chatbot to function

### Step 3: py app.py
While in the home directory, run the following command to start the webpage locally.


## File Structure

### 1. Home Directory
In this home directory, you will find essential files such as app.py and requirements.txt. These files are fundamental to running the program. Follow the Build Instructions to set up and run the website.

### 2. Home/templates
This directory contains all accessible HTML files for the project. Each HTML file corresponds to a different page that is loaded in app.py based on user navigation. Files are named according to their purpose, and each includes comments at the top that explain its use in more detail.

### 3. Home/chatbot
This directory holds all files related to the AI chatbot. It may include chatbot logic, models, or any resources necessary for its functioning.

### 4. Home/static
The static directory stores all static files that remain unchanged during runtime. This includes:
- CSS files for styling
- JavaScript files for client-side functionality
- Python files for any required static scripts
- PHP files to create data files
- Data files (e.g., JSON files) for structured data access
- Images used across the site

## Current Functionalities

### 1. Map Functions
- Uses Google Maps API (API Key stored under static/env/.env)
- Supports Advanced Markers
- Supports Clustering
- Fully Functioning and Efficient Legend
- Working Search Feature
- Three Layer Popup for every point displaying information
- Radius around every point indicating actual location within a 2 mile radius

### 2. Chatbot
- Utilizes ChatGPT API (API Key stored under static/env/.env)
- Trained on Map data/Research Papers/Team Members/Additional Info
- Extendable window by dragging edges

### 3. Dashboard
- Supports pinning points in bottom left (When logged in)
- Does not support real data (Currently an outline)

### 4. Register
- Functional Register
- Email is used as Primary Key
- Organization is set to "NULL" by default
- User must select an account type
- Post registration email will be sent to verify email
    - Valid for 1 hour
    - Verifying email does not give any additional permissions, just changes on backend
    - Currently you are only able to verify email within an hour of registration

