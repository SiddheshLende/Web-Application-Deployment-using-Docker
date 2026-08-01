# ⚡ Streamlit Cloud & Python Engineer Portfolio with Automated CI/CD

An end-to-end continuous integration and continuous deployment (CI/CD) pipeline for a Streamlit Python web application. The application is containerized using **Docker**, stored in **Docker Hub**, and automatically deployed onto an **AWS EC2** instance via **GitHub Actions** workflows upon every commit to the `main` branch.

---

## 🏗️ Architecture & Deployment Flow

```text
  ┌──────────────────────┐
  │ Local Dev (VS Code) │
  └──────────┬───────────┘
             │ git push origin main
             ▼
  ┌──────────────────────┐
  │  GitHub Repository   │
  └──────────┬───────────┘
             │ Triggers Workflow
             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 GitHub Actions Runner                  │
  │                                                        │
  │  1. Checkout Code ──► 2. Build Docker Image           │
  │                               │                        │
  │                               ▼                        │
  │                     3. Push to Docker Hub              │
  │                               │                        │
  │                               ▼                        │
  │                     4. SSH into AWS EC2                │
  └───────────────────────────────┬────────────────────────┘
                                  │
                                  ▼
  ┌────────────────────────────────────────────────────────┐
  │                     AWS EC2 Server                     │
  │                                                        │
  │  1. Pull latest image from Docker Hub                  │
  │  2. Stop & remove existing container                   │
  │  3. Run new container (-p 80:8501)                      │
  └───────────────────────────────┬────────────────────────┘
                                  │
                                  ▼
                   ┌──────────────────────────────┐
                   │   Live App (HTTP Port 80)    │
                   └──────────────────────────────┘
```

---

## 🛠️ Tech Stack

* **Application Framework:** Python 3.11, Streamlit
* **Containerization:** Docker, Docker Hub
* **CI/CD Pipeline:** GitHub Actions
* **Cloud Infrastructure:** AWS EC2 (Ubuntu 22.04 LTS)
* **Version Control:** Git, GitHub
* **Development Environment:** VS Code

---

## 📂 Project Structure

```text
Portfolio Website/
├── .github/
│   └── workflows/
│       └── deployment.yml      # GitHub Actions CI/CD pipeline definition
├── app.py                      # Main Streamlit portfolio application
├── Dockerfile                  # Instructions for building the container image
├── .dockerignore               # Files excluded from the Docker context
├── .gitignore                  # Files excluded from Git tracking
└── requirements.txt            # Python dependencies
```

---

## 📋 Step-by-Step Setup Guide

### 1. Application Files Setup

* **`requirements.txt`**
  ```text
  streamlit>=1.30.0
  ```

* **`Dockerfile`**
  ```dockerfile
  FROM python:3.11-slim

  ENV PYTHONDONTWRITEBYTECODE=1
  ENV PYTHONUNBUFFERED=1

  WORKDIR /app

  RUN apt-get update && apt-get install -y --no-install-recommends       build-essential       && rm -rf /var/lib/apt/lists/*

  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  COPY . .

  EXPOSE 8501

  CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
  ```

---

### 2. AWS EC2 Instance Configuration

1. **Launch Instance:**
   * OS: **Ubuntu 22.04 LTS**
   * Instance Type: `t2.micro` (Free Tier)
   * Key Pair: Save `.pem` private key securely.

2. **Inbound Security Group Rules:**
   * **HTTP (Port 80):** `0.0.0.0/0` (Allows web visitors)
   * **Custom TCP (Port 8501):** `0.0.0.0/0` (Optional direct Streamlit port)
   * **SSH (Port 22):** `0.0.0.0/0` (Allows terminal administration)

3. **Install Docker on EC2:**
   SSH into EC2 and run:
   ```bash
   sudo apt-get update -y
   sudo apt-get install -y docker.io
   sudo systemctl enable --now docker
   ```

---

### 3. GitHub Repository Secrets Setup

Navigate to **GitHub Repository** ➔ **Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **New repository secret** and add:

| Secret Name | Description / Value |
| :--- | :--- |
| `DOCKERHUB_USERNAME` | Your Docker Hub account username |
| `DOCKERHUB_TOKEN` | Docker Hub Personal Access Token |
| `EC2_HOST` | AWS EC2 Public IPv4 address |
| `EC2_USERNAME` | `ubuntu` |
| `EC2_SSH_KEY` | Entire content of your downloaded `.pem` key file |

---

### 4. GitHub Actions CI/CD Workflow (`.github/workflows/deployment.yml`)

```yaml
name: CI/CD Deployment Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/my-python-app:latest

      - name: Deploy to EC2 via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            sudo systemctl start docker
            sudo docker login -u "${{ secrets.DOCKERHUB_USERNAME }}" -p "${{ secrets.DOCKERHUB_TOKEN }}"
            sudo docker stop portfolio-app || true
            sudo docker rm portfolio-app || true
            sudo docker pull ${{ secrets.DOCKERHUB_USERNAME }}/my-python-app:latest
            sudo docker run -d --name portfolio-app --restart always -p 80:8501 ${{ secrets.DOCKERHUB_USERNAME }}/my-python-app:latest
```

---

## 💻 Essential Commands Reference

### Local Git Development (VS Code Terminal)

```powershell
# Create proper workflow directory layout
New-Item -ItemType Directory -Path ".github\workflows" -Force

# Stage changes
git add .

# Commit changes
git commit -m "Configure automated CI/CD pipeline"

# Push to trigger deployment workflow
git push origin main
```

### Server Diagnostics (AWS EC2 SSH Terminal)

```bash
# Check active running containers
sudo docker ps

# View real-time container output logs
sudo docker logs portfolio-app

# Test application availability locally on server
curl -I http://localhost
```

---

## 🌐 Application Access

Once the GitHub Action completes successfully (indicated by a green checkmark in the **Actions** tab), access the website at:

`http://<YOUR_EC2_PUBLIC_IP>`