
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth, expenses


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",       # vite preview
        "https://your-app.vercel.app", # replace later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(expenses.router)

@app.get("/")
def root():
    return {"status": "Expense Tracker API is running"}