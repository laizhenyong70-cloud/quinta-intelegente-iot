# 🐷 IoT-Based Smart Farm Monitoring System

A complete end-to-end IoT monitoring system for smart agriculture, integrating data simulation, real-time communication, backend processing, storage, and visualization.

This project demonstrates the design of a distributed data pipeline using MQTT, with a focus on real-time data acquisition and system integration.

---

## Features

- Real-time sensor data simulation (temperature, humidity, NH3)
- MQTT-based communication using EMQX broker
- Backend processing with Python (Flask)
- Data storage using SQLite
- RESTful API for data access
- Frontend visualization (real-time + historical data)

---

## System Architecture
Simulator → MQTT Broker (EMQX) → Backend (Flask) → SQLite Database → API → Frontend

---

## Tech Stack

- **MQTT Broker**: EMQX (Docker)
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Frontend**: HTML + JavaScript (Chart.js)
- **Environment**: Linux (WSL), VS Code

---

## Project Structure
quinta_intelegente/
│
├── server/
│ ├── app.py # Flask application
│ ├── database.py # Database operations
│
├── simulator/
│ └── simulator.py # MQTT data simulator
│
├── data/
│ └── app.db # SQLite database (ignored in Git)
│
├── frontend/
│ ├── index.html
│ ├── app.js
│
└── README.md

---

## How to Run

1. Start MQTT Broker (EMQX via Docker)

```bash
docker run -d --name emqx -p 1883:1883 emqx/emqx
2. Run Simulator
    python3 simulator/simulator.py
3. Run Backend
    python3 server/app.py
4. Run service
    python3 server/service.py
5. Open Fronted
    Open index.html

Example Data
{
  "sensor_id": "SN-0001",
  "temperature": 28.5,
  "humidity": 65.2,
  "nh3": 12.3,
  "status": "normal",
  "timestamp": "2026-03-31 10:00:00"
}
Project Motivation

    With my background in embedded systems and IoT product development, I developed this project to transition towards software engineering and distributed systems.

    This system reflects real-world scenarios where hardware devices communicate with backend systems through lightweight protocols like MQTT.

Future Improvements

    Deploy backend to cloud (e.g., AWS / Azure)
    Replace SQLite with PostgreSQL
    Add authentication & user management
    Real-time dashboard using WebSocket
    Integration with real IoT devices


