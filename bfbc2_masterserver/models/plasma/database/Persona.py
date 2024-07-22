from pydantic import BaseModel


class Persona(BaseModel):
    id: int
    name: str
