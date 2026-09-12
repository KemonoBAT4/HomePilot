from contextlib import asynccontextmanager

from fastapi import FastAPI

from handlers import mdns
from database import Base, engine
from routers import pairing, pcs, profiles, agents

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    mdns.start_discovery()

    yield

    mdns.stop_discovery()
# #enddef lifespan

app = FastAPI(title="HomePilot server", lifespan=lifespan)

app.include_router(pairing.router)
app.include_router(pcs.router)
app.include_router(profiles.router)
app.include_router(agents.router)

@app.get("/health")
def health():
    return {"status": "ok"}
# #enddef health
