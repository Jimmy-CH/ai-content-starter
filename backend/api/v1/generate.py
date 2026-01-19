
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os

router = APIRouter()


class GenerateRequest(BaseModel):
    keyword: str
    platform: str  # "xiaohongshu", "douyin", "gongzhonghao"


# 从环境变量读取 DeepSeek API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


@router.post("/titles")
async def generate_titles(req: GenerateRequest):
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY 未配置")

    prompt = get_prompt(req.platform, req.keyword)

    try:
        # 调用 DeepSeek API（兼容 OpenAI 格式）
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",  # DeepSeek 主力模型
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
        )
        response.raise_for_status()
        data = response.json()

        # 提取生成的文本
        content = data["choices"][0]["message"]["content"].strip()
        titles_list = [line.strip() for line in content.split("\n") if line.strip()]
        return {"titles": titles_list}

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            error_msg = "API Key 无效，请检查 DEEPSEEK_API_KEY"
        elif "429" in error_msg:
            error_msg = "请求过于频繁，请稍后再试"
        print(f"[ERROR] DeepSeek API 调用失败: {error_msg}")
        raise HTTPException(status_code=500, detail=f"生成失败: {error_msg}")


def get_prompt(platform: str, keyword: str) -> str:
    base = f"你是一个资深自媒体运营专家，请围绕关键词“{keyword}”生成5个爆款标题。要求："
    prompts = {
        "xiaohongshu": base + "口语化、带 emoji（如🔥💡✨）、有冲突感或好奇心，长度20字以内。",
        "douyin": base + "短平快、带悬念、使用感叹号或问号，20字内，适合短视频。",
        "gongzhonghao": base + "有观点、有情绪、引发共鸣，可使用冒号结构，适合深度文章。"
    }
    return prompts.get(platform, prompts["xiaohongshu"])


