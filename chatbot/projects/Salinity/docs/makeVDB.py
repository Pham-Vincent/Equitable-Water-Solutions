import os
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Directory containing the text files
directory = 'unloaded'

# List to store all documents
all_documents = []

# Iterate through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        print(f"processing {filename}")
        file_path = os.path.join(directory, filename)
        loader = TextLoader(file_path)
        documents = loader.load()
        all_documents.extend(documents)

print(f"loaded {len(all_documents)} documents")
# Split the text into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(all_documents)
print(f"split into {len(texts)} texts")

# Create embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Create and save the FAISS index
db = FAISS.from_documents(texts, embeddings)
db.save_local("AllDocumentsVDB")
print(f"saved to AllDocumentsVDB")

print("Vector database created and saved successfully.")