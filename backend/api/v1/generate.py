from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os

router = APIRouter()


class GenerateRequest(BaseModel):
    keyword: str
    platform: str  # "xiaohongshu", "douyin", "gongzhonghao"


# 替换为你的 Qwen API Key（阿里云百炼 / DashScope）
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


@router.post("/titles")
async def generate_titles(req: GenerateRequest):
    if not DASHSCOPE_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    prompt = get_prompt(req.platform, req.keyword)

    try:
        response = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            headers={
                "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen-max",
                "input": {"messages": [{"role": "user", "content": prompt}]},
                "parameters": {"result_format": "message"}
            }
        )
        result = response.json()
        content = result["output"]["choices"][0]["message"]["content"]
        return {"titles": [line.strip() for line in content.split("\n") if line.strip()]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_prompt(platform: str, keyword: str) -> str:
    prompts = {
        "xiaohongshu": f"你是一个资深小红书运营专家，请围绕关键词“{keyword}”生成5个爆款标题。要求：口语化、带emoji（如🔥💡✨）、有冲突感或好奇心，长度20字以内。",
        "douyin": f"你是抖音爆款文案高手，请为“{keyword}”生成5个高点击率短视频标题。要求：短平快、带悬念、使用感叹号或问号，20字内。",
        "gongzhonghao": f"你是公众号百万主笔，请围绕“{keyword}”写5个深度文章标题。要求：有观点、有情绪、引发共鸣，可使用冒号结构。"
    }
    return prompts.get(platform, prompts["xiaohongshu"])


