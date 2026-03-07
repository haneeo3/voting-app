# 🗳️ DevOps Voting App

A full stack voting application built as a hands-on DevOps learning project. Built by **Haneef Olajobi** as part of a junior DevOps engineering roadmap.

> "Like sending someone a fully charged, ready-to-use device instead of instructions on how to build one." — Haneef on Docker 🐳

---

## 🧠 Project Overview

This project was built to get real, hands-on experience with core DevOps tools — not just watch tutorials. The goal was to take an app from idea to a fully containerised, infrastructure-as-code project with a CI/CD pipeline.

**The app lets users vote for their favourite DevOps tool:**
- 🐍 Python
- 🌐 JavaScript
- 🏗️ Terraform
- 🐳 Docker

Votes are stored in an AWS S3 bucket (LocalStack for local development).

---

## 🏆 What This Project Covers

| DevOps Skill | How It's Used |
|---|---|
| Docker | App containerised and pushed to DockerHub |
| CI/CD (GitHub Actions) | Auto builds and pushes Docker image on every push |
| Terraform | Provisions S3 bucket as Infrastructure as Code |
| AWS S3 (LocalStack) | Stores votes as JSON |
| Linux & Bash | Server setup and scripting |
| Git & GitHub | Version control and pipeline trigger |
| Python Flask | Backend web framework |

---

## 🧩 Architecture

```
Browser (port 5000)
        ↓
Flask Python Backend
        ↓
AWS S3 Bucket (LocalStack locally / real AWS in production)
        ↓
votes.json stored in bucket
```

### CI/CD Flow
```
Push code to GitHub
        ↓
GitHub Actions wakes up
        ↓
✅ Downloads code
✅ Logs into DockerHub
✅ Builds Docker image
✅ Pushes to DockerHub automatically
        ↓
Done in ~25 seconds ⚡
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python Flask | Backend web framework |
| HTML/CSS/JavaScript | Frontend UI |
| Docker | Containerisation |
| DockerHub | Container registry |
| LocalStack | Local AWS S3 emulation |
| Terraform | Infrastructure as Code |
| boto3 | AWS SDK for Python |
| GitHub Actions | CI/CD pipeline |
| Git | Version control |

---

## 📁 Project Structure

```
voting-app/
├── .github/
│   └── workflows/
│       └── pipeline.yml    # CI/CD pipeline
├── app/
│   └── app.py              # Flask backend
├── templates/
│   └── index.html          # Frontend UI
├── terraform/
│   └── main.tf             # Infrastructure as Code
├── Dockerfile              # Container recipe
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🚀 How to Run Locally

### Prerequisites
- Docker installed
- Python 3.12+
- LocalStack
- Terraform

### Step 1 — Start LocalStack (fake AWS)
```bash
export PATH=$PATH:~/.local/bin
localstack start
```

### Step 2 — Provision infrastructure with Terraform
```bash
cd terraform
terraform init
terraform apply
```
Type `yes` when prompted. This creates the S3 bucket automatically.

### Step 3 — Run the app
```bash
cd ..
pip install flask boto3
python3 app/app.py
```

Visit `http://localhost:5000` in your browser and start voting! 🗳️

---

## 🐳 Docker

### Build the image
```bash
docker build -t voting-app .
```

### Run the container
```bash
docker run -d -p 5000:5000 --name voting-container voting-app
```

### Pull from DockerHub (run anywhere!)
```bash
docker run -p 5000:5000 olajobihaneef/voting-app
```

### Useful Docker commands
```bash
docker ps                     # see running containers
docker stop voting-container  # stop the container
docker start voting-container # start it again
docker logs voting-container  # see app logs
docker rm voting-container    # delete the container
docker images                 # see all images
```

---

## 🏗️ Terraform

### What it does
Instead of manually creating the S3 bucket by clicking in the AWS console or running CLI commands, Terraform creates it automatically from code.

### The three commands
```bash
terraform init     # download AWS provider plugin
terraform plan     # preview what will be created
terraform apply    # actually create the infrastructure
terraform destroy  # delete everything
```

### main.tf explained
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"   # get AWS plugin from HashiCorp
      version = "~> 5.0"          # use version 5.x
    }
  }
}

provider "aws" {
  region     = "us-east-1"        # Virginia datacenter
  access_key = "test"             # fake credentials for LocalStack
  secret_key = "test"
  skip_credentials_validation = true  # skip real AWS checks
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3 = "http://127.0.0.1:4566"  # point to LocalStack instead of real AWS
  }
}

resource "aws_s3_bucket" "voting_bucket" {
  bucket        = "voting-app"    # create this S3 bucket
  force_destroy = true
}
```

---

## 🔄 CI/CD Pipeline

### pipeline.yml explained
```yaml
name: Voting App CI/CD Pipeline

on:
  push:
    branches: [main]          # trigger on every push to main

jobs:
  build-and-push:
    runs-on: ubuntu-latest    # use fresh Linux machine
    steps:
      - uses: actions/checkout@v3           # download code
      - uses: docker/login-action@v2        # login to DockerHub
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}
      - run: docker build -t olajobihaneef/voting-app .  # build image
      - run: docker push olajobihaneef/voting-app        # push to DockerHub
```

### Secrets required
Add these in GitHub → Repo → Settings → Secrets and variables → Actions:
- `DOCKER_USERNAME` → your DockerHub username
- `DOCKER_TOKEN` → your DockerHub access token (Read/Write/Delete)

---

## 📊 How Votes Are Stored

Votes are stored as a JSON file in the S3 bucket:

```json
{
  "Python": 45,
  "JavaScript": 16,
  "Terraform": 33,
  "Docker": 29
}
```

Check current votes anytime:
```bash
awslocal s3 cp s3://voting-app/votes.json -
```

---

## ⚠️ Errors Encountered & How I Fixed Them

### 1. Docker permission denied
**Error:** `permission denied while trying to connect to the Docker daemon`
**Fix:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```
**Learned:** Docker daemon requires user to be in the docker group.

---

### 2. Windows line endings in bash scripts
**Error:** `cannot execute: required file not found`
**Fix:**
```bash
sed -i 's/\r//' script.sh
```
Or use `cat << 'EOF'` instead of nano.
**Learned:** Always use `cat << 'EOF'` for scripts in WSL, never nano.

---

### 3. Docker image name must be lowercase
**Error:** `invalid reference format: repository name must be lowercase`
**Fix:**
```bash
docker tag voting-app olajobihaneef/voting-app
```
**Learned:** Docker image names must always be lowercase.

---

### 4. Port already allocated
**Error:** `Bind for 0.0.0.0:5000 failed: port is already allocated`
**Fix:**
```bash
docker stop voting-container
docker run -p 5000:5000 voting-app
```
**Learned:** Only one process can use a port at a time.

---

### 5. requirements.txt typo
**Error:** `COPY failed: file not found: stat requirements.txt`
**Fix:**
```bash
mv requirement.txt requirements.txt
```
**Learned:** Always double check filenames with `ls` before building.

---

### 6. LocalStack connection refused
**Error:** `Could not connect to the endpoint URL: http://localhost:4566`
**Fix:** Restart LocalStack in a separate terminal.
**Learned:** LocalStack must always be running before any AWS commands.

---

### 7. Git push rejected
**Error:** `Updates were rejected because the remote contains work you do not have`
**Fix:**
```bash
git pull origin main --rebase
git push
```
**Learned:** Never add README or files on GitHub when creating a repo — keep it empty and push from local.

---

### 8. GitHub Actions permission denied
**Error:** `remote: Permission to repo denied to github-actions[bot]`
**Fix:** Repo → Settings → Actions → General → Workflow permissions → Read and Write.
**Learned:** GitHub Actions needs explicit write permissions to deploy.

---

### 9. Git init in wrong directory
**Error:** Pipeline file not being tracked by Git.
**Fix:**
```bash
cd voting-app   # go INTO the project folder first
git init        # THEN init
```
**Learned:** Always `cd` into your project folder before running `git init`.

---

### 10. Terraform stuck on localhost IPv6
**Error:** Terraform hanging for minutes trying to connect to LocalStack.
**Fix:** Use `127.0.0.1` instead of `localhost` in `main.tf`:
```hcl
endpoints {
  s3 = "http://127.0.0.1:4566"
}
```
**Learned:** WSL has IPv6 issues with localhost. Always use `127.0.0.1` explicitly.

---

### 11. Snap Terraform broken in WSL
**Error:** `transient scope could not be started`
**Fix:** Uninstall snap version and install via HashiCorp apt repo.
**Learned:** Snap packages don't always work well in WSL. Use apt or direct binaries instead.

---

### 12. DockerHub insufficient token scope
**Error:** `unauthorized: access token has insufficient scopes`
**Fix:** Create new DockerHub token with **Read, Write, Delete** permissions.
**Learned:** Always create tokens with the right permissions from the start.

---

## 💡 My Thinking Process

### Why Docker?
The classic problem in software is "it works on my machine but not yours." Docker solves this by packaging the app with everything it needs — like sending someone a fully charged, ready-to-use device instead of instructions on how to build one.

### Why Terraform?
Instead of clicking through the AWS console and hoping you remember every step, Terraform lets you write infrastructure as code. Need 5 identical environments? Change one number. Need to rebuild from scratch? One command.

### Why LocalStack?
AWS costs money and free tier expires. LocalStack runs the same AWS services locally in Docker — completely free. The commands are identical to real AWS so skills transfer directly.

### Why JSON for vote storage?
Simple key-value data like `tool: count` maps perfectly to JSON. For a production app you'd use a proper database like DynamoDB or PostgreSQL, but for this project S3 + JSON keeps the setup simple while still demonstrating cloud storage integration.

---

## 📈 What's Next

- [ ] Deploy to real AWS (EC2 + real S3)
- [ ] Add PostgreSQL database instead of JSON file
- [ ] Add Terraform for EC2 instance provisioning
- [ ] Add monitoring with Prometheus and Grafana
- [ ] Add proper pytest tests to CI/CD pipeline
- [ ] Add security scanning to pipeline

---

## 🐳 DockerHub

Image available at: `olajobihaneef/voting-app`

```bash
docker run -p 5000:5000 olajobihaneef/voting-app
```

---

## 👨‍💻 Author

**Haneef Olajobi** — Junior DevOps Engineer

- GitHub: [haneeo3](https://github.com/haneeo3)
- DockerHub: [olajobihaneef](https://hub.docker.com/r/olajobihaneef/voting-app)
- Project: Part of a hands-on DevOps learning roadmap covering Linux, Docker, Terraform, CI/CD and AWS
