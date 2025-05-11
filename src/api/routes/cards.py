from fastapi import APIRouter, Query
import src.db.database_manager as db
from src.api.dto.cards import Case, Balance, Score, Result

router = APIRouter()


@router.post('/tool')
async def use_tool(room_id: int = Query(..., description="ID комнаты"), card_id: int = Query(..., description="ID карточки")) -> Result:
    """Генеральный директор выбирает какой инструмент купить в этом раунде"""
    card = db.get_tool(tool_id=card_id)
    return await use_card(card.it_points, card.hr_points, card.ec_points, card.bp_points, room_id)


@router.post('/management')
async def use_management_card(room_id: int = Query(..., description="ID комнаты"), card_id: int = Query(..., description="ID карточки")) -> Result:
    """Губернатор применяет карту управления"""
    card = db.get_management_card(card_id=card_id)
    return await use_card(card.it_effect, card.hr_effect, card.ec_effect, card.bp_effect, room_id)


async def use_card(it, hr, ec, bp, room_id):
    score_data = db.update_game_score(
        session_id=room_id,
        it_points=it,
        hr_points=hr,
        ec_points=ec,
        bp_points=bp,
    )
    score = Score(
        total_it_points=score_data.total_it_points,
        total_hr_points=score_data.total_hr_points,
        total_ec_points=score_data.total_ec_points,
        total_bp_points=score_data.total_bp_points
    )
    is_succesful = db.check_requirements(session_id=room_id)
    result = Result(score=score, is_succesful=is_succesful)
    return result


@router.get('/dtc')
async def get_dtc(room_id: int = Query(..., description="ID комнаты")):
    """Получить нынешний баланс DTC"""
    data = db.get_currency(session_id=room_id)
    dtc = Balance(dtc=data.remains)
    return dtc


@router.get('/case')
async def get_case(room_id: int = Query(..., description="ID комнаты")) -> Case:
    """Получить требования по очкам нынешнего кейса"""
    data = db.get_case(session_id=room_id)
    case = Case(
        required_it_points=data.required_it_points,
        required_hr_points=data.required_hr_points,
        required_ec_points=data.required_ec_points,
        required_bp_points=data.required_bp_points,
    )
    return case
