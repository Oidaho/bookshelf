from .base import CRUDBase
from db.models import Author


class CRUDAuthor(CRUDBase[Author]):
    pass


author = CRUDAuthor(Author)
