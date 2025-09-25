from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
# r = redis.Redis(host="redis", port=6379, decode_responses=True)
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
@app.get("/")
def read_root():
    return {"message": "Welcome to Guestbook API"}

@app.post("/add/{name}/{msg}")
def add_entry(name: str, msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{name}: {msg} ({timestamp})"
    r.rpush("guestbook", entry)
    return {"status": "added", "entry": entry}

@app.get("/list")
def list_entries():
    entries = r.lrange("guestbook", 0, -1)
    return {"guestbook": entries}

@app.delete("/delete/{index}")
def delete_entry(index: int):
    try:
        removed = r.lindex("guestbook", index)
        if removed:
            r.lset("guestbook", index, "__deleted__")
            r.lrem("guestbook", 1, "__deleted__")
            return {"status": "deleted", "entry": removed}
        return {"status": "not found"}
    except Exception as e:
        return {"error": str(e)}