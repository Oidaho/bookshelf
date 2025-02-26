from db.models import Reader

from .base import CRUD


class ReaderCRUD(CRUD[Reader]):
    pass


reader = ReaderCRUD(Reader)
