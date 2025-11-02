class InvalidCredentialsException(Exception):
    pass


class InvalidMenuOptionException(Exception):
    def __init__(self, message: str | None = None):
        super().__init__(message or "Digite um número inteiro não negativo.")


class InvalidGradeException(Exception):
    pass


class UserCreationError(Exception):
    pass


class InvalidExamDate(Exception):
    pass
