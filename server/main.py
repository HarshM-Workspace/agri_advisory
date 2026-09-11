import sys
from pathlib import Path

# Add project root to sys.path so imports like `from server.config ...` work
# regardless of whether running from project root or from inside `server/`
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from server.config import BASE_DIR, SERVER_HOST, SERVER_PORT
from server.db.database import create_tables
from server.routers import advisory, demo, farm, sensors


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="AgriAdvisor Server", lifespan=lifespan)

# Allow Cross-Origin Requests for external frontends or API consumers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(farm.router)
app.include_router(sensors.router)
app.include_router(advisory.router)
app.include_router(demo.router)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/demo/controller")


@app.get("/demo")
@app.get("/demo/")
def demo_root():
    return RedirectResponse(url="/demo/controller")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("server.main:app", host=SERVER_HOST, port=SERVER_PORT, reload=False)
