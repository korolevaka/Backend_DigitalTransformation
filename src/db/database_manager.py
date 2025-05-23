from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.db.models import Player, Session, SessionPlayer, GameResult, PlayerStatistics, \
    SessionLocal, Image

db = SessionLocal()


def create_player(name: str, password: str, tg_id: int) -> Player:
    """Добавить человека в бд"""
    new_player = Player(name=name, password=password, tg_id=tg_id)
    db.add(new_player)
    try:
        db.commit()
        db.refresh(new_player)
        return new_player
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Player with Telegram ID {tg_id} already exists.")


def create_room(password):
    new_room = Session(password=password)
    db.add(new_room)
    try:
        db.commit()
        db.refresh(new_room)
        return new_room
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ошибка создания комнаты")


def get_player(player_id: int) -> Player:
    """Получить игрока по id"""
    return db.query(Player).filter(Player.player_id == player_id).first()


def get_player_by_login(login: str) -> Player:
    """Получить игрока по login"""
    return db.query(Player).filter(Player.name == login).first()


def get_player_by_tg_id(tg_id: int) -> Player:
    """Получить игрока по id телеграмма"""
    return db.query(Player).filter(Player.tg_id == tg_id).first()


def get_room_by_id(room_id: int) -> Session:
    return db.query(Session).filter_by(session_id=room_id).first()


def create_session(case_id: int, count_players: int) -> Session:
    """Добавить новую комнату"""
    new_session = Session(case_id=case_id, count_players=count_players)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


def add_player_to_session(session_id: int, player_id: int, role: str, is_positive: bool) -> SessionPlayer:
    """Добавить игрока в комнату"""
    session_player = SessionPlayer(session_id=session_id, player_id=player_id, role=role, is_positive=is_positive)
    db.add(session_player)
    db.commit()
    db.refresh(session_player)
    return session_player


def create_game_result(session_id: int, start_time: str, end_time: str, total_it_points: int,
                       total_hr_points: int, total_ec_points: int, total_bp_points: int,
                       is_successful: bool) -> GameResult:
    """Создать результат игры"""
    new_game_result = GameResult(
        session_id=session_id,
        start_time=start_time,
        end_time=end_time,
        total_it_points=total_it_points,
        total_hr_points=total_hr_points,
        total_ec_points=total_ec_points,
        total_bp_points=total_bp_points,
        is_successful=is_successful
    )
    db.add(new_game_result)
    db.commit()
    db.refresh(new_game_result)
    return new_game_result


def get_player_statistics(player_id: int) -> PlayerStatistics:
    """Получить статистику игрока"""
    return db.query(PlayerStatistics).filter(PlayerStatistics.player_id == player_id).first()


def update_player_statistics(player_id: int, total_games_played: int, total_wins: int, total_losses: int,
                             average_it_points: float, average_hr_points: float, average_ec_points: float,
                             average_bp_points: float) -> PlayerStatistics:
    """Обновить статистику игрока"""
    player_stats = db.query(PlayerStatistics).filter(PlayerStatistics.player_id == player_id).first()
    if player_stats:
        player_stats.total_games_played = total_games_played
        player_stats.total_wins = total_wins
        player_stats.total_losses = total_losses
        player_stats.average_it_points = average_it_points
        player_stats.average_hr_points = average_hr_points
        player_stats.average_ec_points = average_ec_points
        player_stats.average_bp_points = average_bp_points
        db.commit()
        db.refresh(player_stats)
    else:
        raise ValueError(f"Statistics for player {player_id} not found.")
    return player_stats


def delete_player(player_id: int):
    """Удалить игрока"""
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player:
        db.delete(player)
        db.commit()
    else:
        raise ValueError(f"Player with ID {player_id} not found.")


# def validate_room_password(room_id, password):
#     room = get_room_by_id(room_id)
#     if room and room.password == password:  # Сравниваем пароли
#         return True
#     return False


def add_image(image_path, image_name):
    with open(image_path, "rb") as file:
        image_data = file.read()

    new_image = Image(name=image_name, image_data=image_data)
    db.add(new_image)
    db.commit()
    print(f"Изображение '{image_name}' добавлено в БД.")


def get_image(image_name):
    return db.query(Image).filter(Image.name == image_name).first()
