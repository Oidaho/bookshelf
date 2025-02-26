from db.models import Author

from .base import CRUD


class AuthorCRUD(CRUD[Author]):
    pass


author = AuthorCRUD(Author)
