from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.generate import router as generate_router

app = FastAPI(title="AI Content Generator")

# 允许前端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_parent="/api/v1")

