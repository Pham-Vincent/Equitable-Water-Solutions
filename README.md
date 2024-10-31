# SaltCast Prototype Website

## Authors: Nicholas Gammel, Vincent Pham, William Lamuth

## Build Instructions

### Step 1: pip install -r requirements.txt
While in the home directory, run the following command in the console to install the python libraries from the requirements.txt.

### Step 2: Create index.pkl
cd chatbot/projects/docs
Create a directory inside of the docs directory named 'unloaded' and add any number of txt files to train the chatbot. 
Run the command: py makeVDB.py
This should created an index.pkl and an index.faiss inside of the AllDocumentsVDB directory.

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