# 🔥 ContentForge — AI Content Generator

> **Forge your content with AI. Powerfully.**

ContentForge is a free, open-source Streamlit application that generates high-quality content — blogs, emails, social media posts, product copy, and more — powered by ultra-fast cloud inference via the **Groq API**.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-Powered-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Multi-format Content** | Blog posts, emails, social media, product descriptions, newsletters, and more |
| **Multiple AI Models** | Choose from GPT-OSS 20B, GPT-OSS 120B, Qwen 27B, or Allam 7B |
| **Rewrite & Enhance** | Make content shorter, longer, improve grammar, or SEO-optimize |
| **Template Library** | Pre-built templates + create your own custom templates |
| **Export Options** | Export to TXT, DOCX, or PDF with metadata |
| **Generation History** | Full history with search, filter, and statistics |
| **Session Favorites** | Save your best outputs during a session |

---

## 🚀 Quick Start

### 1. Get a Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (Google/GitHub login supported)
3. Navigate to **API Keys** → **Create API Key**
4. Copy your key

### 2. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/ContentForge-AI-content-generator.git
cd ContentForge-AI-content-generator
```

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_api_key_here
```

### 4. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🤖 Available Models

| Display Name | Groq Model ID | Best For |
|-------------|---------------|----------|
| **gpt-oss-20b** | `openai/gpt-oss-20b` | Fast, general-purpose (recommended) |
| **gpt-oss-120b** | `openai/gpt-oss-120b` | Complex reasoning, high-quality output |
| **qwen-27b** | `qwen/qwen3.8-27b` | Balanced speed and quality |
| **allam-7b** | `allam-2-7b` | Lightweight, quick tasks |

> Models are subject to Groq's availability. Check [console.groq.com/docs/models](https://console.groq.com/docs/models) for the latest list.

---

## 📁 Project Structure

```
ContentForge/
├── app.py              # Streamlit UI and page routing
├── generator.py        # Groq API content generation engine
├── prompts.py          # Prompt templates and content analyzer
├── db.py               # SQLite database for history and templates
├── settings.py         # Settings and session memory management
├── templates.py        # Pre-built template library
├── export_utils.py     # TXT, DOCX, PDF export functionality
├── requirements.txt    # Python dependencies
├── settings.json       # Persisted user settings
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
└── OUTPUT/             # Screenshots
```

---

## 🖥️ Deploying to Hugging Face Spaces

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces) with **Streamlit** SDK
2. Push your code to the Space repo
3. Add `GROQ_API_KEY` as a **Secret** in Space Settings → Variables and Secrets
4. The app will auto-deploy

> **Do NOT** commit your `.env` file. The `.gitignore` already excludes it.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io)
- **LLM Inference:** [Groq API](https://groq.com) (ultra-fast cloud inference)
- **Database:** SQLite (zero-config, file-based)
- **Export:** python-docx, ReportLab (PDF)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
