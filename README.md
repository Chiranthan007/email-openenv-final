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

## 🧠 Environment Design

This environment simulates a real-world email filtering system where an agent must classify emails sequentially while maintaining high accuracy.

### Key Features

- Sequential decision-making (not independent classification)
- Mistake tracking with early termination
- Reward shaping based on accuracy and penalties

### Reward Function

- Correct classification → ~0.95+
- Incorrect classification → lower score
- Dynamic shaping:
  - Bonus for higher accuracy
  - Penalty for repeated mistakes
- All rewards strictly in (0,1)

### Episode Termination

- Ends when:
  - All emails processed
  - OR mistake limit reached

### Objective

Maximize long-term accuracy across a stream of emails under constraints.
