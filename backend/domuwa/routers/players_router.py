import fastapi
import pydantic
from fastapi import status
from sqlalchemy import orm
from starlette import responses, templating

from domuwa import database as db
from domuwa import models, schemas
from domuwa.services import players_services as services

router = fastapi.APIRouter(prefix="/player", tags=["Player"])
templates = templating.Jinja2Templates(directory="resources/templates")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def create_player(
    request: fastapi.Request,
    name: str,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.PlayerView | templating._TemplateResponse:
    player = validate_player_data(name)
    db_player = services.create_player(player, db_sess)
    return create_player_view(db_player)


@router.get("/{player_id}", response_model=None)
def get_player_by_id(
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.PlayerView | templating._TemplateResponse:
    player = db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
    return create_player_view(player)


@router.get("/", response_model=None)
def get_all_players(
    request: fastapi.Request,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> list[schemas.PlayerView] | templating._TemplateResponse:
    players = db.get_all_objs_of_type(models.Player, db_sess)
    return [create_player_view(player) for player in players]


@router.get("/from_game_room/{game_room_id}", response_model=None)
def get_all_players_from_game_room(
    request: fastapi.Request,
    game_room_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> list[schemas.PlayerView] | templating._TemplateResponse:
    players = services.get_all_players_from_game_room(game_room_id, db_sess)
    return [create_player_view(player) for player in players]


@router.put("/update_name", response_model=None)
def update_player_name(
    request: fastapi.Request,
    player_id: int,
    new_name: str,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.PlayerView | templating._TemplateResponse:
    new_name_player = validate_player_data(new_name)
    player = services.update_player_name(player_id, new_name_player, db_sess)
    return create_player_view(player)


@router.put("/update_score", response_model=None)
def update_player_score(
    request: fastapi.Request,
    player_id: int,
    points: float,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.PlayerView | templating._TemplateResponse:
    player = services.update_player_score(player_id, points, db_sess)
    return create_player_view(player)


@router.put("/reset_game_room", response_model=None)
def reset_player_game_room(
    request: fastapi.Request,
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.PlayerView | templating._TemplateResponse:
    player = services.reset_player_game_room(player_id, db_sess)
    return create_player_view(player)


@router.put("/reset_score", response_model=None)
def reset_player_score(
    request: fastapi.Request,
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.PlayerView | templating._TemplateResponse:
    player = services.reset_player_score(player_id, db_sess)
    return create_player_view(player)


@router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=responses.Response,
    response_model=None,
)
def delete_player(
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> None:
    db.delete_obj(player_id, models.Player, "Player", db_sess)


def validate_player_data(name: str) -> schemas.PlayerSchema:
    try:
        player = schemas.PlayerSchema(name=name)
    except pydantic.ValidationError:
        raise fastapi.HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Invalid name provided",
        )
    return player


def create_player_view(player: models.Player) -> schemas.PlayerView:
    return schemas.PlayerView.model_validate(player)
