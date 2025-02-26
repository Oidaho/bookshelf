from .base import CRUD
from db.models import Publisher


class PublisherCRUD(CRUD[Publisher]):
    pass


publisher = PublisherCRUD(Publisher)
