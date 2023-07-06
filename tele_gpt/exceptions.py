class CustomError(Exception):
    pass


class DBError(CustomError):
    pass


class APIError(CustomError):
    pass

class OpenAIError(CustomError):
    pass
