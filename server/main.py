from flask import Flask
from pinecone import Pinecone
import os
app = Flask(__name__)
from dotenv import load_dotenv

# create a pinceone client to interact with vector db
load_dotenv()
pinecone_api = os.getenv("PINECONE_API_KEY")
# Pinecone client initialization
pc = Pinecone(api_key=pinecone_api)

# Create a dense index with integrated embedding
def create_dense_index():
    index_name = "dense_bookmarks"
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model":"llama-text-embed-v2",
                "field_map":{"text": "chunk_text"}
            }
        )


@app.route("/")
def hello_world():
    return "Hello, World!"