---

title: Email OpenEnv Environment
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 📧 Email Classification OpenEnv Environment

## 🧠 Overview

This project implements a real-world OpenEnv environment for email triage where an AI agent classifies emails as spam or not_spam.

## ▶️ Running

python inference.py

## 🐳 Docker

docker build -t email-env .
docker run -p 8000:8000 email-env
