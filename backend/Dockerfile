# backend/Dockerfile

# ==============================
# 第一阶段：构建依赖
# ==============================
FROM python:3.11-slim AS builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖（可选，如需要编译 C 扩展）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖（使用 --user 避免权限问题）
RUN pip install --no-cache-dir --user -r requirements.txt


# ==============================
# 第二阶段：运行时镜像
# ==============================
FROM python:3.11-slim AS runtime

# 创建非 root 用户（安全最佳实践）
RUN addgroup --system app && adduser --system --ingroup app app

# 设置工作目录
WORKDIR /app

# 复制已安装的依赖（从 builder 阶段）
COPY --from=builder /root/.local /root/.local

# 将非 root 用户加入 app 组并设置权限
RUN chown -R app:app /app
USER app

# 将用户本地 bin 加入 PATH
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 暴露端口（标准）
EXPOSE 8000

# 启动命令
# 注意：$PORT 由 Render/Fly.io 等平台自动注入
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
