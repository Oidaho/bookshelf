from db.models import Author

from .base import WithHTTPExceptions, WithParameterizedListing


class AuthorCRUD(WithParameterizedListing[Author], WithHTTPExceptions[Author]):
    pass


author = AuthorCRUD(Author)
