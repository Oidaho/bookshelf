from .base import CRUD
from db.models import Author


class AuthorCRUD(CRUD[Author]):
    pass


author = AuthorCRUD(Author)
