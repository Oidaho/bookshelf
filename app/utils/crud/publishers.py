from db.models import Publisher

from .base import WithHTTPExceptions, WithParameterizedListing


class PublisherCRUD(WithParameterizedListing[Publisher], WithHTTPExceptions[Publisher]):
    """Класс, предоставляющий CRUD операции для сущности Publisher.

    Этот класс наследуется от:
    - `WithParameterizedListing[Publisher]`: Предоставляет функциональность для параметризованного
      получения списка объектов Publisher с поддержкой поиска, сортировки и пагинации.
    - `WithHTTPExceptions[Publisher]`: Добавляет вызов HTTP-исключений при определенных ситуациях,
      которые возникают при исполнении CRUD операций.
    """

    pass


publisher = PublisherCRUD(Publisher)
