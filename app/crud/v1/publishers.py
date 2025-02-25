from ..base import CRUDBase
from db.models import Publisher


class CRUDPublisher(CRUDBase[Publisher]):
    pass


publisher = CRUDPublisher(Publisher)
