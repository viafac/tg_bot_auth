from pydantic import BaseModel, field_validator


class PromptInput(BaseModel):
    books: str
    question: str

    @field_validator('books')
    def check_books_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Books cannot be empty.")
        return v

    @field_validator('question')
    def check_question_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Question cannot be empty.")
        return v
