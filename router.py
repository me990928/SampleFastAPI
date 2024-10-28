""" This file is used to include all the routers in the application. """

from fastapi import APIRouter
import api.v1.api as api
import api.v1.todo.api as todo_api
import api.v1.todo.async_api as async_todo_api

# APIるーターを作成
api_router = APIRouter()

# APIルーターを呼び出す
# http://localhost:8000/api/{prefix} でアクセス可能
api_router.include_router(api.router, prefix="/test")
api_router.include_router(todo_api.router, prefix="/todoapp")
api_router.include_router(async_todo_api.router, prefix="/asynctodoapp")
