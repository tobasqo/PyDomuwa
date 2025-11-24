from fastapi import HTTPException, status


class ModelNotFoundError(Exception):
    pass


class RelationModelNotFoundError(Exception):
    def __init__(self, message: str, *args) -> None:
        self.message = message
        super().__init__(self.message, *args)


class InvalidModelInputError(Exception):
    pass


class ModelNotFoundHttpException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)


class RelationModelNotFoundHttpException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)


class InvalidRequestBodyHttpException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)
