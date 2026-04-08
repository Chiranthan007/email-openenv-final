# 📧 Email Classification OpenEnv Environment

## 🧠 Overview

This project implements a real-world OpenEnv environment for **email triage**, where an AI agent classifies emails as:

* spam
* not_spam

The environment simulates practical systems like spam filters, phishing detection, and inbox prioritization.

---

## 🎯 Objective

The agent must correctly classify emails across three difficulty levels:

* Easy → obvious spam vs normal emails
* Medium → promotional vs transactional emails
* Hard → subtle phishing detection

---

## 🧩 Environment Design

### Observation Space

EmailObservation:

* email: str
* step_count: int

### Action Space

EmailAction:

* label: str  ("spam" or "not_spam")

### Reward Space

EmailReward:

* score: float  (0.0 to 1.0)

---

## ⚙️ Environment API

The environment follows the OpenEnv specification:

* reset(task_id) → initializes environment
* step(action) → returns (observation, reward, done, info)
* state() → returns current internal state

---

## 🧪 Tasks

Defined in app/tasks.py with increasing difficulty:

* Easy → clear spam keywords
* Medium → contextual classification
* Hard → phishing-like ambiguity

---

## ⚖️ Reward Function

Implemented in app/graders.py:

* 1.0 → correct classification
* 0.3 → valid label but incorrect
* 0.0 → invalid output

This provides dense reward signals across the full trajectory.

---

## 🤖 Baseline Inference

The inference.py script:

* Uses OpenAI client interface
* Runs all tasks (easy, medium, hard)
* Logs output in required format: [START], [STEP], [END]

Fallback logic ensures reproducibility without API access.

---

## ▶️ Running Locally

python inference.py

---

## 🐳 Docker

docker build -t email-env .
docker run email-env

---

## 📦 Requirements

* Python 3.10+
* pydantic
* openai

---

## 📌 Notes

* Deterministic baseline results
* Fully OpenEnv compliant
* Designed for evaluating agent reasoning across difficulty levels

---

## 🚀 Motivation

Email classification is a core real-world AI task. This environment provides a structured benchmark for evaluating:

* spam detection
* phishing awareness
* contextual reasoning

---

## 🏁 Status

* OpenEnv compliant
* Dockerized
* Baseline inference implemented
* Ready for submission
