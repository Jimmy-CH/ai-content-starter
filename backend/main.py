import os
from dotenv import load_dotenv
load_dotenv()
# 👇 临时添加：打印 Key（部署前记得删除！）
print("Loaded DEEPSEEK_API_KEY:", os.getenv("DEEPSEEK_API_KEY"))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.generate import router as generate_router

app = FastAPI(title="AI Content Generator", debug=True)

# 允许前端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(generate_router, prefix="/api/v1")

