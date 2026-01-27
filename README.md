# 🌱 KnowledgeShare  
**Preserving Traditional Sustainability. Adapting It for the Modern World.**

> A trust-aware, AI-assisted knowledge platform that captures, validates, discovers, and adapts traditional sustainable practices for today’s lifestyles.

---

## 🚀 Why KnowledgeShare?

Traditional sustainability knowledge is disappearing fast — passed orally, scattered across regions, and often unverified.  
At the same time, generic AI tools provide unsafe or hallucinated recommendations.

**KnowledgeShare bridges this gap** by combining:
- Human-validated knowledge
- Semantic search
- Context-aware AI adaptation
- Trust-driven ranking

---

## 🧩 Core Problems We Address

- Loss of undocumented traditional sustainability knowledge  
- Scattered and unstructured information  
- Lack of credibility and trust  
- Poor adaptability to modern, urban contexts  
- Unsafe or generic AI recommendations  

---

## 🏗️ System Architecture (Modular by Design)

KnowledgeShare is built as **independent but integrated engines**, ensuring scalability and clarity.

├── Ingestion Engine

├── Validation Engine

├── Search Engine

└── Modern Adaptation Engine


Each engine solves a **specific problem** and communicates through structured data.

---

## 🔹 Module Overview

### 1️⃣ Knowledge Ingestion Engine
- Accepts text, audio, image, and video inputs
- Converts submissions into structured JSON posts
- Stores practices with region, principles, steps, risks, and materials

### 2️⃣ Validation Engine
- Collects community comments and feedback
- Computes a dynamic **verification score (0–100)**
- Continuously updates trust level of each post

### 3️⃣ Semantic Search Engine
- Uses vector embeddings (ChromaDB)
- Combines semantic relevance with verification score
- Returns **trusted and relevant** practices first

### 4️⃣ Modern Adaptation Engine (AI)
- Personalizes a traditional practice to user context
- Context-aware (location, space, constraints)
- Grounded strictly in the original post (no hallucinations)
- Gracefully handles unsuitable practices

---

## 🧠 Key Design Principles

- Trust before intelligence  
- Human-in-the-loop validation  
- AI as an adapter, not a knowledge source  
- Modular & scalable architecture  
- Fail-safe design for AI services  

---

## 🖥️ User Experience Flow

1. Knowledge contributor submits a practice  
2. Community adds comments → trust score updates  
3. User searches for a sustainability problem  
4. Trusted practices are ranked and shown  
5. User adapts the practice to their modern context via chat-like interface  

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Flask (Python) |
| Search | ChromaDB + Sentence Transformers |
| AI | OpenAI API (context-aware adaptation) |
| Storage | JSON-based structured storage |
| Frontend | HTML, CSS (Server-side rendered) |

---

## 📁 Project Structure
knowledge_platform/

│

├── app.py

├── routes/

│ └── post_routes.py

│

├── adaptation_engine/

│ ├── adapter.py

│ └── prompt.py

│

├── search_engine/

│ ├── indexer.py

│ ├── searcher.py

│ └── chroma_client.py

│

├── validation_module/

│ ├── routes.py

│ └── utils.py

│

├── shared/

│ └── data_provider.py

│

├── templates/

├── static/

├── uploads/

│ ├── posts/

│ ├── comments/

│ └── media/

└── README.md


---

## ⚙️ Setup & Run

### 1️⃣ Clone Repository
```bash
git clone <repo-url>
cd knowledge_platform

### 2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Configure Environment
OPENAI_API_KEY=your_api_key_here

### 4️⃣ Configure Environment
python app.py


