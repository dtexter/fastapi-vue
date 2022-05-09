from pydantic import BaseModel


class Program(BaseModel):
    title: str
    body: str
