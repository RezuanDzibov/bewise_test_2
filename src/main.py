import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from core.settings import get_settings
from endpoints.routes import router

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse("/docs")


@app.on_event("startup")
async def startup():
    if not os.path.isdir(settings.MEDIA_PATH):
        Path.mkdir(settings.MEDIA_PATH)


if __name__ == "__main__":
    uvicorn.run(app)
