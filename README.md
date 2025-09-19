---
title: "Intelligent Issue Triage"
emoji: "🤖"
colorFrom: "indigo"
colorTo: "purple"
sdk: "docker"
app_port: 7860
pinned: false
---

# Intelligent GitHub Issue Triage System 🤖

An AI-powered bot that automatically classifies and labels new GitHub issues using a state-of-the-art NLP model. This project demonstrates a full end-to-end MLOps pipeline, from data collection and model training to a deployed, automated application.

---

## 🚦 Live Demo & Status

**The live API for this project is deployed on Hugging Face Spaces.**

* **Live API Endpoint:** https://khush25-issue-triage-api.hf.space
* **Interactive Docs:** Visit https://khush25-issue-triage-api.hf.space/docs to test the API live in your browser.
* **Project Status:** ✅ Complete and Deployed.

---

## 🚀 Features

- **Automated Labeling:** Automatically applies one of four labels (`bug`, `enhancement`, `documentation`, `question`) to new issues.
- **High-Performance Data Pipeline:** Uses the GitHub GraphQL API to build a custom dataset from multiple large-scale repositories.
- **Modern AI Model:** Fine-tuned a `microsoft/deberta-v3-base` transformer model, achieving a **weighted F1-score of ~0.84** on the classification task.
- **API-Driven:** The model is served via a high-performance FastAPI application deployed in a Docker container.
- **Fully Automated Workflow:** A GitHub Action integrates the system directly into any repository's workflow.

---

## 🛠️ Tech Stack

- **AI/ML:** PyTorch, Hugging Face (`transformers`, `datasets`)
- **Data Pipeline:** Python, Pandas, GraphQL, Requests
- **Backend API:** FastAPI, Uvicorn
- **Deployment:** Hugging Face Spaces, Docker, Git LFS
- **Automation:** GitHub Actions

---

## 🏛️ Architecture

The system uses a modern, event-driven architecture:

`New GitHub Issue` -> `GitHub Action (Trigger)` -> `FastAPI on HF Spaces (Prediction)` -> `GitHub API (Apply Label)`

1. A user creates a new issue in a repository.
2. A GitHub Action workflow is triggered automatically.
3. The Action sends the issue's title and body to the live FastAPI endpoint deployed on Hugging Face Spaces.
4. The FastAPI app uses the fine-tuned DeBERTa model to predict the correct label.
5. The API returns the predicted label to the GitHub Action.
6. The Action uses the GitHub API to apply the predicted label to the original issue.

---

## ⚙️ Setup and Usage (Local)

To run this project on your local machine:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Khush-Ojha/GIT-intelligent-issue-triage.git
    cd GIT-intelligent-issue-triage
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the project root and add your GitHub Personal Access Token:
    ```
    GITHUB_TOKEN=ghp_YourTokenHere
    ```

5. **Run the FastAPI server:**
    ```bash
    uvicorn app:app --reload
    ```
    The server will be available at `http://127.0.0.1:8000`.

---

## 📈 Results

The fine-tuned DeBERTa-v3 model achieved a weighted **F1-score of 0.837** on the validation set, demonstrating a strong ability to classify complex, real-world GitHub issues.