# ExpMantenibilidad2

**A Django-based microservices system implementing bulkhead isolation and read/write separation, deployed on Google Cloud Platform.**

Developed as part of *ISIS2503 – Arquitectura y diseño de software* at Universidad de los Andes, this project explores scalable service architecture through a distributed, cloud-deployed medical records system.

[📽️ Watch the project demo (Spanish)](https://youtu.be/RImE-6kuCwk)

---

## ✨ Overview

This system consists of loosely coupled Django services that reflect common real-world architectural patterns for resilience and scalability:

* **Bulkhead Isolation** – Failures in one service don’t propagate across the system.
* **Read/Write Separation** – Optimized performance and data access through independent services and databases.
* **Cloud Deployment** – Services deployed on GCP with startup automation and role-based configuration.

Though designed as an academic experiment, the project emulates production-like environments with role-based microservices, independent deployment pipelines, and flexible runtime control over service behavior.

---

## 🧩 Architecture

The system is composed of three main services, each running on its own GCP VM and configured independently via environment variables:

| Role       | Description                                                             |
| ---------- | ----------------------------------------------------------------------- |
| `bulkhead` | Routes requests and controls GET/POST availability via runtime toggles. |
| `write`    | Accepts and stores new medical entries.                                 |
| `read`     | Serves paginated and filtered medical records to clients.               |

Each service exposes REST endpoints, health checks, and is initialized with pre-loaded medical data for demonstration.

**Example Endpoints:**

* `POST /bulkhead/toggle/` – Control read/write access dynamically.
* `GET /database/read/` – Query medical data (on read servers).
* `POST /database/write/` – Add entries (on write servers).

---

## 🛠 Tech Stack

* **Django 4.2** + **Django REST Framework** – Rapid API development with strong modularity.
* **Python 3.8+**
* **Google Cloud Platform**

  * Compute Engine VMs per service
  * Firewall configuration and startup scripts
* **Linux (Debian 11)**
* **Git** – Version control and collaboration

---

## 🗂 Project Structure

```
ExpMantenibilidad2/
├── bulkhead/               # Routing and availability logic
├── database/               # Read/write microservices
├── deployment.yaml         # GCP deployment spec
├── populate_db.py          # Sample data generator
├── requirements.txt
└── ...
```

---

## 🚀 Cloud Deployment

Each service VM is provisioned using a declarative `deployment.yaml` file. Startup scripts:

* Install dependencies
* Clone the repo
* Set environment variables (`SERVER_TYPE`, `WRITE_DB_IP`, `READ_DB_IP`)
* Run migrations and seed sample data
* Start the Django server

This setup supports reproducible deployments, modular development, and fault-isolated service upgrades.

---

## 🧪 Local Testing (Optional)

While the system was designed for a cloud environment, it can also be run locally:

```bash
pip install -r requirements.txt
export SERVER_TYPE=write  # or read / bulkhead
python manage.py migrate
python populate_db.py
python manage.py runserver
```

---

## 📦 Models

* `WriteData` / `ReadData`: Distinct models for logical data separation
* `ServiceStatus`: Runtime service toggling metadata for bulkhead control

---

## 🧪 Tests

```bash
python manage.py test
```

---

## 🎯 Final Notes

This project is a practical demonstration of scalable service design, deployment automation, and runtime flexibility using Python and cloud-native tools. While simple in scope, the architectural decisions reflect principles found in production systems—emphasizing separation of concerns, failure containment, and adaptable infrastructure.

---

Let me know if you'd like a version in Spanish or one tailored more toward a portfolio website layout.
