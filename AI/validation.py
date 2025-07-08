from pydantic import BaseModel, validator


class PromptInput(BaseModel):
    books: str
    question: str

    @validator('books')
    def check_books_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Книги не могут быть пустыми.")
        return v

    @validator('question')
    def check_question_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Вопрос не может быть пустым.")
        return v


