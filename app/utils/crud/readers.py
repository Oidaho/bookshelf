from .base import CRUD
from db.models import Reader


class ReaderCRUD(CRUD[Reader]):
    pass


reader = ReaderCRUD(Reader)
