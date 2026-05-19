# ⚡ StrideIQ — AI-Powered Running Form Analyzer

> Upload your running video → Get instant biomechanical feedback, injury risk score, and personalised coaching tips.

**Stack:** Django + Django REST Framework · React · Docker · GitHub Actions · AWS EC2

---

## 📁 Project Structure

```
strideiq/
├── backend/                         # Django + DRF API
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── strideiq_project/            # Django project (settings, urls, wsgi)
│   ├── analysis/                    # Django app — models, views, serializers, urls
│   ├── models_ml/                   # Random Forest ML model
│   └── utils/                       # pose_estimator, biomechanics, storage
│
├── frontend/                        # React SPA
│   ├── Dockerfile
│   ├── nginx.conf                   # Nginx config for container
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── components/              # Navbar, VideoUploader, ResultsPanel
│       ├── pages/                   # Home, History, About
│       └── utils/api.js             # Axios client
│
├── docker-compose.yml               # Local & production orchestration
└── .github/workflows/deploy.yml     # GitHub Actions CI/CD
```

---

## 🚀 Local Development (without Docker)

### Prerequisites: Python 3.11+, Node 20+

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
python manage.py runserver
# API available at http://localhost:8000
# Health check: curl http://localhost:8000/api/health/
```

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm start
# App opens at http://localhost:3000
# Proxies /api → http://localhost:8000
```

---

## 🐳 Docker (Recommended)

```bash
# Copy and configure environment
cp backend/.env.example backend/.env
# Edit backend/.env — set SECRET_KEY at minimum

# Build and run everything
docker compose up --build

# App available at http://localhost:80
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analyze/` | Upload video for analysis |
| `GET`  | `/api/history/?session_id=<id>` | List past analyses |
| `GET`  | `/api/analysis/<id>/` | Single analysis detail |
| `GET`  | `/api/health/` | Health check |

### POST `/api/analyze/`

**Request:** `multipart/form-data`
- `video` — mp4/mov/avi/webm file
- `session_id` — optional string (UUID generated if omitted)

**Response:**
```json
{
  "id": 1,
  "session_id": "uuid",
  "risk_level": "Medium",
  "overall_score": 72.4,
  "scores": { "cadence": 85, "knee_drive_angle": 62, "..." : "..." },
  "metrics": { "cadence": 163.0, "forward_lean": 7.2, "..." : "..." },
  "injuries": ["Shin Splints", "Knee Pain (Overstriding)"],
  "feedback": [{ "metric": "cadence", "injury": "...", "fix": "..." }],
  "probabilities": { "Low": 0.12, "Medium": 0.68, "High": 0.20 },
  "shap_values": { "cadence": 0.35, "knee_drive_angle": 0.28 },
  "video_url": "/media/videos/original.mp4",
  "annotated_url": "/media/annotated/skeleton.mp4"
}
```

---

## 🌐 AWS EC2 Deployment

### 1. Launch EC2 (Ubuntu 22.04, t3.medium+)

Open ports: **22** (SSH), **80** (HTTP), **443** (HTTPS)

### 2. Server Setup

```bash
# Install Docker
sudo apt update && sudo apt install -y docker.io docker-compose-plugin git
sudo usermod -aG docker ubuntu
newgrp docker

# Clone the repo
sudo mkdir -p /opt/strideiq && sudo chown ubuntu:ubuntu /opt/strideiq
git clone https://github.com/yourusername/strideiq.git /opt/strideiq
cd /opt/strideiq

# Configure environment
cp backend/.env.example backend/.env
nano backend/.env  # Set SECRET_KEY, DEBUG=False, ALLOWED_HOSTS=your-domain.com

# Start the app
docker compose up -d --build
```

### 3. SSL with Certbot (optional but recommended)

```bash
sudo apt install -y certbot
sudo certbot certonly --standalone -d your-domain.com
# Then update docker-compose.yml to mount certs and expose 443
```

---

## 🔐 GitHub Actions Secrets

In your repo → **Settings → Secrets → Actions**, add:

| Secret | Value |
|--------|-------|
| `EC2_HOST` | EC2 public IP or domain |
| `EC2_USER` | `ubuntu` |
| `EC2_SSH_KEY` | Contents of your `.pem` private key |
| `REACT_APP_API_URL` | `https://your-domain.com/api` |
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password or access token |

### CI/CD Pipeline Steps
1. **Django checks + migrate dry-run** — validates models and settings
2. **React build** — produces optimised static bundle
3. **Docker build & push** — images pushed to Docker Hub
4. **SSH deploy** — pulls new images and restarts containers on EC2

---

## 🔧 Environment Variables (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | *(required)* | Django secret key |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `DATABASE_NAME` | `strideiq.db` | SQLite filename |
| `UPLOAD_FOLDER` | `media/uploads` | Local video storage path |
| `MAX_CONTENT_LENGTH_MB` | `100` | Max upload size |
| `AWS_ACCESS_KEY_ID` | *(optional)* | S3 upload |
| `AWS_SECRET_ACCESS_KEY` | *(optional)* | S3 upload |
| `AWS_REGION` | `us-east-1` | S3 region |
| `S3_BUCKET_NAME` | *(optional)* | S3 bucket — videos stored locally if unset |

---

## 🧠 Biomechanical Metrics

| Metric | Optimal Range | Related Injury |
|--------|---------------|----------------|
| Cadence | 170–180 spm | Shin splints, knee pain |
| Knee Drive Angle | 55–75° | IT band syndrome |
| Forward Lean | 5–10° | Lower back pain, hamstring strain |
| Foot Strike Offset | 0.02–0.06 | Knee pain (overstriding) |
| Arm Crossing Index | 0.05–0.15 | Hip rotational stress |

---

## 📄 License

MIT — free for personal and academic use.
