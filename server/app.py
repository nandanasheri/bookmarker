from flask import Flask,  request, jsonify
from pinecone import Pinecone
import os
from dotenv import load_dotenv
import uuid
from utils import HTMLtoText
from datetime import datetime, timezone
import time
from supabase import create_client, Client

app = Flask(__name__)

# Create a dense index with integrated embedding
def create_dense_index():
    index_name = "dense-bookmarks"
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model":"llama-text-embed-v2",
                "field_map": {"text": "chunk_text"}
            }
        )

'''
 * @route POST /bookmark
 * @desc Add a bookmark to the Pinecone DB

 * @inputExample  -- POST http://localhost:5000/add
  req body : {}

'''
@app.route("/add", methods=["POST"])
def add_bookmark():
    content_type = request.headers.get('Content-Type')
    created_at = datetime.now(timezone.utc).isoformat()

    if content_type == "application/json":
        req_body = request.get_json()
        result = HTMLtoText(req_body)
        dense_index = pc.Index("dense-bookmarks")
        records = []
        i = 0
        document_id = str(uuid.uuid4())

        for each in result:
            print(each)
            each_chunk = {}
            each_chunk["_id"] = f"{document_id}#chunk{i}"
            each_chunk["chunk_text"] = each
            each_chunk["title"] = req_body["title"]
            each_chunk["url"] = req_body["url"]
            each_chunk["tags"] = []
            each_chunk["created_at"] = created_at
            i += 1
            records.append(each_chunk)
        
        # Batch requests to send to pinecone only 20 at a time - avoid rate limits
        BATCH_SIZE = 20
        for start in range(0, len(records), BATCH_SIZE):
            batch = records[start:start+BATCH_SIZE]
            dense_index.upsert_records("bookmarks-namespace", batch)
            time.sleep(5)

        response = (
            supabase.table("bookmarks")
            .insert({"url": req_body["url"], "title": req_body["title"], "notes": req_body["notes"], "created_at": created_at})
            .execute()
        )

        return jsonify({"document_id": document_id, "url": req_body['url']}), 200
    
    else:
        return jsonify({}), 400


''' 
    * @route GET /search 
    * @desc Semantic Search to Pinecone DB
    * @inputExample  -- GET http://localhost:5000/search?q=jobs websites of SWE&t=portfolios, SWE
    * @outputExample  -- {}
  '''
@app.route("/search", methods=["GET"])
def search_bookmarks():
    query = request.args.get("q")
    tags = request.args.get("t")

    dense_index = pc.Index("dense-bookmarks")

    query = {
        "top_k": 10,
        "inputs": {'text': query},
    }

    # check if any tags to filter exist
    if tags is not None:
        query["filter"] = {"tags": {"$in": tags}}
    
    # Search the dense index
    results = dense_index.search(
        namespace="bookmarks-namespace",
        query=query,
        rerank={
        "model": "bge-reranker-v2-m3",
        "top_n": 10,         # rerank and return only the most relevant documents
        "rank_fields": ["chunk_text"]
        }
    )
    # using to_dict() because Pinecone result isn't JSON serializable because it's a QueryResponse Object
    return results.to_dict()
    
@app.route("/")
def main():
    return "Root Endpoint"


# create a pinceone client to interact with vector db
load_dotenv()
pinecone_api = os.getenv("PINECONE_API_KEY")

# Pinecone client initialization
pc = Pinecone(api_key=pinecone_api)
create_dense_index()

# Supabase client initialization
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)