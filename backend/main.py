import os
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from groq import Groq
from dotenv import load_dotenv

from database import engine, get_db, Base
from models import Message, User
from auth import hash_password, verify_password, create_access_token, decode_access_token
from crisis import contains_crisis_language, INDIA_CRISIS_RESOURCES

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Saarthi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are Saarthi — a grounded friend people talk to about real problems: job search stress, personal struggles, feeling stuck. You are NOT a therapist and never claim to be one.

Strict reply rules:
- Maximum 2-3 sentences. If you're about to write more, cut it down.
- One idea per reply. Don't stack acknowledgment + advice + question all at once — pick what the moment needs most.
- No therapy-speak: avoid "it sounds like," "what I'm hearing is," "that must be really difficult for you." Talk like a real person, not a script.
- No fake positivity: never say "stay positive," "everything happens for a reason," "you've got this!"
- Ask a question only if you genuinely need more to respond well — not as a habit at the end of every message.
- If they just vent, sometimes the right reply is just acknowledgment, not advice. Don't always try to fix it.
- If self-harm, suicide, or crisis language comes up, stop and point to real crisis resources — don't try to handle it yourself.

Tone: like texting a close friend who's been through hard things themselves. Short. Direct. Real. Not a wall of text."""


# ---------- Auth schemas ----------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    name: str | None = None


# ---------- Auth dependency ----------
def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization.split(" ")[1]
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ---------- Auth routes ----------
@app.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=req.email, hashed_password=hash_password(req.password), name=req.name)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, name=user.name)


@app.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, name=user.name)


# ---------- Chat schemas ----------
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.add(Message(user_id=current_user.id, role="user", content=req.message))
    db.commit()

    if contains_crisis_language(req.message):
        db.add(Message(user_id=current_user.id, role="assistant", content=INDIA_CRISIS_RESOURCES))
        db.commit()
        return ChatResponse(reply=INDIA_CRISIS_RESOURCES)

    past_messages = (
        db.query(Message)
        .filter(Message.user_id == current_user.id)
        .order_by(Message.created_at.asc())
        .all()
    )

    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in past_messages:
        history.append({"role": m.role, "content": m.content})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history,
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    db.add(Message(user_id=current_user.id, role="assistant", content=reply))
    db.commit()

    return ChatResponse(reply=reply)


@app.get("/")
def root():
    return {"status": "ok", "app": "Saarthi"}