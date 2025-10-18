# Smart Pharma Web - Core Workflow Diagram

## System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    SMART PHARMA WEB SYSTEM                      │
│           Medicine Inventory + AI Prescription Assistant        │
└─────────────────────────────────────────────────────────────────┘
```

## Core Workflows

### 1️⃣ Medicine Search & Inventory Management
```
┌──────────┐
│   USER   │
└────┬─────┘
     │
     │ Opens Inventory Page
     ▼
┌─────────────────┐
│  Inventory UI   │
│  (Frontend)     │
└────┬────────────┘
     │
     │ Enter Search Query
     │ (Brand/Generic Name, Filters)
     ▼
┌─────────────────┐
│  Search API     │
│  /api/medicines │
│     /search     │
└────┬────────────┘
     │
     │ Query Database
     ▼
┌─────────────────┐
│  medicines.db   │
│  • Search       │
│  • Filter       │
│  • Sort         │
└────┬────────────┘
     │
     │ Return Results
     ▼
┌─────────────────┐
│  Display List   │
│  • Medicine Info│
│  • Price        │
│  • Availability │
└─────────────────┘
```

### 2️⃣ Prescription Upload & Processing
```
┌──────────┐
│   USER   │
└────┬─────┘
     │
     │ Upload Prescription Image
     ▼
┌─────────────────────┐
│   Upload Page       │
│   (Frontend)        │
└────┬────────────────┘
     │
     │ POST Image File
     ▼
┌─────────────────────┐
│ Prescription Router │
│  /prescription      │
│     /upload         │
└────┬────────────────┘
     │
     │ Process Image
     ▼
┌─────────────────────┐
│   AI Service        │
│  (Google Gemini)    │
│                     │
│  • Extract Text     │
│  • Identify Meds    │
│  • Parse Dosage     │
└────┬────────────────┘
     │
     │ Extracted Medicine Names
     ▼
┌─────────────────────┐
│  Match Medicines    │
│  (Fuzzy Search)     │
│                     │
│  • Search DB        │
│  • Find Matches     │
└────┬────────────────┘
     │
     │ Save Prescription Data
     ▼
┌─────────────────────┐
│ conversation_       │
│   history.db        │
└────┬────────────────┘
     │
     │ Redirect with Data
     ▼
┌─────────────────────┐
│   Chatbot Page      │
│  (Ready to Chat)    │
└─────────────────────┘
```

### 3️⃣ AI Chatbot Interaction
```
┌──────────┐
│   USER   │
└────┬─────┘
     │
     │ Ask Medical Question
     │ (e.g., "What is this medicine for?")
     ▼
┌─────────────────────┐
│   Chatbot UI        │
│   (WebSocket)       │
└────┬────────────────┘
     │
     │ Send Message
     ▼
┌─────────────────────┐
│  Chatbot Router     │
│   /chatbot/ws       │
└────┬────────────────┘
     │
     │ Load Context
     ▼
┌─────────────────────┐
│  Chat Service       │
│                     │
│  • Get History      │
│  • Get Prescription │
│    Context          │
└────┬────────────────┘
     │
     │ Prepare Prompt
     ▼
┌─────────────────────┐
│   AI Service        │
│  (LangChain +       │
│   Google Gemini)    │
│                     │
│  • Process Query    │
│  • Generate Answer  │
└────┬────────────────┘
     │
     │ Need More Info?
     ▼
┌─────────────────────┐
│  Web Search         │
│  (Tavily API)       │
│                     │
│  • Search Web       │
│  • Get Latest Info  │
└────┬────────────────┘
     │
     │ AI Response
     ▼
┌─────────────────────┐
│  Save to History    │
│  conversation_      │
│    history.db       │
└────┬────────────────┘
     │
     │ Send Response
     ▼
┌─────────────────────┐
│  Display in Chat    │
│  (Real-time)        │
└─────────────────────┘
```

## Complete User Journey
```
START
  │
  ▼
┌─────────────────┐
│  Landing Page   │
│  Choose Action  │
└────┬────────────┘
     │
     ├─────────────────────┬─────────────────────┐
     │                     │                     │
     ▼                     ▼                     ▼
┌──────────┐      ┌──────────────┐      ┌──────────────┐
│ Browse   │      │   Upload     │      │   Direct     │
│ Inventory│      │ Prescription │      │   Chatbot    │
└────┬─────┘      └──────┬───────┘      └──────┬───────┘
     │                   │                      │
     │                   │                      │
     ▼                   ▼                      │
┌──────────┐      ┌──────────────┐             │
│ Search & │      │ AI Processes │             │
│  Filter  │      │    Image     │             │
│ Medicines│      └──────┬───────┘             │
└────┬─────┘             │                     │
     │                   │                     │
     │                   ▼                     │
     │            ┌──────────────┐             │
     │            │  Medicines   │             │
     │            │   Matched    │             │
     │            └──────┬───────┘             │
     │                   │                     │
     └───────────────────┴─────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Chatbot    │
                  │  Ask Questions│
                  │  Get Answers  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Get Medical │
                  │  Information │
                  │  & Advice    │
                  └──────────────┘
                         │
                         ▼
                       END
```

## Key Components Interaction
```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Frontend  │◄───────►│   FastAPI   │◄───────►│  Database   │
│  (HTML/JS)  │         │   Backend   │         │  (SQLite)   │
└─────────────┘         └──────┬──────┘         └─────────────┘
                               │
                               │
                               ▼
                        ┌─────────────┐
                        │ AI Services │
                        │             │
                        │ • Gemini    │
                        │ • LangChain │
                        │ • Tavily    │
                        └─────────────┘
```

## Data Flow Summary
```
User Input → Frontend → API → Business Logic → Database
                                      ↓
                                 AI Service
                                      ↓
                              External APIs
                                      ↓
                                  Response
                                      ↓
                                   Frontend
                                      ↓
                                    User
```

## Core Features at a Glance
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. 🔍 SEARCH MEDICINES                                     │
│     └─ Search by brand/generic name                        │
│     └─ Filter by type, dosage, price                       │
│     └─ View detailed information                           │
│                                                             │
│  2. 📄 UPLOAD PRESCRIPTION                                  │
│     └─ Upload image of prescription                        │
│     └─ AI extracts medicine names                          │
│     └─ Auto-match with inventory                           │
│                                                             │
│  3. 💬 AI CHATBOT                                           │
│     └─ Ask questions about medicines                       │
│     └─ Get dosage information                              │
│     └─ Learn about side effects                            │
│     └─ Real-time web search for latest info                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
