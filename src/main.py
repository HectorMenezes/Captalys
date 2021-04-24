from fastapi import FastAPI
from src.res.repository import router as reporouter
from src.services.database import run_migration, MigrationType

APP = FastAPI(title="captalys", version="0.0.1")

APP.include_router(router=reporouter, prefix='/repository', tags=['repositories'])


@APP.on_event('startup')
def start_up():
    try:
        run_migration(MigrationType.upgrade, 'head')
    except Exception: print("Error")
