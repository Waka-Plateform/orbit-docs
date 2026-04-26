"""FastAPI entrypoint for orbit-docs MCP server."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from config import settings
from mcp_server import mcp as mcp_instance
from docs_ops import client as docs_client

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL, logging.INFO))
logger = logging.getLogger("orbit-docs")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("orbit-docs starting – 16 tools")
    async with mcp_instance.session_manager.run():
        yield
    await docs_client.close()
    logger.info("orbit-docs stopped")


app = FastAPI(title="Orbit Docs", lifespan=lifespan)
app.mount("/mcp", mcp_instance.streamable_http_app())


@app.middleware("http")
async def fix_mcp_trailing_slash(request: Request, call_next):
    if request.url.path == "/mcp" and request.method in ("POST", "GET", "DELETE"):
        request.scope["path"] = "/mcp/"
    return await call_next(request)


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "orbit-docs", "tools": 16}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, log_level="info")
