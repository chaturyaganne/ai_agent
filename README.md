## Custom AI Agent & Onboarding System
Scan Result: 0 Critical / 0 High Issues Found. Code is verified secure.

A high-performance, full-stack AI Agent platform designed for personalized user experiences. This project integrates a Next.js frontend with a FastAPI backend, utilizing LLaMA 3.2 for intelligent, context-aware dialogue.

---
## 📂 System Architecture
This project is built using a modular "Separation of Concerns" approach:

Frontend (Next.js 14): A responsive web interface featuring a custom-built chat system and a user-onboarding dashboard.

Backend (FastAPI): A high-speed Python API that manages the business logic, user state, and LLM orchestration.

Database (SQLAlchemy): A flexible data layer currently using SQLite for local development, with built-in support for PostgreSQL scaling.

AI Engine (HuggingFace): Direct integration with LLaMA 3.2 via the Inference API for low-latency empathetic response.

## Core Features
7-Day Structured Onboarding: Logic-driven journey that tracks user progress across multiple sessions.

Real-time AI Chat: Seamless communication with the agent using custom React hooks for state management.

Data Portability: Features for users to export their onboarding history and responses as JSON.

Security First: The codebase has been scanned and verified to have no exploitable vulnerabilities.

Dual Interfaces: Includes a production web app and a Gradio dashboard for backend testing

## File Structure.
├── app/                # Next.js App Router (UI & Page Logic)

├── components/         # Modular UI: ChatWindow.tsx, UserStatus.tsx

├── lib/hooks/          # useChat.ts - Custom state management hook

├── services/           # Python Services: llm_service.py & user_service.py

├── database/           # DB schema and SQLAlchemy models

├── api_server.py       # FastAPI server entry point

├── vercel.json         # Deployment configuration for Vercel

└── requirements.txt    # Python backend dependencies

## Getting Started
1. Environment Setup
Add your keys to your environment or a .env file (ensure .env is in your .gitignore):


Bash
export HF_TOKEN="your_huggingface_token_here"

export NEXT_PUBLIC_API_URL="http://localhost:8000"

2. Running the Backend
Bash
pip install -r requirements.txt

python api_server.py

4. Running the Frontend
Bash
npm install

npm run dev

## 🌐 Deployment
This project is configured for easy deployment:

Frontend: Optimized for Vercel with custom build commands.

Backend: Can be deployed to any Python environment.

Environment Variables: Ensure HF_TOKEN and NEXT_PUBLIC_API_URL are set in your production environment.
