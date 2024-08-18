# fastapi_middleware_aa/middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class AAMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 在这里添加中间件逻辑
        response = await call_next(request)
        response.headers["X-Custom-Header"] = "Middleware AA Applied"
        return response