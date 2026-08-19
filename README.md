# AdI-Psychotherapist-Chatbot
## Build-a-Complete-Mental-Health-Chatbot-with-LLMs-LangChain-Pinecone-Flask

Rationale Behind the Name "AdI Bot"

The nomenclature AdI Bot has been chosen to reflect both technological orientation and personal identity. The term "AdI" originates as a contraction of the developer's name, Adiba, while simultaneously incorporating AI (Artificial Intelligence), the central foundation of the project. This dual representation establishes a meaningful connection between the creator and the system, offering a personalized dimension to an otherwise technical construct. By embedding individuality into the project, it emphasizes the human-centered intent behind its design, aligning with the broader objective of leveraging artificial intelligence for empathetic, socially impactful applications in mental health support.

## ✨ Features

### 🧠 Core Capabilities
- **AI-Powered Therapy** - Uses LangChain and NVIDIA LLaMA models for empathetic responses
- **RAG (Retrieval Augmented Generation)** - Knowledge base retrieval from Pinecone vector database
- **Solution-Focused Responses** - Provides practical solutions alongside emotional validation
- **Persistent Chat History** - All conversations saved with timestamps

### 💾 Chat Management
- **Multiple Conversations** - Create and manage multiple chat sessions
- **Chat History Sidebar** - Browse all previous chats with dates and message previews
- **Switch Between Chats** - Seamlessly switch between different conversations
- **Delete Chats** - Remove individual conversations

### 📊 Query Logging & Analytics
- **Global Query Log** - All user queries stored in `queries_log.json`
- **Individual Query Files** - Each query saved separately with metadata
- **Query Search** - Search through all queries by keyword
- **Query Statistics** - Track total queries, average length, per-chat counts

### 🔒 Security
- **.env Protection** - API keys are gitignored and not uploaded to GitHub
- **Secure Credentials** - PINECONE_API_KEY and NVIDIA_API_KEY stored securely

## 🚀 How to Run

### Prerequisites
- Python 3.12+
- pip or conda
- NVIDIA API Key
- Pinecone API Key

### Installation Steps

**STEP 01 - Clone the repository**
```bash
git clone https://github.com/adibaarooj/AdI-Psychotherapist-Chatbot.git
cd AdI-Psychotherapist-Chatbot
```

**STEP 02 - Create a Python virtual environment**

Using venv:
```bash
python -m venv psycho
# On Windows:
psycho\Scripts\activate
# On macOS/Linux:
source psycho/bin/activate
```

Or using conda:
```bash
conda create -n adibot python=3.12 -y
conda activate adibot
```

**STEP 03 - Install dependencies**
```bash
pip install -r requirements.txt
```

**STEP 04 - Configure environment variables**

Create a `.env` file in the root directory with your API keys:
```ini
PINECONE_API_KEY=your_pinecone_api_key_here
NVIDIA_API_KEY=your_nvidia_api_key_here
```

⚠️ **Important**: The `.env` file is gitignored and will NOT be uploaded to GitHub. Never share your API keys!

**STEP 05 - Initialize the vector database**
```bash
python store_index.py
```

**STEP 06 - Run the Flask application**
```bash
python app.py
```

The chatbot will be available at `http://localhost:8080`

## 🔌 API Endpoints

### Chat Management
- `GET /` - Main chat interface
- `GET /api/chats` - Get all chat conversations
- `GET /api/chat/<chat_id>` - Get specific chat messages
- `POST /api/chat/new` - Create new chat
- `DELETE /api/chat/<chat_id>/delete` - Delete a chat
- `POST /get` - Send message and get AI response

### Query Analytics
- `GET /api/queries` - Get all logged user queries
- `GET /api/queries/chat/<chat_id>` - Get queries from specific chat
- `POST /api/queries/search` - Search queries by keyword
- `GET /api/queries/stats` - Get query statistics
- `GET /api/queries/export` - Export all queries as JSON

### Example API Calls
```bash
# Get all chats
curl http://localhost:8080/api/chats

# Search for queries containing "anxiety"
curl -X POST http://localhost:8080/api/queries/search \
	-H "Content-Type: application/json" \
	-d '{"search_term":"anxiety"}'

# Get query statistics
curl http://localhost:8080/api/queries/stats
```

## 📁 Project Structure

```
AdI-Psychotherapist-Chatbot/
├── app.py                 # Main Flask application with chat endpoints
├── requirements.txt       # Python dependencies
├── .env                   # API keys (gitignored - not shared)
├── .gitignore            # Files to ignore in git
├── README.md             # Project documentation
├── store_index.py        # Initialize Pinecone vector database
├── template.py           # Template configurations
│
├── src/
│   ├── __init__.py
│   ├── helper.py         # Helper functions & embeddings
│   └── prompt.py         # System prompts for the chatbot
│
├── templates/
│   └── chat.html         # Web interface
│
├── static/
│   └── style.css         # UI styling
│
├── chats_history/        # Stored chat conversations (JSON)
├── user_queries/         # Individual query logs (JSON)
├── queries_log.json      # Global query log
│
└── psycho/              # Virtual environment directory (gitignored)
```

## 💾 File Storage

### Chat History
All conversations are stored as JSON files in the `chats_history/` directory with filenames based on timestamps (e.g., `20260819_163640_798.json`).

### Query Logs
User queries are logged in two places:
- **`queries_log.json`** - Master log with all queries
- **`user_queries/`** - Individual JSON files for each query with metadata

Each logged query contains:
- Timestamp (ISO format)
- Chat ID
- User's question
- Bot's response
- Query length & response length

## 🛠️ Technologies Used

- **Flask** - Web framework for the chatbot interface
- **LangChain** - LLM orchestration and RAG implementation
- **Pinecone** - Vector database for knowledge retrieval
- **NVIDIA LLaMA 3.1** - Large language model via NVIDIA AI Endpoints
- **HuggingFace Embeddings** - Text embedding generation
- **jQuery** - Frontend interactivity
- **JSON** - Data persistence for chats and queries

## 🔐 Environment Variables

```env
PINECONE_API_KEY=your_api_key_here      # Pinecone vector database key
NVIDIA_API_KEY=your_api_key_here        # NVIDIA LLM API key
```

## 🛡️ Security Best Practices

✅ **Files Protected by .gitignore**
- `.env` - Environment variables with API keys
- `psycho/` - Virtual environment (auto-generated)
- `chats_history/` - Local chat data
- `user_queries/` - Local query data

✅ **Never:**
- Commit `.env` file to GitHub
- Share API keys or credentials
- Upload local data files to repository

✅ **Do:**
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Keep dependencies updated

## 🐛 Troubleshooting

### API Key Issues
- Ensure `PINECONE_API_KEY` and `NVIDIA_API_KEY` are set in `.env`
- Verify keys have correct permissions in their respective dashboards
- Check if API keys are expired or revoked

### Model Loading
- First run may take time loading HuggingFace embeddings
- Ensure sufficient disk space for model downloads (2-3GB)
- Check internet connection for downloading models

### Chat Not Saving
- Verify `chats_history/` and `user_queries/` directories exist
- Check file permissions for JSON storage
- Ensure disk space is available

### Port Already in Use
- Change Flask port in `app.py` from 8080 to another port
- Or kill process using port 8080

## ⚙️ Performance Considerations

- **Embeddings**: Generated using HuggingFace (cached after first run)
- **Vector Search**: Powered by Pinecone for fast similarity matching
- **LLM Inference**: Uses NVIDIA's optimized models for quick responses
- **Frontend**: Real-time chat updates using jQuery AJAX

## 🚀 Future Enhancements

- [ ] User authentication and profiles
- [ ] Advanced analytics dashboard
- [ ] Export chat history to PDF
- [ ] Dark/Light theme toggle
- [ ] Voice input/output support
- [ ] Sentiment analysis per conversation
- [ ] Scheduled mental health check-ins
- [ ] Multi-language support
- [ ] Mobile app version

## 📜 License

This project is open-source and available under the MIT License.

## 💬 Contact & Support

For questions or support, please:
- Open an issue in the GitHub repository
- Contact the developer at your email
- Check documentation for troubleshooting

---

**Last Updated**: August 19, 2026  
**Version**: 1.0.0  
**Status**: Active Development
