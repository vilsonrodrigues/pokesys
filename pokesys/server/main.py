import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.globals import set_verbose, set_debug
from pokesys.config.app import APP_CONFIG
from pokesys.logger import enable_debug_logging
from pokesys.server.routers import battle, chat, health, root


if APP_CONFIG.logger_level == "debug":
    enable_debug_logging()
    set_verbose(True)
    set_debug(True)

app = FastAPI(
    title="Pokemon AI System",
    description="A multi-agent system for answering questions about Pokémon",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(battle.router)
app.include_router(chat.router)
app.include_router(health.router)
app.include_router(root.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True,
    )