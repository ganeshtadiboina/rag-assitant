🚀 Overview

RAG Assistant is a production-grade Retrieval-Augmented Generation (RAG) system that enables users to upload documents and ask context-aware questions. The application combines semantic search, hybrid retrieval, and large language models to generate accurate, citation-based answers.

Designed with scalability and usability in mind, the system integrates modern AI technologies and provides an intuitive Material UI interface for seamless interaction.

🌟 Key Features
📄 Document Upload – Supports ingestion of text and PDF documents.
🔍 Hybrid Retrieval – Combines BM25 keyword search with semantic vector search.
🧠 Vector Database – Utilizes Qdrant for efficient embedding storage and retrieval.
🎯 Cross-Encoder Reranking – Improves the relevance of retrieved results.
🤖 LLM-Powered Responses – Generates accurate answers using OpenAI GPT models.
🧵 Thread-Based Context – Supports multi-user and multi-session querying.
📚 Citation Support – Answers include references to source documents.
🎨 Modern UI – Built with React and Material UI for a professional experience.
⚡ FastAPI Backend – High-performance API for ingestion and querying.
☁️ Vercel Deployment – Frontend hosted for global accessibility.


🏗️ Architecture

User → React (Vercel) → FastAPI Backend → Qdrant Vector DB
                                 ↓
                        Hybrid Retrieval (BM25 + Embeddings)
                                 ↓
                        Cross-Encoder Reranker
                                 ↓
                          OpenAI GPT Model
                                 ↓
                           Final Answer



🔧 Technology Stack
Layer	Technology
Frontend	React, Vite, Material UI
Backend	FastAPI
Vector Database	Qdrant
Embeddings	Sentence Transformers
Retrieval	BM25 + Semantic Search
Reranking	Cross-Encoder
LLM	OpenAI GPT (e.g., gpt-4o-mini)
Deployment	Vercel (Frontend)


🌐 Live Demo
Frontend (Vercel): https://your-vercel-app.vercel.app
Backend API: http://localhost:8001/docs (or your hosted backend URL)



📸 Application Screenshots
Upload Interface

	Query Interface	Response
Upload documents for indexing	Ask questions based on uploaded content	Receive accurate, citation-based answers



📁 Project Structure
production-rag-app/
│
├── api/                     # FastAPI application
│   ├── routes/
│   ├── services/
│   └── schemas/
│
├── app/                     # Core RAG pipeline
│   ├── ingestion/
│   ├── retrieval/
│   ├── reranker/
│   ├── generation/
│   └── vectorstore/
│
├── rag-frontend/            # React + Material UI frontend
│   ├── src/
│   └── public/
│
├── data/                    # Uploaded and sample documents
├── requirements.txt         # Backend dependencies
├── .env                     # Environment variables
└── README.md
⚙️ Getting Started
🔹 1. Clone the Repository
git clone https://github.com/your-username/rag-assistant.git
cd rag-assistant
🔹 2. Backend Setup
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
touch .env
🔹 3. Environment Variables
OPENAI_API_KEY=your_openai_api_key
QDRANT_HOST=localhost
QDRANT_PORT=6333
COLLECTION_NAME=rag_documents
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
LLM_MODEL=gpt-4o-mini
TOP_K=5
🔹 4. Start Qdrant
docker run -p 6333:6333 qdrant/qdrant
🔹 5. Run the Backend
uvicorn api.main:app --reload --port 8001

Access API docs at:

http://localhost:8001/docs
🔹 6. Frontend Setup
cd rag-frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5174
☁️ Deployment on Vercel
🔹 Step 1: Prepare Frontend Environment

Create rag-frontend/.env:

VITE_API_URL=https://your-backend-api.com
🔹 Step 2: Deploy to Vercel
npm install -g vercel
cd rag-frontend
vercel

Follow the prompts:

Framework: Vite
Build Command: npm run build
Output Directory: dist
🔹 Step 3: Add Environment Variables in Vercel

In the Vercel dashboard:

VITE_API_URL = https://your-backend-api.com
🧪 API Endpoints
📤 Upload Document
POST /upload
Content-Type: multipart/form-data

Form Fields

file – Document to upload
user_id – Unique user identifier
thread_id – Conversation thread identifier
🔍 Query Documents
POST /query
Content-Type: application/json

Request

{
  "query": "What is deep learning?",
  "thread_id": "thread_ai"
}

Response

{
  "answer": "Deep learning uses neural networks. [Doc1]"
}
📊 Qdrant Database Access
Dashboard: http://localhost:6333/dashboard
List Collections: http://localhost:6333/collections
🛡️ Security Considerations
Store API keys securely using .env.
Ensure .env is included in .gitignore.
Rotate API keys if accidentally exposed.
Enable HTTPS when deploying the backend.
📈 Future Enhancements
🔐 User Authentication (JWT/Firebase)
💬 Chat History per Thread
📊 Analytics Dashboard
🐳 Dockerization and AWS Deployment
📚 Support for Additional Document Formats
🌍 Multi-language Query Support
🤝 Contributing

Contributions are welcome! Please follow these steps:

# Fork the repository
# Create a new branch
git checkout -b feature/your-feature

# Commit changes
git commit -m "Add your feature"

# Push and create a pull request
git push origin feature/your-feature
📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

👨‍💻 Author

Ganesh Tadiboina

🌐 LinkedIn: https://www.linkedin.com/
💻 GitHub: https://github.com/your-username
📧 Email: your-email@example.com


🙏 Acknowledgements
OpenAI – Language model capabilities
Qdrant – Vector database
LangChain Community – Document loaders
Hugging Face – Embedding and reranking models
Material UI – Frontend design system
Vercel – Seamless frontend deployment
⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub!