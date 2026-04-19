from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.rag_routes import router

app = FastAPI(title="Production RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost:5174",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "ok"}