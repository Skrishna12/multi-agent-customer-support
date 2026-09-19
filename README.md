# 🤖 Multi-Agent Customer Support Intelligence Platform

An AI-powered multi-agent customer support platform designed to automate ticket understanding, classification, sentiment analysis, knowledge retrieval, response generation, escalation, and support analytics for high-volume eCommerce environments.

The system combines **CrewAI, Machine Learning, RAG, FAISS, Sentence Transformers, and Groq LLMs** to create an end-to-end intelligent customer support workflow.

---

## 🚀 Overview

Customer support teams handle thousands of tickets involving delivery problems, refunds, payment issues, product defects, account problems, and technical issues.

This project automates the support workflow using specialized AI agents.

### Core Workflow
Customer Ticket
      │
      ▼
┌─────────────────────┐
│    Intake Agent     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Classification Agent│
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│   Sentiment Agent   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│   Retrieval Agent   │
│        RAG          │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│    Response Agent   │
│      Groq LLM       │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Escalation Agent   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Learning & Analytics│
└─────────────────────┘

✨ Features
🎯 Intelligent Ticket Intake

The Intake Agent processes incoming customer messages and extracts:

Cleaned ticket text
Customer intent
Urgency
Order ID
Product information
Follow-up context

Supported intents include:

Refund Request
Replacement Request
Delivery Issue
Payment Issue
Account/Login Issue
🧠 Ticket Classification

The Classification Agent predicts:

Ticket category
Priority
Assigned support team
Prediction confidence

Supported categories:

Delivery Issue
Refund & Return
Payment Issue
Product Issue
Account & Login
Seller & Product Listing
App & Website Issue

The classification system uses:

TF-IDF + Logistic Regression

😊 Sentiment Analysis

The Sentiment Agent analyzes customer tone and identifies:

Positive
Neutral
Slightly Negative
Negative
Very Negative

The system also provides sentiment signals and confidence.

🔎 Retrieval-Augmented Generation (RAG)

The Retrieval Agent searches a knowledge base containing:

Frequently Asked Questions
Historical resolved support tickets

The RAG system uses:

Sentence Transformers
all-MiniLM-L6-v2
FAISS
384-dimensional embeddings
Normalized vector similarity search
Knowledge Base
10,000 historical support tickets
150 FAQ documents
-------------------------
10,150 indexed documents

The system retrieves relevant historical resolutions and FAQ information before generating a response.

💬 AI Response Generation

The Response Agent generates customer-facing responses using:

Groq + OpenAI GPT-OSS 120B

The response generation process considers:

Customer ticket
Intent
Category
Priority
Sentiment
Conversation context
Retrieved knowledge

The system is designed to use retrieved information and avoid inventing unsupported policies.

🚨 Intelligent Escalation

The Escalation Agent calculates an escalation score based on factors such as:

Ticket priority
Customer sentiment
Classification confidence
Retrieval quality
Ticket complexity

Possible outcomes:

AUTO-HANDLE
     or
ESCALATE

The system also records the reasons behind escalation decisions.

📊 Learning & Analytics

The Learning Agent analyzes support activity and provides statistics such as:

Total tickets analyzed
Automation rate
Escalation rate
Category distribution
Sentiment distribution
Classification confidence
Retrieval statistics
Customer feedback
Satisfaction statistics
🏗️ System Architecture
                    ┌─────────────────────┐
                    │    Customer Ticket  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Intake Agent     │
                    │ Intent / Entities   │
                    │ Urgency / Context   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Classification      │
                    │ Agent               │
                    │ Category / Priority │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Sentiment Agent     │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       Retrieval Agent           │
              │                                │
              │  FAQ Knowledge Base            │
              │          +                     │
              │  Historical Support Tickets    │
              │          ↓                     │
              │         FAISS                  │
              └──────────────┬─────────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │   Response Agent    │
                    │    Groq LLM         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Escalation Agent    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
              AUTO-HANDLE             ESCALATE
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Learning & Database  │
                    │ Analytics            │
                    └─────────────────────┘
🧩 Multi-Agent Architecture

The CrewAI implementation contains seven specialized agents:

Agent	Responsibility
Intake Agent	Understand and extract ticket information
Classification Agent	Predict category and priority
Sentiment Agent	Analyze customer sentiment
Retrieval Agent	Retrieve relevant knowledge
Response Agent	Generate customer response
Escalation Agent	Determine escalation requirement
Learning Agent	Analyze system performance

The agents operate sequentially as part of the CrewAI workflow.

🛠️ Technology Stack
Component	Technology
Programming Language	Python
Multi-Agent Framework	CrewAI
LLM	Groq – GPT-OSS 120B
Machine Learning	Scikit-learn
Text Features	TF-IDF
Classification	Logistic Regression
Embeddings	Sentence Transformers
Vector Search	FAISS
Backend API	FastAPI
Frontend	Streamlit
Database	SQLite
Data Processing	Pandas, NumPy
Model Persistence	Joblib
📁 Project Structure
multi-agent-customer-support/
│
├── agents/
│   ├── intake_agent.py
│   ├── classification_agent.py
│   ├── sentiment_agent.py
│   ├── retrieval_agent.py
│   ├── response_agent.py
│   ├── escalation_agent.py
│   ├── learning_agent.py
│   ├── feedback_agent.py
│   ├── support_pipeline.py
│   ├── crewai_agents.py
│   ├── crewai_tasks.py
│   └── crewai_orchestrator.py
│
├── api/
│   └── ...
│
├── app/
│   └── ...
│
├── database/
│   └── support_database.py
│
├── models/
│   ├── train_models.py
│   └── predict.py
│
├── rag/
│   ├── build_index.py
│   └── retrieval_agent.py
│
├── evaluation/
│   ├── evaluate_system.py
│   └── ...
│
├── data/
│   ├── support_tickets_10k.csv
│   └── faq_knowledge_base_150.csv
│
├── main.py
├── requirements.txt
└── README.md
📊 Dataset

The project uses two primary datasets.

Support Tickets
10,000 support tickets
15 columns

Important fields include:

Ticket ID
Created Date
Ticket Text
Product Name
Product Segment
Ticket Category
Priority
Sentiment
Confidence Score
Escalation
Resolution Text
Resolved Date
Resolution Days
Auto Resolved
Customer Satisfaction Score
FAQ Knowledge Base
150 FAQ documents

Fields include:

FAQ ID
Question
Answer
Category
📈 Model Evaluation

The classification system was evaluated on a held-out test set of 2,000 tickets.

Category Classification
Accuracy:  1.0000
Precision: 1.0000
Recall:    1.0000
F1 Score:  1.0000
Priority Classification
Accuracy:  0.9119
Precision: 0.9121
Recall:    0.9119
F1 Score:  0.9108
RAG Evaluation

The retrieval system was evaluated on 700 tickets.

Coverage:             100%
Average Top-1 Score: 0.7920
Average Top-3 Score: 0.7511
Average Top-5 Score: 0.6291
Category Match:      100%

The RAG knowledge base contains:

10,150 documents

including FAQs and historical support tickets.

🔧 Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/multi-agent-customer-support.git
cd multi-agent-customer-support
2. Create a virtual environment
python -m venv crewai_venv
3. Activate the environment
Windows
.\crewai_venv\Scripts\Activate.ps1
Linux/macOS
source crewai_venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create a .env file or configure the environment variable directly.

GROQ_API_KEY=your_groq_api_key

Never commit your .env file or API keys to GitHub.

▶️ Running the Project
Run the Support Pipeline
python -m agents.support_pipeline
Run the CrewAI Orchestrator
python -m agents.crewai_orchestrator
Run Streamlit
streamlit run app/app.py
Run FastAPI
uvicorn api.main:app --reload
🧪 Example
Customer Ticket
My wireless headphones are broken and I want a replacement.
Order: ORD7824512
AI Processing
Category: Product Issue
Priority: High
Sentiment: Slightly Negative
Team: Product Support Team

The Retrieval Agent searches historical tickets and FAQs for similar cases.

The Response Agent generates a contextual customer response using the retrieved information.

The Escalation Agent then determines whether the ticket can be automatically handled or should be escalated.

💾 Database

The system stores operational information including:

Processed tickets
Escalation scores
Retrieval logs
Agent logs
Customer feedback

SQLite is used for local persistence.

📊 Evaluation Metrics

The platform evaluates multiple aspects of the system.

Classification
Accuracy
Precision
Recall
F1 Score
Retrieval
Top-K similarity
Retrieval coverage
Category matching
FAQ vs historical-ticket retrieval
Operations
Automation rate
Escalation rate
Resolution time
Customer satisfaction
Response Generation
Response quality
Relevance to retrieved knowledge
Customer-facing consistency
🔮 Future Improvements

Potential future enhancements include:

Human-in-the-loop feedback learning
Automated model retraining
Advanced conversation memory
BLEU/ROUGE response evaluation
PostgreSQL deployment
Production-grade vector database
Authentication and role-based access
Docker deployment
Cloud deployment
Monitoring and observability
Real-time customer support integration
🎯 Project Goals

The platform demonstrates how multiple AI agents can collaborate to automate customer support workflows while maintaining:

Context awareness
Knowledge-grounded responses
Explainable escalation decisions
Retrieval-based support
Operational analytics
👨‍💻 Author

Sai Krishna

Data Science | Machine Learning | Artificial Intelligence | Python

📄 License

This project is intended for educational, research, and portfolio purposes.
