from flask import Flask, Response, render_template, jsonify, request
import re
import json
import os
from datetime import datetime
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
NVIDIA_API_KEY=os.environ.get('NVIDIA_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["NVIDIA_API_KEY"] = NVIDIA_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "adibot" 
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)


retriever = docsearch.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 4, "score_threshold": 0.5})

chatModel = ChatNVIDIA(model="meta/llama-3.1-8b-instruct", temperature=0.7, max_tokens=400)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Chat history storage
CHATS_DIR = 'chats_history'
QUERIES_LOG_FILE = 'queries_log.json'
QUERIES_DIR = 'user_queries'

if not os.path.exists(CHATS_DIR):
    os.makedirs(CHATS_DIR)
if not os.path.exists(QUERIES_DIR):
    os.makedirs(QUERIES_DIR)

def log_query(chat_id, user_query, bot_response):
    """Log user query with full metadata"""
    timestamp = datetime.now()
    query_data = {
        'timestamp': timestamp.isoformat(),
        'chat_id': chat_id,
        'user_query': user_query,
        'bot_response': bot_response,
        'query_length': len(user_query),
        'response_length': len(bot_response)
    }
    
    # Save to global queries log
    queries_log = []
    if os.path.exists(QUERIES_LOG_FILE):
        with open(QUERIES_LOG_FILE, 'r') as f:
            try:
                queries_log = json.load(f)
            except:
                queries_log = []
    
    queries_log.append(query_data)
    with open(QUERIES_LOG_FILE, 'w') as f:
        json.dump(queries_log, f, indent=2)
    
    # Save individual query file
    query_filename = timestamp.strftime("%Y%m%d_%H%M%S_%f")[:-3]
    query_filepath = os.path.join(QUERIES_DIR, f"{query_filename}.json")
    with open(query_filepath, 'w') as f:
        json.dump(query_data, f, indent=2)
    
    return query_data

def get_current_chat_id():
    """Get current chat ID from session or create new one"""
    chat_id = request.cookies.get('current_chat_id')
    if not chat_id:
        chat_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    return chat_id

def save_chat(chat_id, messages):
    """Save chat messages to file"""
    filepath = os.path.join(CHATS_DIR, f"{chat_id}.json")
    with open(filepath, 'w') as f:
        json.dump(messages, f)

def load_chat(chat_id):
    """Load chat messages from file"""
    filepath = os.path.join(CHATS_DIR, f"{chat_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def get_all_chats():
    """Get list of all chat files"""
    chats = []
    if os.path.exists(CHATS_DIR):
        for filename in sorted(os.listdir(CHATS_DIR), reverse=True):
            if filename.endswith('.json'):
                chat_id = filename[:-5]
                messages = load_chat(chat_id)
                if messages:
                    # Get chat name from timestamp and first message
                    try:
                        dt = datetime.strptime(chat_id, "%Y%m%d_%H%M%S_%f")
                        chat_name = dt.strftime("%b %d, %Y %I:%M %p")
                    except:
                        chat_name = chat_id
                    
                    # Try to use first user message as preview
                    preview = ""
                    for msg in messages:
                        if msg.get('role') == 'user':
                            preview = msg.get('text', '')[:50]
                            break
                    
                    chats.append({
                        'id': chat_id,
                        'name': chat_name,
                        'preview': preview,
                        'timestamp': chat_id
                    })
    return chats

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/api/chats", methods=["GET"])
def get_chats():
    """Get all chats"""
    chats = get_all_chats()
    return jsonify(chats)

@app.route("/api/chat/<chat_id>", methods=["GET"])
def get_chat(chat_id):
    """Get specific chat"""
    messages = load_chat(chat_id)
    return jsonify({'messages': messages})

@app.route("/api/chat/new", methods=["POST"])
def new_chat():
    """Create new chat"""
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    save_chat(chat_id, [])
    response = jsonify({'chat_id': chat_id})
    response.set_cookie('current_chat_id', chat_id, max_age=31536000)
    return response

@app.route("/api/chat/<chat_id>/delete", methods=["DELETE"])
def delete_chat(chat_id):
    """Delete a chat"""
    filepath = os.path.join(CHATS_DIR, f"{chat_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'status': 'deleted'})
    return jsonify({'status': 'not found'}), 404

@app.route("/api/queries", methods=["GET"])
def get_all_queries():
    """Get all logged user queries"""
    if os.path.exists(QUERIES_LOG_FILE):
        with open(QUERIES_LOG_FILE, 'r') as f:
            try:
                queries = json.load(f)
                return jsonify({
                    'total_queries': len(queries),
                    'queries': queries
                })
            except:
                return jsonify({'total_queries': 0, 'queries': []})
    return jsonify({'total_queries': 0, 'queries': []})

@app.route("/api/queries/chat/<chat_id>", methods=["GET"])
def get_chat_queries(chat_id):
    """Get all queries from a specific chat"""
    if os.path.exists(QUERIES_LOG_FILE):
        with open(QUERIES_LOG_FILE, 'r') as f:
            try:
                all_queries = json.load(f)
                chat_queries = [q for q in all_queries if q.get('chat_id') == chat_id]
                return jsonify({
                    'chat_id': chat_id,
                    'total_queries': len(chat_queries),
                    'queries': chat_queries
                })
            except:
                return jsonify({'chat_id': chat_id, 'total_queries': 0, 'queries': []})
    return jsonify({'chat_id': chat_id, 'total_queries': 0, 'queries': []})

@app.route("/api/queries/export", methods=["GET"])
def export_queries():
    """Export all queries as JSON"""
    if os.path.exists(QUERIES_LOG_FILE):
        with open(QUERIES_LOG_FILE, 'r') as f:
            try:
                queries = json.load(f)
                return jsonify(queries)
            except:
                return jsonify([])
    return jsonify([])

@app.route("/api/queries/search", methods=["POST"])
def search_queries():
    """Search queries by keyword"""
    search_term = request.json.get('search_term', '').lower()
    if not search_term:
        return jsonify({'results': []})
    
    if os.path.exists(QUERIES_LOG_FILE):
        with open(QUERIES_LOG_FILE, 'r') as f:
            try:
                all_queries = json.load(f)
                results = [q for q in all_queries if search_term in q.get('user_query', '').lower()]
                return jsonify({
                    'search_term': search_term,
                    'total_results': len(results),
                    'results': results
                })
            except:
                return jsonify({'search_term': search_term, 'total_results': 0, 'results': []})
    return jsonify({'search_term': search_term, 'total_results': 0, 'results': []})

@app.route("/api/queries/stats", methods=["GET"])
def get_query_stats():
    """Get statistics about all queries"""
    if os.path.exists(QUERIES_LOG_FILE):
        with open(QUERIES_LOG_FILE, 'r') as f:
            try:
                all_queries = json.load(f)
                total_queries = len(all_queries)
                total_chars = sum(q.get('query_length', 0) for q in all_queries)
                avg_query_length = total_chars / total_queries if total_queries > 0 else 0
                
                # Count queries per chat
                chat_counts = {}
                for q in all_queries:
                    chat_id = q.get('chat_id')
                    chat_counts[chat_id] = chat_counts.get(chat_id, 0) + 1
                
                return jsonify({
                    'total_queries': total_queries,
                    'total_characters': total_chars,
                    'average_query_length': round(avg_query_length, 2),
                    'queries_per_chat': chat_counts
                })
            except:
                return jsonify({'total_queries': 0})
    return jsonify({'total_queries': 0})

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    chat_id = request.form.get("chat_id", get_current_chat_id())
    
    print(f"User query: {msg}")
    response = rag_chain.invoke({"input": msg})
    answer = re.sub(r'<think>.*?</think>', '', response["answer"], flags=re.DOTALL).strip()
    answer = re.sub(r"Here's a thinking process:.*", '', answer, flags=re.DOTALL).strip()
    print("Response : ", answer)
    
    # Log the query with all metadata
    log_query(chat_id, msg, answer)
    
    # Save to chat history
    messages = load_chat(chat_id)
    messages.append({'role': 'user', 'text': msg})
    messages.append({'role': 'bot', 'text': answer})
    save_chat(chat_id, messages)
    
    return jsonify({
        'answer': answer,
        'chat_id': chat_id
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)