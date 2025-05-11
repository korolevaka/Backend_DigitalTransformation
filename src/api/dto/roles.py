from pydantic import BaseModel

class Role(BaseModel):
    player_id: int
    role: str

class Character(BaseModel):
    player_id: int
    character: bool
