# Guestbook Application

This repository contains a simple microservice-based Guestbook application with a **FastAPI backend**, a **Redis datastore**, and a **Nginx-based frontend**.

---

## Components

### Backend (FastAPI)
- Provides REST API endpoints:
  - `GET /` → health check
  - `GET /list` → list all guestbook entries
  - `POST /add/{name}/{msg}` → add a new entry
  - `DELETE /delete/{index}` → delete an entry
- Uses Redis to persist guestbook messages.
- Configurable via `.env` file.

### Frontend (Nginx + HTML/JS)
- Serves `index.html` with a form to add entries and list them dynamically.
- Proxies `/api/*` requests to the backend service.

### Redis
- In-memory datastore to store guestbook entries.

---

## Local Development Setup

### 1. Clone the repo
```sh
git clone <your-repo-url>
cd PI_ASSIGNMENT/app
```

### 2. Start Redis locally
```sh
docker run -d --name redis -p 6379:6379 redis:alpine
```

### 3. Configure Backend
Create a `.env` file in `app/backend/` (see `.env.example`):
```env
REDIS_HOST=redis
REDIS_PORT=6379
```

### 4. Build & Run Backend
```sh
cd backend
docker build -t guestbook-backend .
docker run -d --name guestbook-backend --network host --env-file .env -p 8000:8000 guestbook-backend
```

Test it:
```sh
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/list
```

### 5. Build & Run Frontend
```sh
cd ../frontend
docker build -t guestbook-frontend .
docker run -d --name guestbook-frontend -p 8080:80 guestbook-frontend
```

Open in browser: [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## Local Development with Docker Network

To connect backend ↔ redis automatically, use a custom network:
```sh
docker network create guestbook-net

docker run -d --name redis --network guestbook-net redis:alpine

docker run -d --name guestbook-backend --network guestbook-net --env-file ./backend/.env -p 8000:8000 guestbook-backend

docker run -d --name guestbook-frontend --network guestbook-net -p 8080:80 guestbook-frontend
```

---

## API Examples

### Add Entry
```sh
curl -X POST http://127.0.0.1:8000/add/Aashutosh/Hello
```

### List Entries
```sh
curl http://127.0.0.1:8000/list
```

### Delete Entry
```sh
curl -X DELETE http://127.0.0.1:8000/delete/0
```

---

## Kubernetes Deployment
The application can be deployed to AKS using Helm. See [`helm/guestbook`](../../helm/guestbook) for manifests.

---

## Folder Structure
```
app/
├── backend/
│   ├── .env.example      # environment variables template
│   ├── Dockerfile        # FastAPI backend container
│   ├── main.py           # FastAPI app
│   ├── requirements.txt  # Python dependencies
└── frontend/
    ├── Dockerfile        # Nginx + static HTML/JS
    ├── index.html        # frontend UI
    └── nginx.conf        # Nginx proxy config
```
