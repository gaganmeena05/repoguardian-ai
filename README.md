# RepoGuardian AI

AI-powered Pull Request Reviewer using:

- LangChain
- LangGraph
- LlamaIndex
- Ollama
- GitHub API
- FAISS
- Sentence Transformers

---

## Features

- AI PR Reviews
- Repository RAG
- GitHub Review Comments
- Local LLM Support
- Docker Support
- GitHub Actions

---

## Installation

```bash
git clone https://github.com/<username>/repoguardian-ai

cd repoguardian-ai
```

Create virtual environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Install

```bash
pip install .
```

---

## Ollama

Install Ollama

https://ollama.com/

Pull model

```bash
ollama pull qwen2.5-coder:7b
```

Run

```bash
ollama serve
```

---

## Configure

Copy

```
.env.example
```

to

```
.env
```

Fill in

```
GITHUB_TOKEN

GITHUB_OWNER

GITHUB_REPO
```

---

## Build Repository Index

```bash
python main.py --pr 1 --index
```

---

## Review Pull Request

```bash
python main.py --pr 25
```

---

## Review & Post Comment

```bash
python main.py --pr 25 --comment
```

---

## Stack

- Python
- LangChain
- LangGraph
- LlamaIndex
- Ollama
- PyGithub
- FAISS
- Docker
- GitHub Actions

---

## Roadmap

- MCP Server
- Jira Integration
- Confluence Integration
- Multi-Agent Review
- Security Agent
- Test Generation
- Auto Fix Suggestions
