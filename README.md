# 🤖 HR Chacha: AI-Powered Hiring Assistant

&#x20;  &#x20;

> **HR Chacha** is an AI-powered hiring assistant chatbot built using **Streamlit**, **Groq-hosted LLMs**, **MongoDB** and deployed with **AWS ECR + EC2**. It simulates an intelligent recruiter that collects candidate details, asks technical questions based on their skills, and formats their data into a clean JSON format for HR/admins to evaluate.

AWS Deployment: Deployment has been paused.

---

## 📌 Project Overview

**HR Chacha** is a conversational AI assistant built for recruitment automation. It:

* Greets candidates professionally
* Collects basic candidate info (name, email, experience, location, tech stack)
* Dynamically generates tech-specific questions (e.g., Python, Django)
* Accepts candidate answers, stores data in MongoDB
* Outputs final structured data for HR teams to assess

---
## Screenshots
![Home Page](assets/screenshots/ss1.png)
![Home Page](assets/screenshots/ss2.png)
![Home Page](assets/screenshots/ss3.png)
___



## 🚀 Installation Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Phantom-VK/HRChacha.git
cd HRChacha
```

### 2. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Use Python 3.12

```bash
uv python install 3.12
```

### 4. Setup environment

```bash
uv sync --locked
```

This creates a project-managed virtual environment at `.venv` from `pyproject.toml` and `uv.lock`.

### 5. Environment Variables

Create a `.env` file:

```env
MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/
GROQ_API_KEY=your_groq_api_key_here
```

### 6. Run the app

```bash
uv run streamlit run app.py
```

### 7. Docker build

The Docker image now installs dependencies from `uv.lock`, so local uv and container environments resolve from the same lockfile.

---

## 📖 Usage Guide

1. Open your browser to `http://localhost:8501`
2. Start chatting! HR Chacha will ask for your name, email, experience, and skills
3. Based on your tech stack, HR Chacha will generate 3-5 relevant questions
4. Once all answers are received, your structured JSON will be shown and saved to MongoDB

---

## ⚙️ Technical Details

### 🧱 Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **Python version**: 3.12
* **LLM API**: Groq
* **Database**: MongoDB Atlas
* **Deploymet**: Github Workflow, Runners, Docker,  AWS ECR, AWS EC2
* **Prompt Management**: Custom, static system prompt with extract logic

### 📦 Libraries Used

* `streamlit`
* `pymongo`
* `python-dotenv`
* `groq`

### 🧠 LLM Architecture

* Uses chat history and a persistent `system` role
* Messages streamed with cursor-style output
* Structured prompt instructs LLM to collect & serialize user data

---

## 🎯 Prompt Design

Prompting strategy follows best practices:

* Starts with a clear role definition
* Instructionally structured in numbered format
* Uses trigger phrase `USER_DATA` to tag final JSON output
* Prompts candidate to answer tech questions with number and answer pairing
* Handles irrelevant input with fallback behavior

> See the full prompt in [`hrchacha/prompts`](./hrchacha/prompts/__init__.py)

---


## 📦 CI/CD & Deployment

* **Docker**: for containerized development and deployment
* **GitHub Actions**: to automate test and deployment workflows
* **AWS EC2 / ECR**: for cloud hosting + storing image
* **Environment management**: `uv`

```mermaid
graph TD;
  Dev-->GitHub;
  GitHub-->CI/CD;
  CI/CD-->Docker;
  Docker-->AWS;
  AWS-->Production;
```

---

## 👨‍💻 Author

* 👤 **Vikramaditya Khupse**
  Final Year IT | ML + Fullstack | Building real-world solutions
