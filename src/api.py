from fastapi import FastAPI, HTTPException
from src.db.database import Database
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()
db = Database()

class WordCreate(BaseModel):
    simplified: str
    pinyin: str
    english: str
    parts: Dict = None

@app.post("/words/")
async def create_word(word: WordCreate):
    word_id = db.add_word(word.simplified, word.pinyin, word.english, word.parts)
    return {"id": word_id}

@app.get("/words/")
async def get_words():
    return db.get_words() 