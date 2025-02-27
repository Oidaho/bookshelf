from db.models import Publisher

from .base import WithHTTPExceptions, WithParameterizedListing


class PublisherCRUD(WithParameterizedListing[Publisher], WithHTTPExceptions[Publisher]):
    pass


publisher = PublisherCRUD(Publisher)
