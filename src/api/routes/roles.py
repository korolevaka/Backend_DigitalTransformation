from random import shuffle

from fastapi import APIRouter

import src.db.database_manager as db
from src.api.dto.roles import Role, Character
from src.db.models import SessionPlayer

router = APIRouter()


@router.get("/roles/")
def get_roles(room_id: int) -> list[Role]:
    data = db.get_session_players(session_id=room_id)
    if not data[0].role:
        shuffle_roles(data)
    result = []
    for entry in data:
        result.append(Role(player_id=entry.player_id, role=entry.role))
    return result



@router.post("/characters/")
def get_character(room_id: int, user_id: int):
    """Get character of specified user"""
    data = db.get_session_player(session_id=room_id, player_id=user_id)
    result = Character(player_id=data.player_id, character=data.is_positive)
    return result


def shuffle_roles(room_id, players: list[SessionPlayer]):
    roles = db.get_roles()
    shuffle(roles)
    for i in range(len(roles)):
        db.set_player_role(room_id, players[i].player_id, roles[i].name)


@router.post("/characters/")
def set_character(room_id: int):
    """Get character of specified user"""
    characters = [True, True, True, True, True, True, False, False, False, False]
    players = db.get_session_players(room_id)
    shuffle(characters)
    for i in range(len(characters)):
        db.set_player_character(room_id, players[i].player_id, characters[i])
    return True