from functools import wraps
from http import HTTPStatus

import typer


def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            message = typer.style(f"Ops! We found an error: {str(e)}",
                                  fg=typer.colors.RED, bold=True)
            typer.echo(message)
    return wrapper


class Error(Exception):
    name = None
    description = None
    status = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.status = kwargs.get("status")

    def __str__(self):
        return self.description

    def to_dict(self):
        return {
            'error': {
                'name': self.name,
                'description': self.description,
            }}


class AWSCredentialsNotFound(Error):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "credentials-not-found"
        self.description = "You must configurate your aws credentials at li before using aws commands." \
                           " Try: > li aws configure"
        self.status = HTTPStatus.NOT_FOUND
