from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user



app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)

# utilizamos o alembic para gerenciar a criação das tabelas:

# models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "FastAPI api is working"}






