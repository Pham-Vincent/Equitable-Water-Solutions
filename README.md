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