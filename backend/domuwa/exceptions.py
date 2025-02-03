from fastapi import HTTPException, status


class ModelNotFoundError(Exception):
    pass


class InvalidModelInputError(Exception):
    pass


class ModelNotFoundHttpException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)


class InvalidRequestBodyHttpException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)
