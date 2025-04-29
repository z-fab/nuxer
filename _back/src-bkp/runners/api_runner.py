import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, fabbank, root, webhooks

app = FastAPI(
    title="Nuxer API",
    description="API do Nuxer",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(fabbank.router)
app.include_router(auth.router)
app.include_router(webhooks.router)


def init_api():
    uvicorn.run("runners.api_runner:app", host="0.0.0.0", port=8000, reload=True)
