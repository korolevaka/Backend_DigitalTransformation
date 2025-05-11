from pydantic import BaseModel, Field


class Role(BaseModel):
    player_id: int = Field(..., alias="playerId", description="ID игрока")
    role: str = Field(..., description="Роль игрока")

class Character(BaseModel):
    player_id: int = Field(..., alias="playerId", description="ID игрока")
    character: bool = Field(..., description="Характер игрока")
