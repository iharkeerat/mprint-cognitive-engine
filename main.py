import os
import json
import sqlite3
import random
import jwt
import datetime
import re
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr
from dotenv import load_dotenv
from google import genai
from graph_query import get_learning_path, get_adaptive_path

load_dotenv()

# Fetch the key
api_key = os.getenv("GEMINI_API_KEY", "").strip().strip("'\"")

if not api_key or api_key == "your_actual_api_key_here":
    print("\n" + "!"*60)
    print("⚠️ CRITICAL: YOU HAVE NOT SET A VALID GOOGLE API KEY! ⚠️")
    print("The app will ONLY generate placeholder questions.")
    print("!"*60 + "\n")

ai_client = genai.Client(api_key=api_key)

app = FastAPI()

def clean_json(text):
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    text = text.strip()

    start = text.find('[')
    end = text.rfind(']')
    if start != -1 and end != -1:
        return text[start:end+1]
    return text


def fallback_questions(topic, num_questions=5):
    file_path = f"{topic.lower()}_questions.json"

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                local_data = json.load(f)
                random.shuffle(local_data)  # Mix them up
                return local_data[:num_questions]
        except Exception as e:
            print(f"Error reading local file: {e}")

    questions = []
    for i in range(num_questions):
        questions.append({
            "question": f"Pre-generated logic: Explain a core concept of {topic}?",
            "difficulty": 2,
            "concept": "General",
            "options": [
                {"text": "Correct Analysis", "is_correct": True, "style": "Theorist"},
                {"text": "Incorrect Data", "is_correct": False, "style": "Activist"},
                {"text": "Observation Error", "is_correct": False, "style": "Reflector"},
                {"text": "Practical Mismatch", "is_correct": False, "style": "Pragmatist"}
            ]
        })
    return questions

# --- SECURITY CONFIG ---
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_for_local_dev_only")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_ai_questions(topic, difficulty, level, weak_concepts=None, num_questions=5):
    num_questions = min(max(num_questions, 1), 10)

    if weak_concepts is None:
        weak_concepts = []

    prompt = f"""
    Generate EXACTLY {num_questions} MCQ questions.

    Topic: {topic}
    Difficulty: {difficulty} (1-5)
    Level: {level}

    Return ONLY a raw JSON array. No markdown formatting, no backticks.

    [
      {{
        "question": "...",
        "difficulty": {difficulty},
        "concept": "...",
        "options": [
          {{"text": "...", "is_correct": true, "style": "Theorist"}},
          {{"text": "...", "is_correct": false, "style": "Activist"}},
          {{"text": "...", "is_correct": false, "style": "Reflector"}},
          {{"text": "...", "is_correct": false, "style": "Pragmatist"}}
        ]
      }}
    ]
    """

    if weak_concepts:
        prompt += f"\nFocus more on weak areas: {', '.join(weak_concepts)}"

    try:
        # Use the modern API call structure
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print("\n" + "="*50)
        print("🚨 API CONNECTION FAILED 🚨")
        print(f"Error Details: {str(e)}")
        print("="*50 + "\n")
        return "[]"

def create_access_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# 0. DATABASE INITIALIZATION
# -----------------------------
def init_db():
    conn = sqlite3.connect("alis.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            level TEXT,
            goal TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT,
            topic TEXT,
            target_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            style TEXT,
            type TEXT,
            is_correct BOOLEAN,
            time REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()


# -----------------------------
# 1. MODELS
# -----------------------------
class ResponseModel(BaseModel):
    style: str
    type: str
    difficulty: int
    time: float
    is_correct: bool

class SessionData(BaseModel):
    user_id: int
    session_id: str
    topic: str
    target_level: str
    responses: List[ResponseModel]

class PathRequest(BaseModel):
    session_id: str
    target_skill: str = Field(..., min_length=1)
    target_level: str
    responses: List[ResponseModel] = Field(..., min_items=1)

class SignupData(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    level: str
    goal: str

class LoginData(BaseModel):
    email: str
    password: str


# -----------------------------
# 2. DIAGNOSTIC QUESTIONS
# -----------------------------
@app.get("/get-questions")
async def get_questions(
        topic: str,
        level: str = "Beginner",
        accuracy: Optional[float] = None,
        weak_concepts: Optional[str] = None,
        num_questions: int = 5
):
    num_questions = min(max(num_questions, 1), 10)

    difficulty = 2
    if accuracy is not None:
        difficulty = 1 if accuracy < 40 else 3 if accuracy > 80 else 2

    wc_list = [c.strip() for c in weak_concepts.split(",")] if weak_concepts else []

    ai_output = generate_ai_questions(
        topic,
        difficulty=difficulty,
        level=level,
        weak_concepts=wc_list,
        num_questions=num_questions
    )

    ai_output = clean_json(ai_output)

    try:
        questions = json.loads(ai_output)
        if not isinstance(questions, list) or len(questions) == 0:
            raise ValueError("AI did not return a valid JSON list.")
    except Exception as e:
        print(f"⚠️ Falling back to templates. Reason: {e}")
        questions = fallback_questions(topic, num_questions=num_questions)

    return questions[:num_questions]

# -----------------------------
# 3. CORE ENGINE ENDPOINTS
# -----------------------------
@app.post("/save-session")
def save_session(data: SessionData):
    conn = sqlite3.connect("alis.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO sessions (user_id, session_id, topic, target_level) VALUES (?, ?, ?, ?)",
            (data.user_id, data.session_id, data.topic, data.target_level)
        )
        for r in data.responses:
            cursor.execute(
                "INSERT INTO responses (session_id, style, type, is_correct, time) VALUES (?, ?, ?, ?, ?)",
                (data.session_id, r.style, r.type, r.is_correct, r.time)
            )
        conn.commit()
        return {"status": "saved"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


@app.post("/generate-path")
def generate_path(data: PathRequest):
    total_q = len(data.responses)
    accuracy = (sum(1 for r in data.responses if r.is_correct) / total_q) * 100

    weak_concepts = []
    for r in data.responses:
        if not r.is_correct:
            weak_concepts.append(r.type)

    if accuracy < 40:
        routing_mode = "FOUNDATION_BRIDGE"
        message = "Foundational gaps detected. Re-routing to core prerequisites."
    elif accuracy > 80:
        routing_mode = "EXPERT_ACCELERATION"
        message = "High proficiency detected. Fast-tracking to advanced architecture."
    else:
        routing_mode = "BALANCED_GROWTH"
        message = "Standard pathway generated based on your profile."

    paths = get_adaptive_path(data.target_skill, accuracy, routing_mode)
    style_counts = {}

    for r in data.responses:
        style = r.style
        style_counts[style] = style_counts.get(style, 0) + 1

    return {
        "mprint": {
            "confidence": round(accuracy, 2),
            "marker": "Proficient" if accuracy > 70 else "Learning",
            "message": message
        },
        "paths": paths,
        "mode": routing_mode,
        "style_distribution": style_counts,
        "weak_concepts": weak_concepts
    }


@app.get("/user-history")
def get_user_history(user_id: int):
    conn = sqlite3.connect("alis.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.topic,
               s.timestamp,
               AVG(r.time) as avg_speed,
               (SUM(CASE WHEN r.is_correct = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(r.id)) as accuracy
        FROM sessions s
        JOIN responses r ON s.session_id = r.session_id
        WHERE s.user_id = ?
        GROUP BY s.session_id
        ORDER BY s.timestamp ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    history = {}
    for row in rows:
        topic, timestamp, speed, acc = row
        if topic not in history:
            history[topic] = []
        history[topic].append({"date": timestamp, "speed": round(speed, 2), "accuracy": round(acc, 1)})
    return history


# -----------------------------
# 4. AUTHENTICATION
# -----------------------------
@app.post("/signup")
def signup(data: SignupData):
    conn = sqlite3.connect("alis.db")
    cursor = conn.cursor()
    try:
        hashed_pwd = pwd_context.hash(data.password)
        cursor.execute("INSERT INTO users (name, email, password, level, goal) VALUES (?, ?, ?, ?, ?)",
                       (data.name, data.email, hashed_pwd, data.level, data.goal))
        conn.commit()
        return {"message": "Signup successful"}
    except sqlite3.IntegrityError:
        return {"error": "User already exists"}
    finally:
        conn.close()


@app.post("/login")
def login(data: LoginData):
    conn = sqlite3.connect("alis.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email=?", (data.email,))
    user = cursor.fetchone()
    conn.close()

    if user and pwd_context.verify(data.password, user[1]):
        token = create_access_token(user[0])
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user[0]
        }
    else:
        return {"error": "Invalid credentials"}