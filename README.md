# Saarthi 🤝

### An AI companion built for honest, grounded conversations.

Saarthi is a full-stack AI companion application designed to give people a private space to talk through everyday challenges — such as job-search stress, personal struggles, uncertainty, or simply feeling stuck.

The goal is not to simulate a therapist or provide clinical advice. Saarthi is designed around **short, grounded, human-like conversations** that help users think through what they are experiencing without being preachy or overly generic.

> **Saarthi** means "guide" or "companion" in Hindi/Sanskrit.

---

## ✨ Features

### 🤖 AI-Powered Conversations

* Powered by **Groq's LLaMA 3.3 API**
* Custom system prompting for concise, grounded responses
* Designed to avoid overly verbose, generic, or motivational responses
* Maintains conversational context

### 🧠 Persistent Conversation Memory

* Conversations are persisted in **PostgreSQL**
* Users can continue conversations across sessions
* Conversation history is retrieved from the database to maintain context

### 🔐 Secure Multi-User Authentication

* JWT-based authentication
* Password hashing using **bcrypt**
* User-specific conversation isolation
* Protected API endpoints

### 🛡️ Safety Detection

Saarthi includes a dedicated safety-detection layer rather than relying exclusively on the language model.

The application can identify potentially sensitive inputs and route them through an appropriate support flow instead of treating every message as a normal AI conversation.

### 💬 WhatsApp-Inspired Chat Interface

* React-based interface
* Chat bubbles
* Typing indicators
* Automatic scrolling
* Responsive conversation experience

---

## 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  React + Vite    │
                         │    Frontend      │
                         └────────┬─────────┘
                                  │
                              REST API
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │     Backend      │
                         └───────┬──────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌────────────┐     ┌─────────────┐    ┌─────────────┐
       │    JWT     │     │   Safety    │    │  PostgreSQL │
       │    Auth    │     │   Layer     │    │  + SQLAlchemy│
       └────────────┘     └──────┬──────┘    └─────────────┘
                                 │
                                 ▼
                         ┌──────────────────┐
                         │   Groq API       │
                         │   LLaMA 3.3      │
                         └──────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* SQLAlchemy
* REST APIs

### Database

* PostgreSQL

### AI

* Groq API
* LLaMA 3.3

### Authentication & Security

* JWT
* bcrypt
* Protected API routes
* User-specific data isolation

### Deployment

* Vercel
* Render

---

## 📁 Project Structure

```text
saarthi/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── database/
│   └── main.py
│
├── .gitignore
├── README.md
└── ...
```

> Project structure may vary depending on the current implementation.

---

## 🔐 Authentication Flow

```text
User
 │
 ▼
Register / Login
 │
 ▼
Password → bcrypt hash
 │
 ▼
JWT generated
 │
 ▼
Authenticated API requests
 │
 ▼
User-specific conversations
```

Passwords are never stored as plaintext.

JWT authentication is used to protect backend endpoints and associate conversations with the authenticated user.

---

## 🧠 Conversation Flow

```text
User sends message
        │
        ▼
Authentication validation
        │
        ▼
Safety detection
        │
        ├──────── Sensitive ────────► Support response
        │
        ▼
Retrieve conversation context
        │
        ▼
Groq / LLaMA 3.3
        │
        ▼
Generate response
        │
        ▼
Persist conversation
        │
        ▼
Return response to frontend
```

---

## 🗄️ Data Persistence

Saarthi uses PostgreSQL to persist application data and conversation history.

The backend uses SQLAlchemy as the ORM layer.

At a high level:

```text
User
 │
 └──► Conversations
          │
          └──► Messages
```

This allows conversations to remain available across sessions while keeping user data logically isolated.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

* Python 3.x
* Node.js
* PostgreSQL
* A Groq API key

---

### 1. Clone the repository

```bash
git clone https://github.com/rohanhosamane/saarthi.git

cd saarthi
```

---

### 2. Backend setup

```bash
cd backend

python -m venv venv
```

Activate the virtual environment.

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_groq_api_key
```

Never commit your `.env` file.

A `.env.example` file should be included in the repository to document the required configuration.

---

### 4. Start the backend

```bash
uvicorn main:app --reload
```

The API will be available locally through the configured FastAPI server.

FastAPI's interactive API documentation can be accessed through:

```text
/docs
```

---

### 5. Start the frontend

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

The React development server will provide the frontend application locally.

---

## 🧪 Testing

Testing is an important part of the project and the backend can be tested independently from the frontend.

```bash
pytest
```

> Add the exact test command and coverage information here once the test suite is finalized.

---

## 🌐 Deployment

The application is designed as a separated frontend/backend architecture.

```text
React + Vite
     │
     ▼
  Vercel

FastAPI
     │
     ▼
  Render
     │
     ▼
PostgreSQL
```

Environment-specific secrets are kept outside the source code.

---

## 🔒 Security Considerations

Saarthi was designed with several security considerations:

* Password hashing using bcrypt
* JWT-based authentication
* Protected API endpoints
* User-specific conversation access
* Environment variables for secrets
* Separation of frontend and backend
* Dedicated safety-detection logic

### Important

Saarthi is **not a medical or clinical service** and should not be treated as a replacement for professional mental-health care or emergency services.

---

## 🎯 Engineering Challenges

### Maintaining conversation context

An AI companion becomes significantly less useful if every conversation starts from zero.

Saarthi therefore persists conversation history and retrieves relevant context when generating responses.

### Separating safety handling from generation

Safety-critical behavior should not depend entirely on the language model.

A separate detection layer provides an additional control point before the request reaches the normal conversation flow.

### Multi-user data isolation

Because conversations can contain private information, authentication and user-specific database queries are used to ensure one user's conversations are not exposed to another user.
---

## 🔮 Future Improvements

* Streaming AI responses
* Improved conversation summarization
* More granular safety classifications
* Rate limiting
* Better observability and logging
* Automated testing and CI/CD
* Improved conversation search
* User-controlled memory
* More robust prompt evaluation
* Production monitoring

---

## 👨‍💻 Author

**Rohan Hosamane**

AI Engineer | GenAI, LLMs & RAG | Python Backend | Full-Stack Development

📧 [rohanhosamane4252@gmail.com](mailto:rohanhosamane4252@gmail.com)

🔗 LinkedIn: [www.linkedin.com/in/hosamane-h-rohan-10b0ab209](http://www.linkedin.com/in/hosamane-h-rohan-10b0ab209)

💻 GitHub: github.com/rohanhosamane

---

## ⭐ If you found Saarthi interesting

Feel free to explore the repository, open an issue, or suggest improvements.
