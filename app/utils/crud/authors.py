from db.models import Author

from .base import WithHTTPExceptions, WithParameterizedListing


class AuthorCRUD(WithParameterizedListing[Author], WithHTTPExceptions[Author]):
    """Класс, предоставляющий CRUD операции для сущности Author.

    Этот класс наследуется от:
    - `WithParameterizedListing[Author]`: Предоставляет функциональность для параметризованного
      получения списка объектов Author с поддержкой поиска, сортировки и пагинации.
    - `WithHTTPExceptions[Author]`: Добавляет вызов HTTP-исключений при определенных ситуациях,
      которые возникают при исполнении CRUD операций.
    """

    pass


author = AuthorCRUD(Author)
