# AI Research Paper Reviewer

An advanced, automated platform for academic paper analysis. Powered by multi-agent AI, this tool extracts deep insights, synthesizes literature, and provides actionable future research directions.

## 🚀 Key Features

- **Multi-Agent Deep Analysis**: Extracts detailed methodology, key contributions, and core research problems.
- **Dedicated Future Scope**: A specialized module that identifies paper limitations and converts them into actionable improvement points for follow-up research.
- **AI Peer Review**: Generates structured reviews with strengths, weaknesses, and conference-style scoring (1-10).
- **Literature Synthesis**: Automatically searches Semantic Scholar and arXiv to summarize the current state of the field and identify trends/gaps.
- **Novelty Assessment**: Uses AI to determine the uniqueness of the research compared to existing literature.
- **Premium UI/UX**: Modern glassmorphism design with responsive tabs, real-time analysis progress, and a custom AI-themed interface.

## 🛠 Tech Stack

### Frontend
- **Framework**: [Next.js 14](https://nextjs.org/) (App Router)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **State Management**: React Hooks (useState/useEffect)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **LLM Engine**: [GROQ](https://groq.com/) (Llama-3-70B & 8B)
- **PDF Processing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- **Search API**: [Semantic Scholar API](https://www.semanticscholar.org/product/api)

## 📦 Installation & Setup

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Configuration**:
Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Frontend Setup
```bash
cd frontend
npm install
```

## 🏃 Running the Application

### Start Backend Server
```bash
cd backend
python main.py
```
*Backend runs on `http://localhost:8000`*

### Start Frontend Dev Server
```bash
cd frontend
npm run dev
```
*Frontend runs on `http://localhost:3000`*

## 📁 Project Structure

- `backend/agents/`: Specialized AI agents (Analyzer, Literature, Peer Review).
- `backend/tools/`: Integration with external search APIs and PDF parsers.
- `frontend/app/components/`: Modular React components (FutureScope, PaperSummary, etc.).
- `frontend/app/lib/`: API client and utility functions.

## ✍️ Author

**Developed by Hazrat Ali**
- [Portfolio/Website](https://hazratali1.github.io/Hazrat-Ali/)
- Built with passion for academic research and AI innovation.

---
*Disclaimer: This tool is intended for research assistance. Always verify AI-generated insights with original source materials.*
