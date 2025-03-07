from pydantic import BaseModel

from domuwa.answers.schemas import *  # noqa: F403
from domuwa.auth.schemas import *  # noqa: F403
from domuwa.core.schemas import *  # noqa: F403
from domuwa.game_categories.schemas import *  # noqa: F403
from domuwa.game_rooms.schemas import *  # noqa: F403
from domuwa.game_types.schemas import *  # noqa: F403
from domuwa.players.schemas import *  # noqa: F403
from domuwa.qna_categories.schemas import *  # noqa: F403
from domuwa.questions.schemas import *  # noqa: F403
from domuwa.users.schemas import *  # noqa: F403


def get_subclasses(kls: type[BaseModel]):
    for subclass in kls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


models = get_subclasses(BaseModel)
for cls in models:
    cls.model_rebuild()
