from fastapi import FastAPI
from starlette.responses import RedirectResponse

from core.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs")
