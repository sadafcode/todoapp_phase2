from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # NEW IMPORT
from db import create_db_and_tables
from routes.tasks import router as tasks_router
from routes.auth import router as auth_router # NEW IMPORT

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    create_db_and_tables()  # Create database tables on startup
    yield
    # Code to run on shutdown (if any)

app = FastAPI(lifespan=lifespan)

# NEW CORS CONFIGURATION
origins = [
    "http://localhost",
    "http://localhost:3000", # Frontend's default port
    "http://localhost:3001", # Frontend on port 3001
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router)
app.include_router(auth_router) # NEW INCLUDE

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend!"}