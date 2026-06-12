
from fastapi import FastAPI
from pydantic import BaseModel

from legalmind_core import run_legalmind

app = FastAPI(
    title="LegalMind API",
    version="1.0"
)

class LegalQuery(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "LegalMind API Running"
    }


@app.post("/analyze")
def analyze(query: LegalQuery):

    result = run_legalmind(
        query.question
    )

    return result
