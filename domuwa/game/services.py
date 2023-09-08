from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from domuwa.database import db_obj_save, get_db, get_obj_of_type_by_id
from domuwa.game.model import Game
from domuwa.game.schema import GameCategory, GameCreate
from domuwa.player.model import Player
from domuwa.question.model import Question


async def create_game(game: GameCreate, db: Session = Depends(get_db)) -> Game:
    query_filter = Question.game_name == game.name
    if game.category != GameCategory.MIXED.value:
        query_filter = query_filter and Question.game_category == game.category
    questions = db.query(Question).filter(query_filter).all()
    db_game = Game(
        name=game.name,
        category=game.category,
        players=[],
        questions=questions,
    )
    return await db_obj_save(db_game, db)


async def add_player(game_id: int, player_id: int, db: Session = Depends(get_db)) -> Type[Game]:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    game = await get_obj_of_type_by_id(game_id, Game, "Game", db)
    player.game = game
    if player not in game.players:
        await db_obj_save(player, db)
        game.players.append(player)
    return await db_obj_save(game, db)


async def remove_player(game_id: int, player_id: int, db: Session = Depends(get_db)) -> Type[Game]:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    player.game = None
    await db_obj_save(player, db)
    game = await get_obj_of_type_by_id(game_id, Game, "Game", db)
    game.players.remove(player)
    return await db_obj_save(game, db)


async def remove_all_players(game_id: int, db: Session = Depends(get_db)) -> Type[Game]:
    game = await get_obj_of_type_by_id(game_id, Game, "Game", db)
    for player in game.players:
        player.game = None
        await db_obj_save(player, db)
    return await db_obj_save(game, db)
