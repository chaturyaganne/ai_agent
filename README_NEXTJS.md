# Anton - AI Companion for Hytribe

A modern AI companion application built with Next.js and powered by LLaMA 3.2.

## Features

- 🤖 **AI-Powered Conversations** - Empathetic AI responses powered by LLaMA 3.2
- 📊 **7-Day Onboarding** - Structured onboarding journey with daily check-ins
- 💾 **Data Export** - Export your onboarding responses as JSON
- 🎨 **Modern UI** - Built with React, Next.js, and Tailwind CSS
- ⚡ **Fast & Scalable** - Optimized for Vercel deployment
- 🔒 **Privacy-First** - User data stored locally in SQLite (upgradeable to PostgreSQL)

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **Tailwind CSS** - Styling
- **TypeScript** - Type safety

### Backend
- **FastAPI** - Python web framework
- **HuggingFace Hub** - LLM API integration
- **SQLAlchemy** - Database ORM
- **SQLite/PostgreSQL** - Data storage

## Getting Started

### Prerequisites
- Node.js 18+ (for Next.js)
- Python 3.10+ (for backend)
- HuggingFace API token (get one from https://huggingface.co/settings/tokens)

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/chaturyaganne/ai_agent.git
   cd ai_agent
   ```

2. **Set up environment variables**
   ```bash
   export HF_TOKEN="your_huggingface_token_here"
   export NEXT_PUBLIC_API_URL="http://localhost:8000"
   ```

3. **Install dependencies**
   ```bash
   npm install
   pip install -r requirements.txt
   ```

### Running Locally

**Terminal 1 - Backend API Server**
```bash
python api_server.py
# Server starts at http://localhost:8000
```

**Terminal 2 - Frontend Development Server**
```bash
npm run dev
# App available at http://localhost:3000
```

## Project Structure

```
.
├── app/                    # Next.js App Router
│   ├── api/               # API routes
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── ChatWindow.tsx     # Main chat interface
│   └── UserStatus.tsx     # User progress sidebar
├── lib/                   # Utilities and hooks
│   └── hooks/
│       └── useChat.ts     # Chat state management
├── services/              # Python services
│   ├── llm_service.py     # LLM integration
│   └── user_service.py    # User management
├── database/              # Database models
│   ├── db.py
│   └── models.py
├── api_server.py          # FastAPI backend
├── package.json           # Node dependencies
├── requirements.txt       # Python dependencies
└── vercel.json           # Vercel deployment config
```

## Deployment

### Deploy to Vercel

1. **Push to GitHub**
   ```bash
   git push origin nextjs-vercel
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com
   - Click "New Project"
   - Select your GitHub repo
   - Add environment variables:
     - `HF_TOKEN` - Your HuggingFace token
     - `NEXT_PUBLIC_API_URL` - Backend URL (for production)

3. **Backend Deployment** (separate from frontend)
   - Backend should be deployed separately (e.g., on Railway, Render, or your own server)
   - Update `NEXT_PUBLIC_API_URL` to point to your backend

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HF_TOKEN` | ✅ | HuggingFace API token for LLM |
| `NEXT_PUBLIC_API_URL` | ✅ | Backend API URL (frontend only) |
| `DATABASE_URL` | ❌ | PostgreSQL URL (optional, uses SQLite by default) |

## API Endpoints

### Chat
- `POST /api/chat` - Send a message and get response

### User
- `GET /api/user` - Get user status and progress
- `POST /api/user/message` - Process user message
- `POST /api/user/mark-complete` - Mark day as complete
- `POST /api/user/export` - Export user data as JSON

## Development

### Running Tests
```bash
npm run test
```

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ for Hytribe
