import uvicorn
from fastapi import FastAPI
from src.api.routes.cards import router as cards_router
from src.api.routes.roles import router as roles_router

app = FastAPI()
app.include_router(cards_router)
app.include_router(roles_router)


def run():
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")


if __name__ == "__main__":
    run()