import fastapi
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class ChoiseBase(BaseModel):
    choice_text:str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices : List[ChoiseBase]


def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


@app.post("/questions/")
async def create_questions(question: QuestionBase, db:db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()