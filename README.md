# 💰 Expense Tracker AI# 💰 Agentic Expense Tracker



An intelligent expense tracking system powered by Ollama and LangGraph, featuring a modern React frontend and FastAPI backend. Chat with your expenses naturally and get AI-powered insights.An intelligent expense tracking system powered by **LangGraph** and **Groq's Llama 3.1** that goes beyond simple logging—it analyzes, predicts, and provides proactive insights about your spending habits.



![License](https://img.shields.io/badge/license-MIT-blue.svg)## 🌟 What Makes This "Agentic"?

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

![React](https://img.shields.io/badge/react-18.2.0-blue.svg)Unlike traditional expense trackers, this system exhibits **true agentic behavior**:



## ✨ Features1. **🧠 Autonomous Planning** - Breaks down complex queries into actionable steps

2. **🔄 Tool Chaining** - Combines multiple tools to provide comprehensive answers

- **🤖 AI-Powered Chat Interface**: Natural language interaction with your expense data using Ollama LLM3. **💡 Proactive Insights** - Volunteers helpful information without being asked

- **📊 Real-time Analytics**: Instant spending insights and visualizations4. **📊 Context Awareness** - Remembers conversation history and user preferences

- **💳 Splitwise Integration**: Automatic sync with your Splitwise expenses5. **🎯 Goal-Oriented** - Works toward understanding and improving your financial health

- **💱 Multi-Currency Support**: Automatic currency conversion (INR → USD)

- **🎯 Smart Filtering**: Only tracks expenses you're actually involved in### Example Agentic Behaviors:

- **💬 Conversation Memory**: Context-aware responses across multiple queries

- **🎨 Modern UI**: Clean, responsive interface inspired by Frappe design**Query:** "How am I doing this month?"



## 🏗️ Architecture**Agent's Reasoning:**

```

```1. Fetch total spending for current month

┌─────────────────────────────────────────────────────────────┐2. Compare with last month's spending

│                      Frontend (React)                        │3. Analyze category breakdown

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │4. Check budget status across categories

│  │   Overview   │  │  Chat Panel  │  │   Results    │      │5. Generate insights and recommendations

│  │   Panel      │  │              │  │   Panel      │      │```

│  └──────────────┘  └──────────────┘  └──────────────┘      │

└─────────────────────────────────────────────────────────────┘**Response:**

                            │> "You've spent $1,247 this month, which is 23% more than last month ($1,015). Your top category is Food & Drink at $487 (39%). ⚠️ You're over budget on Groceries by $47. Consider reviewing your food expenses."

                     REST API (JSON)

                            │---

┌─────────────────────────────────────────────────────────────┐

│                     Backend (FastAPI)                        │## ✨ Features

│  ┌──────────────────────────────────────────────────────┐   │

│  │             LangGraph Agent (ReAct)                  │   │### Core Capabilities

│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │   │- ✅ **Natural Language Interface** - Chat with your expenses

│  │  │ Ollama   │  │ 4 Tools  │  │ Memory   │          │   │- ✅ **Smart SQL Generation** - Automatically converts questions to queries

│  │  │ LLM      │  │          │  │          │          │   │- ✅ **Budget Tracking** - Set limits and get proactive alerts

│  │  └──────────┘  └──────────┘  └──────────┘          │   │- ✅ **Trend Analysis** - Understand spending patterns over time

│  └──────────────────────────────────────────────────────┘   │- ✅ **Splitwise Integration** - Sync shared expenses automatically

│                            │                                 │- ✅ **Category Insights** - Break down spending by category

│  ┌─────────────────────────┼──────────────────────────┐     │- ✅ **Time Comparisons** - Compare months, weeks, or years

│  │         SQLite Database │  Splitwise API          │     │- ✅ **Persistent Memory** - Remembers your preferences and budgets

│  │         (expenses.db)   │  Integration            │     │

│  └─────────────────────────┴──────────────────────────┘     │### Agentic Tools

└─────────────────────────────────────────────────────────────┘1. **add_expense** - Add personal expenses

```2. **run_query** - Execute SQL queries intelligently

3. **analyze_spending_trends** - Detect patterns over time

## 🛠️ Tech Stack4. **get_category_insights** - Category breakdown with percentages

5. **compare_periods** - Month-over-month comparisons

### Backend6. **set_budget** - Define spending limits

- **FastAPI** - Modern Python web framework7. **get_smart_insights** - Proactive recommendations

- **LangGraph 0.6+** - Agentic workflow orchestration

- **Ollama** - Local LLM inference (llama3.1:8b-instruct-q4_K_M)---

- **SQLite** - Lightweight database

- **Splitwise API** - Expense synchronization## 🚀 Quick Start



### Frontend### 1. Prerequisites

- **React 18** - UI library- Python 3.8+

- **Vite** - Build tool and dev server- Free Groq API key ([Get it here](https://console.groq.com))

- **Tailwind CSS** - Utility-first styling

- **Lucide Icons** - Modern icon set### 2. Installation



### AI Agent Tools```powershell

1. **add_expense** - Add new expense with category detection# Clone or download the project

2. **run_query** - Execute SQL queries on expense datacd "Expense Tracker AI"

3. **get_spending_insights** - Generate AI-powered spending analysis

4. **sync_splitwise** - Sync expenses from Splitwise# Install dependencies

pip install -r requirements.txt

## 🚀 Quick Start```



### Prerequisites### 3. Configuration



1. **Install Ollama**```powershell

   ```bash# Copy the example environment file

   # Download from https://ollama.aiCopy-Item .env.example .env

   # Pull the required model

   ollama pull llama3.1:8b-instruct-q4_K_M# Edit .env and add your Groq API key

   ```# Get free key at: https://console.groq.com

```

2. **Python 3.9+** and **Node.js 16+**

Your `.env` file should look like:

### Installation```env

GROQ_API_KEY=gsk_your_actual_key_here

1. **Clone the repository**```

   ```bash

   git clone <your-repo-url>### 4. Initialize Database

   cd "Expense Tracker AI"

   ``````powershell

python db.py

2. **Set up Backend**```

   ```bash

   # Install Python dependencies### 5. Run the App

   pip install -r requirements.txt

```powershell

   # Copy environment templatepython app.py

   copy .env.example .env```



   # (Optional) Add Splitwise credentials to .envThe web interface will open at `http://localhost:7860`

   # SPLITWISE_ACCESS_TOKEN=your_token

   # MY_USER_ID=your_user_id---

   ```

## 🎮 Usage Examples

3. **Set up Frontend**

   ```bash### Adding Expenses

   cd frontend```

   npm installYou: "Add $15.50 for lunch at Chipotle"

   cd ..Agent: "✅ Added expense: $15.50 for lunch at Chipotle"

   ```

You: "Add $50 groceries"

4. **Initialize Database**Agent: "✅ Added expense: $50.00 for groceries. 

   ```bash       ⚡ You're at 87% of your Groceries budget this month."

   python -c "from db import init_db; init_db()"```

   ```

### Querying Expenses

### Running the Application```

You: "How much did I spend on food this month?"

**Option 1: Start Both Servers Manually**Agent: "You spent $487.50 on Food & Drink this month across 23 transactions. 

       That's 15% more than last month."

```bash

# Terminal 1 - Backend (from project root)You: "What are my top spending categories?"

python -m uvicorn backend.api:app --reloadAgent: "📊 Your top categories this month:

       1. Food & Drink: $487 (39%)

# Terminal 2 - Frontend       2. Transportation: $245 (20%)

cd frontend       3. Entertainment: $185 (15%)

npm run dev       ..."

``````



**Option 2: Using Separate Terminals**### Budget Management

```

1. Open PowerShell in project rootYou: "Set a budget of $500 for groceries"

2. Start backend: `python -m uvicorn backend.api:app --reload`Agent: "✅ Budget set: $500.00/month for groceries"

3. Open another PowerShell, navigate to `frontend/`

4. Start frontend: `npm run dev`You: "Am I over budget anywhere?"

Agent: "⚠️ You're over budget on:

**Access the Application:**       - Entertainment: $215 / $200 (107%)

- Frontend: http://localhost:5173       ✅ Everything else is on track!"

- Backend API: http://localhost:8000```

- API Docs: http://localhost:8000/docs

### Trend Analysis

## 💬 Example Queries```

You: "Show my spending trends"

Try these natural language commands:Agent: "📈 Spending trends (month):

       Total: $1,247, Average: $41.57/day

```       

🗨️ "Add expense for coffee $5"       You're spending more on weekends (avg $68/day) 

🗨️ "Show me all expenses from this month"       vs weekdays (avg $35/day)."

🗨️ "What did I spend on groceries in October?"```

🗨️ "Give me insights on my spending patterns"

🗨️ "Sync my Splitwise expenses"---

🗨️ "What are my top 3 expense categories?"

🗨️ "How much did I spend on food last month?"## 🔄 Splitwise Integration (Optional)

```

If you use Splitwise for shared expenses:

## 📂 Project Structure

### 1. Get Splitwise Token

```1. Go to https://secure.splitwise.com/apps

Expense Tracker AI/2. Register a new application

├── backend/3. Copy your API token

│   ├── api.py              # FastAPI routes and chat endpoint

│   └── __init__.py### 2. Configure

├── frontend/Add to your `.env` file:

│   ├── src/```env

│   │   ├── components/SPLITWISE_ACCESS_TOKEN=your_token_here

│   │   │   ├── Chat.jsx          # Chat interfaceMY_USER_ID=your_user_id

│   │   │   ├── Overview.jsx      # Spending summary```

│   │   │   └── ResultsPanel.jsx  # Tool results display

│   │   ├── App.jsx               # Main React component### 3. Get Your User ID

│   │   └── main.jsx              # React entry point```powershell

│   ├── package.jsonpython id.py

│   └── vite.config.js```

├── agent.py                # LangGraph agent with 4 tools

├── db.py                   # SQLite database operations### 4. Sync Expenses

├── sync_splitwise.py       # Splitwise API integration```powershell

├── mappers.py              # Data transformation & currency conversion# Sync latest 10 expenses

├── id.py                   # Configuration (API keys, user ID)python sync_splitwise.py

├── .env.example            # Environment template

├── .gitignore              # Git exclusions# Or use the "Sync Splitwise" button in the web UI

├── requirements.txt        # Python dependencies```

└── README.md               # This file

```---



## 🔧 Configuration## 🏗️ Architecture



### Environment Variables (`.env`)```

┌─────────────────────────────────────────┐

```bash│         Gradio Web Interface            │

# Splitwise Integration (Optional)└──────────────┬──────────────────────────┘

SPLITWISE_ACCESS_TOKEN=your_token_here               │

MY_USER_ID=your_splitwise_user_id┌──────────────▼──────────────────────────┐

│      LangGraph Agent (Groq LLM)         │

# Database Path (Optional, defaults to expenses.db)│  - Planning & Reasoning                 │

DB_PATH=expenses.db│  - Tool Selection                       │

```│  - Context Management                   │

└──────────────┬──────────────────────────┘

### Ollama Model               │

    ┌──────────┼──────────┐

The project uses `llama3.1:8b-instruct-q4_K_M` by default. To change:    │          │          │

┌───▼───┐  ┌──▼───┐  ┌──▼────┐

```python│ Tools │  │ DB   │  │Prefs  │

# Edit agent.py│       │  │      │  │       │

llm = ChatOllama(└───────┘  └──────┘  └───────┘

    model="your-model-name",```

    base_url="http://localhost:11434"

)### Key Components

```

- **app.py** - Gradio web interface

## 🎯 Key Features Deep Dive- **agent.py** - LangGraph agent with Groq LLM

- **db.py** - SQLite database operations

### 1. Agentic Architecture- **preferences.py** - User preferences & budgets

- Uses LangGraph's `create_react_agent` for ReAct (Reasoning + Acting) pattern- **splitwise_client.py** - Splitwise API integration

- Agent decides which tools to call based on user query- **sync_splitwise.py** - Sync Splitwise expenses

- Maintains conversation memory for context-aware responses- **mappers.py** - Data transformation utilities



### 2. Splitwise Integration---

- Automatic sync of shared expenses

- Filters expenses by user participation (only your expenses)## 🧪 Testing

- Adds group names to expense descriptions

- Caches group data for performance### Add Test Data

```powershell

### 3. Currency Conversionpython test.py

- Automatic conversion to USD for consistency```

- Preserves original amount in description: "(INR 3653.00)"

- Supports multiple currencies via `CURRENCY_TO_USD` mapping### Manual Testing Queries

- "How much did I spend this week?"

### 4. Smart Database Management- "Compare my spending to last month"

- Absolute path resolution prevents duplicate databases- "What's my biggest expense category?"

- Automatic schema initialization- "Set a $300 budget for dining out"

- SQL injection protection via parameterized queries- "Show me spending trends"

- "Add $8.50 coffee at Starbucks"

### 5. Real-time UI Updates

- Auto-refreshes overview panel after every interaction---

- Displays tool results in dedicated panel

- Smooth scrolling and responsive design## 🆓 Why Groq?



## 📊 Database Schema**Groq** is chosen because it's:

1. ✅ **Completely Free** - Generous free tier (30 req/min)

```sql2. ⚡ **Extremely Fast** - Optimized inference (<1s responses)

CREATE TABLE expenses (3. 🧠 **Capable Models** - Llama 3.1 70B (great for SQL & reasoning)

    id INTEGER PRIMARY KEY AUTOINCREMENT,4. 🔓 **No Local Installation** - Just API key needed

    date TEXT,              -- ISO format: YYYY-MM-DD5. 🎯 **Perfect for Structured Tasks** - Excels at SQL generation

    amount REAL,            -- In USD

    category TEXT,          -- Food, Transport, Entertainment, etc.### Getting Groq API Key

    description TEXT,       -- Includes group name if from Splitwise1. Visit https://console.groq.com

    splitwise_id TEXT       -- NULL for manual entries2. Sign up (Google/GitHub)

);3. Go to API Keys section

```4. Create new key

5. Copy and paste into `.env`

## 🐛 Troubleshooting

**It takes 2 minutes and is completely free!** ✨

### Backend Issues

---

**"Module not found" errors:**

```bash## 📊 Database Schema

# Make sure you're in project root and running:

python -m uvicorn backend.api:app --reload```sql

```CREATE TABLE expenses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

**Database not found:**    sw_expense_id INTEGER UNIQUE,          -- Splitwise ID (if synced)

```bash    description TEXT NOT NULL,

# Reinitialize database    amount REAL NOT NULL,

python -c "from db import init_db; init_db()"    category TEXT,                         -- e.g., 'Food & Drink'

```    source TEXT DEFAULT 'personal',        -- 'personal' or 'splitwise'

    date TEXT DEFAULT CURRENT_TIMESTAMP    -- 'YYYY-MM-DD'

**Ollama connection errors:**);

```bash```

# Check if Ollama is running

ollama list---



# Restart Ollama service## 🎯 Agentic Behavior Examples

ollama serve

```### Multi-Step Reasoning

**Query:** "Should I be worried about my spending?"

### Frontend Issues

**Agent thinks:**

**Port 5173 already in use:**1. Get total spending this month

```bash2. Compare to last month

# Kill the process or change port in vite.config.js3. Check all budget statuses

```4. Analyze category trends

5. Provide comprehensive assessment

**API connection refused:**

```bash### Proactive Insights

# Verify backend is running on port 8000The agent will volunteer information:

# Check backend terminal for errors- "By the way, you're spending 40% more on weekends"

```- "You've already hit 80% of your Food budget"

- "Your Transportation costs dropped 25% this month - great job!"

### Splitwise Sync Issues

### Context Awareness

**No expenses syncing:**```

- Verify `SPLITWISE_ACCESS_TOKEN` and `MY_USER_ID` in `.env`You: "Set a budget of $500 for food"

- Check you're a participant in the expenses (not just in the group)Agent: "✅ Budget set..."

- API limits to 50 most recent expenses per sync

[Later in conversation]

## 📝 Development NotesYou: "Add $30 dinner"

Agent: "✅ Added... You're now at $470/$500 for your food budget (94%)"

### Running Tests```

```bash

python test.py  # Basic database tests---

```

## 🐛 Troubleshooting

### Adding New Expense Categories

Edit `agent.py` and update the category list in the `add_expense` tool description.### "GROQ_API_KEY not found"

- Make sure you created `.env` file (not `.env.example`)

### Modifying Currency Rates- Verify the key is on the line: `GROQ_API_KEY=gsk_...`

Edit `mappers.py` and update the `CURRENCY_TO_USD` dictionary:

```python### "Import langchain_groq could not be resolved"

CURRENCY_TO_USD = {```powershell

    'USD': 1.0,pip install langchain-groq

    'INR': 0.012,```

    'EUR': 1.10,  # Add more currencies

}### "No module named 'preferences'"

```Make sure all files are in the same directory.



## 🤝 Contributing### Splitwise sync fails

- Check your `SPLITWISE_ACCESS_TOKEN` is correct

Contributions are welcome! Please feel free to submit a Pull Request.- Verify `MY_USER_ID` is set

- Run `python id.py` to get your correct user ID

## 📄 License

---

This project is licensed under the MIT License.

## 🔮 Future Enhancements

## 🙏 Acknowledgments

- [ ] Multi-user support

- Built with [Ollama](https://ollama.ai) for local LLM inference- [ ] Recurring expense tracking

- Agent framework powered by [LangGraph](https://github.com/langchain-ai/langgraph)- [ ] Receipt scanning (OCR)

- UI inspired by [Frappe](https://frappe.io) design principles- [ ] Advanced visualization (charts/graphs)

- Splitwise API for expense synchronization- [ ] Bill splitting suggestions

- [ ] Savings goal tracking

## 📧 Contact- [ ] Export to CSV/Excel

- [ ] Mobile app integration

For questions or feedback, please open an issue on GitHub.

---

---

## 📝 License

**Made with ❤️ for smarter expense tracking**

This project is open source and available for educational purposes.

---

## 🙋 FAQ

**Q: Do I need Ollama?**
A: No! We switched from Ollama to Groq for easier setup and testing.

**Q: Is Groq really free?**
A: Yes! 30 requests/minute on the free tier, perfect for personal use.

**Q: Do I need Splitwise?**
A: No, it's optional. The app works fine tracking only personal expenses.

**Q: Can I use OpenAI instead?**
A: Yes! Just modify `agent.py` to use `ChatOpenAI` instead of `ChatGroq`.

**Q: How is this "agentic"?**
A: It autonomously plans, chains tools, provides proactive insights, and learns from context—not just reacting to commands.

**Q: What LLM model does it use?**
A: Llama 3.1 70B via Groq (excellent for reasoning and SQL generation).

---

## 🤝 Contributing

Feel free to submit issues or pull requests!

---

**Built with ❤️ using LangGraph, Groq, and Gradio**
