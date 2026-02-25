🌦️ Python Weather App — Flask • Docker • Redis • Prometheus • Grafana • Azure Ready
📌 Project Overview

This project is a production-style, containerized Python Flask Weather Application enhanced with:

Redis caching

Prometheus monitoring

Grafana visualization

Docker multi-container orchestration

Azure-ready deployment structure

It demonstrates how a simple Python app evolves into a full DevOps monitoring stack.

🧩 Architecture Overview
GitHub
  ↓
Docker Image
  ↓
Docker Compose
  ↓
Flask Application  ←→  Redis Cache
  ↓
Azure Container Platform

Key Architecture Highlights

Flask app runs inside a Docker container

Redis is used for caching weather API responses

Docker Compose orchestrates multi-container setup

Redis data is persisted using Docker named volumes

Application exposed on port 80 (production-style)

🚀 Features

🌍 Fetches real-time weather data by city name

⚡ Caches API responses using Redis for performance

🐳 Fully containerized using Docker

🔁 Multi-container orchestration with Docker Compose

☁️ Cloud-ready deployment architecture for Azure

🔐 Secure API key handling via environment variables

🛠️ Technologies Used

Python

Flask

Redis

Docker

Docker Compose

GitHub

Azure (Container-based deployment)

OpenWeatherMap API

📚 What I Learned

Containerizing existing applications using Docker

Multi-container orchestration with Docker Compose

Using Redis for caching and performance optimization

Managing persistent data with Docker volumes

Environment variable–based secret management

Preparing containerized apps for cloud deployment

Debugging real-world Docker and pipeline issues

▶️ How to Run the Project Locally
1️⃣ Clone the Repository
git clone https://github.com/tanvishinde017/Python-Weather-App.git
cd Python-Weather-App

2️⃣ Create Environment File

Create a .env file:

OPENWEATHER_API_KEY=your_api_key_here
REDIS_HOST=redis
REDIS_PORT=6379


⚠️ Do not commit .env to GitHub. Use .env.example instead.

3️⃣ Run Using Docker Compose
docker compose up --build

4️⃣ Access the Application

Open browser:

http://localhost

📦 Docker Compose Services

web → Flask weather application

redis → Redis cache with persistent storage

🔗 Project Links

🔹 GitHub Repository
https://github.com/tanvishinde017/Python-Weather-App

🔹 OpenWeatherMap API
https://openweathermap.org/api

🧠 Future Improvements

Kubernetes deployment (AKS)

CI/CD pipeline automation

Centralized logging and monitoring

Rate limiting and caching strategies

Secrets management using Azure Key Vault

✨ Key Takeaway

This project demonstrates how a simple Python application can be evolved into a production-ready, containerized system by applying real-world DevOps principles such as automation, scalability, and reliability.

Developer
   ↓
Push Code to GitHub
   ↓
Docker Build
   ↓
Docker Compose
   ↓
-------------------------------------------------
|                                               |
|  Flask Weather App  ←→  Redis Cache          |
|         |                                     |
|         | exposes /metrics                    |
-------------------------------------------------
                ↓
          Prometheus
      (scrapes metrics every 15s)
                ↓
      Time-Series Database
                ↓
            Grafana
     (visualizes metrics)
                ↓
        Monitoring Dashboard
                ↓
      Ready for Azure Deployment