from fastapi import HTTPException


class PasswordsNotMatchException(HTTPException):
    pass
