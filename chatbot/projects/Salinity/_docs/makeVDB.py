from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Load the document
loader = TextLoader('unloaded/Team_List.txt')
documents = loader.load()

# Split the text into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Create and save the FAISS index
db = FAISS.from_documents(texts, embeddings)
db.save_local("TeamListVDB")

print("Vector database created and saved successfully.")