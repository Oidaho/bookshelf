from db.models import Reader

from .base import WithHTTPExceptions, WithParameterizedListing


class ReaderCRUD(WithParameterizedListing[Reader], WithHTTPExceptions[Reader]):
    pass


reader = ReaderCRUD(Reader)
