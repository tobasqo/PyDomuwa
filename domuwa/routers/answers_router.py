from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette import templating

from domuwa import config
from domuwa.database import (
    db_obj_delete,
    get_all_objs_of_type,
    get_db,
    get_obj_of_type_by_id,
)
from domuwa.models import Answer
from domuwa.schemas import (
    AnswerSchema,
    AnswerView,
    AnswerWithQuestionView,
    QuestionView,
)
from domuwa.services import answers_services as services
from domuwa.utils.logging import get_logger

logger = get_logger("domuwa")

router = APIRouter(prefix="/answer", tags=["Answer"])
templates = templating.Jinja2Templates(directory="resources/templates")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_answer(
    request: Request,
    author: str,
    text: str,
    question_id: int,
    correct: bool = False,
    db: Session = Depends(get_db),
) -> AnswerWithQuestionView | templating._TemplateResponse:
    answer_view = validate_answer_data(author, text, correct, question_id)
    logger.debug(f"{answer_view=}")
    db_answer = await services.create_answer(answer_view, db)
    answer_view = create_answer_view_with_question(db_answer)
    if config.TESTING:
        return answer_view
    ctx = {"request": request, "answer": answer_view.model_dump()}
    return templates.TemplateResponse("create_answer.html", ctx)


@router.get("/{answer_id}", response_model=AnswerWithQuestionView)
async def get_answer_by_id(
    request: Request,
    answer_id: int,
    db: Session = Depends(get_db),
) -> AnswerWithQuestionView | templating._TemplateResponse:
    answer = await get_obj_of_type_by_id(answer_id, Answer, "Answer", db)
    answer_view = create_answer_view_with_question(answer)
    if config.TESTING:
        return answer_view
    ctx = {"request": request, answer: answer_view.model_dump()}
    return templates.TemplateResponse("get_answer.html", ctx)


@router.get("/")
async def get_all_answers(
    request: Request,
    db: Session = Depends(get_db),
) -> list[AnswerWithQuestionView] | templating._TemplateResponse:
    answers = await get_all_objs_of_type(Answer, db)
    answer_views = [create_answer_view_with_question(answer) for answer in answers]
    if config.TESTING:
        return answer_views
    ctx = {
        "request": request,
        "answers": [answer_view.model_dump() for answer_view in answer_views],
    }
    return templates.TemplateResponse("get_all_answers.html", ctx)


@router.get("/for_question/{question_id}")
async def get_answers_for_question(
    request: Request,
    question_id: int,
    db: Session = Depends(get_db),
) -> list[AnswerView] | templating._TemplateResponse:
    answers = await services.get_answers_for_question(question_id, db)
    answer_views = [create_answer_view(answer) for answer in answers]
    if config.TESTING:
        return answer_views
    ctx = {
        "request": request,
        "answers": [answer_view.model_dump() for answer_view in answer_views],
    }
    return templates.TemplateResponse("get_answers_for_question.html", ctx)


@router.put("/")
async def update_answer(
    request: Request,
    answer_id: int,
    author: str,
    text: str,
    correct: bool,
    question_id: int,
    db: Session = Depends(get_db),
) -> AnswerWithQuestionView | templating._TemplateResponse:
    modified_answer = validate_answer_data(author, text, correct, question_id)
    answer = await services.update_answer(answer_id, modified_answer, db)
    answer_view = create_answer_view_with_question(answer)
    if config.TESTING:
        return answer_view
    ctx = {"request": request, "answer": answer_view.model_dump()}
    return templates.TemplateResponse("update_answer.html", ctx)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_answer(answer_id: int, db: Session = Depends(get_db)) -> None:
    await db_obj_delete(answer_id, Answer, "Answer", db)


def validate_answer_data(
    author: str,
    text: str,
    correct: bool,
    question_id: int,
) -> AnswerSchema:
    try:
        answer = AnswerSchema(
            author=author,
            text=text,
            correct=correct,
            question_id=question_id,
        )
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    return answer


def create_answer_view(answer: Answer | Type[Answer]) -> AnswerView:
    return AnswerView.model_validate(answer)


def create_answer_view_with_question(
    answer: Answer | Type[Answer],
) -> AnswerWithQuestionView:
    return AnswerWithQuestionView(
        id=answer.id,  # type: ignore
        author=answer.author,  # type: ignore
        text=answer.text,  # type: ignore
        correct=answer.correct,  # type: ignore
        question_id=answer.question_id,  # type: ignore
        question=QuestionView.model_validate(answer.question),
    )