from db.models import Publisher

from .base import CRUD


class PublisherCRUD(CRUD[Publisher]):
    pass


publisher = PublisherCRUD(Publisher)
