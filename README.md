# Saarthi 🤝

Saarthi is a full-stack AI companion chat application built to give people a space to talk through real problems — job search stress, personal struggles, or just feeling stuck — with a grounded, real, non-clinical tone.

Saarthi means "guide" or "companion" in Hindi/Sanskrit.

## Features

- **Real-time AI chat** powered by Groq's LLaMA 3.3 API, with a custom-tuned system prompt for short, honest, non-preachy responses
- **Persistent memory** — conversations are stored in PostgreSQL, so Saarthi remembers context across sessions instead of resetting
- **Secure multi-user auth** — JWT-based register/login with bcrypt password hashing; each user's chat history stays private and isolated
- **Safety-detection layer** — flags sensitive user input and responds with appropriate support resources instead of relying on the LLM alone
- **WhatsApp-style chat UI** — built in React with real-time bubbles, typing indicators, and auto-scroll

## Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy, Groq API, JWT, bcrypt
**Frontend:** React, Vite

## Architecture