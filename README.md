# Expense Tracker AI

An AI-powered expense management app built with a LangGraph ReAct agent and a React frontend. Ask questions about your spending in plain English and get answers backed by real data.
<br><br/>
<br>
<img width="2153" height="1377" alt="Expenses" src="https://github.com/user-attachments/assets/0e581e15-e3a1-42a1-b9c7-d123d4108f75" />
<br/>
<br>
<img width="2234" height="1348" alt="cat_break" src="https://github.com/user-attachments/assets/d4dbdd41-11a3-436e-83e9-0ce4bd31ecad" />
<br/>
<br>
<img width="2332" height="1381" alt="spending_trends" src="https://github.com/user-attachments/assets/eba2d950-4903-4301-9984-e62e0ec5787a" />
<br/>



## Stack

- **Frontend**: React + Vite + Tailwind CSS + Recharts
- **Backend**: FastAPI
- **Agent**: LangGraph ReAct agent
- **LLM**: Ollama (Llama 3.1 8B, runs locally)
- **Database**: SQLite
- **Optional**: Splitwise API for importing shared expenses

## Prerequisites

- Python 3.8+
- Node.js 16+
- [Ollama](https://ollama.ai/download) with the model pulled:

```bash
ollama pull llama3.1:8b-instruct-q4_K_M
```

## Setup

**1. Install Python dependencies**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Install frontend dependencies**

```bash
cd frontend && npm install && cd ..
```

**3. Configure environment**

Copy `.env.example` to `.env` and fill in your values:

```env
DB_PATH=expenses.db
OLLAMA_MODEL=llama3.1:8b-instruct-q4_K_M
OLLAMA_BASE_URL=http://localhost:11434

# Optional — only needed for Splitwise sync
SPLITWISE_ACCESS_TOKEN=your_token_here
MY_USER_ID=your_user_id
```

## Running

Start both servers in separate terminals:

```bash
# Terminal 1 — backend
python -m uvicorn backend.api:app --reload

# Terminal 2 — frontend
npm run dev --prefix frontend
```

Open [http://localhost:5173](http://localhost:5173).

## Project Structure

```
expense-tracker-ai/
├── backend/
│   └── api.py              # FastAPI server
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── agent.py                # LangGraph ReAct agent
├── db.py                   # SQLite operations
├── sync_splitwise.py       # Splitwise integration
├── requirements.txt
└── .env
```

## Example Queries

- "What were my expenses this month?"
- "Show me spending trends for the last 2 months"
- "Give me a category breakdown for this month"
- "Add $50 for groceries"
- "What are my top expenses?"

## Troubleshooting

**Ollama errors** — make sure Ollama is running (`ollama serve`) and the model is downloaded (`ollama list`).

**Port conflicts** — backend defaults to `8000`, frontend to `5173`. Make sure both are free.

**Fresh database** — delete `expenses.db` and restart the backend to reset.
