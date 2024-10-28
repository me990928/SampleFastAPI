""" Main file to run the FastAPI application """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from router import api_router

# FastAPIのインスタンスを作成
app = FastAPI(
    title="FastAPI Example",
    description="This is an example of how to include routers in FastAPI",
    version="0.1"
)

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターを追加
# http://localhost:8000/api でアクセス可能
app.include_router(api_router, prefix="/api")

# メイン関数
if __name__ == "__main__":
    # FastAPIアプリケーションを実行
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
