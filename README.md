# 📘 arXiv Pedagogy Report Generator

Convert arXiv research papers into structured, student-friendly explanations using Sarvam AI.

This application downloads a research paper from arXiv, extracts its content, and generates a pedagogy-based educational report.

---

## 🧠 What It Does

1. Accepts an arXiv PDF URL  
2. Extracts text from the PDF  
3. Sends content to Sarvam AI (`sarvam-m`)  
4. Returns a structured, easy-to-understand explanation  

---

## 🏗 Architecture

Frontend: Next.js + Tailwind CSS  
Backend: FastAPI  
LLM: Sarvam AI (`sarvam-m`)

```
Frontend (Next.js)
        ↓
FastAPI Backend
        ↓
Sarvam AI API
        ↓
Generated Pedagogy Report
```

---

## 📂 Project Structure

```
paperSummarizer/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── app/
    ├── package.json
    └── tailwind.config.ts
```

---

# 🚀 Backend Setup

## 1️⃣ Create Virtual Environment

### Windows
```
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```
python3 -m venv venv
source venv/bin/activate
```

---

## 2️⃣ Install Dependencies

Inside `/backend`:

```
pip install -r requirements.txt
```

If `uvicorn` is not installed globally:

```
pip install uvicorn
```

If CORS or form handling is required:

```
pip install python-multipart
```

---

## 3️⃣ Environment Variables

Create a `.env` file inside `/backend`:

```
SARVAM_API_KEY=your_api_key_here
```

⚠️ Never commit this file.

---

## 4️⃣ Run Backend

```
uvicorn main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

API documentation available at:

```
http://localhost:8000/docs
```

---

# 🎨 Frontend Setup

Inside `/frontend`:

## 1️⃣ Install Dependencies

```
npm install
```

Install additional packages:

```
npm install react-markdown
npm install @tailwindcss/typography
```

---

## 2️⃣ Run Development Server

```
npm run dev
```

Frontend runs at:

```
http://localhost:3000
```

---

# 📦 Backend Requirements

`backend/requirements.txt`

```
fastapi
uvicorn
requests
python-dotenv
pypdf
```

---

# 📦 Frontend Dependencies

Installed via npm:

```
react-markdown
@tailwindcss/typography
```

# 🌍 Recommended Deployment

Frontend → Vercel  
Backend → Render  

This setup is production-friendly and scalable.

---

# 🛡 Security

- API keys stored in `.env`
- `.env` excluded via `.gitignore`
- Backend handles all API communication
- Frontend never sees secret keys

---
