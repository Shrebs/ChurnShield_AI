# 🛡️ ChurnShield AI: Enterprise Risk Hub

An interactive, multi-tier full-stack analytics application designed to predict corporate account cancellation risks ("churn"). The system employs a modern hybrid database strategy (SQL + NoSQL) alongside predictive modeling logic to deliver real-time risk simulation and telemetry audit logs.

---

## 🛠️ System Architecture & Data Strategy

The platform is engineered using an enterprise-grade hybrid storage topology to optimize data handling based on structural requirements:

- **Frontend User Interface:** A Single Page Application (SPA) styled with custom dark-mode CSS Grid layouts. It uses asynchronous JavaScript Fetch APIs to update metrics dynamically without full-page reloads.
- **Backend Controller:** Built on Python (Flask Framework) to handle API routing, coordinate dual-database state changes, and process input variables.
- **Relational Storage (SQL):** Managed via **SQLite 3** (`users.db`) to handle rigid, high-integrity relational tables. It holds the active session profile data for authorized system operators.
- **Non-Relational Storage (NoSQL):** Integrated with a cloud **MongoDB Atlas** cluster using BSON document schemas. This functions as a high-speed ingestion sink for streaming unstructured system event logs in real time.
- **Machine Learning Simulation:** Uses algorithmic logic designed to mirror an ensemble Random Forest Classifier, evaluating customer friction points (Support Complaints vs. Application Activity Clicks) into live risk percentages.

---

## 📂 Project Directory Breakdown

```text
churnshield-ai/
│
├── backend/
│   ├── app.py                # Core web service engine & API controllers
│   └── users.db              # Relational engine data file (SQLite)
│
├── frontend/
│   ├── static/
│   │   ├── app.js            # Asynchronous UI handler & event listener
│   │   └── style.css         # Custom responsive dark-mode styling
│   └── templates/
│       └── index.html        # Main presentation template dashboard
│
└── requirements.txt          # Production environment dependency registry

```



##Live Demo Access

You can interact with the live production deployment instantly without running any local code:

1. Click the production URL: **https://churnshield-ai-jdnj.onrender.com/**
2. Look at the top right to see your session profile load securely from the **SQLite relational engine**.
3. Use the **AI Simulation Controls** to adjust customer parameters:
   - Increase **Support Tickets** or drop **App Engagement** to see the system calculate risk states dynamically.
4. Watch the **Live System Audit Trail** update automatically, demonstrating real-time data ingestion pipelines communicating natively with our cloud **MongoDB Atlas** cluster.

---
