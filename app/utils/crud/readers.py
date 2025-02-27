from db.models import Reader

from .base import WithHTTPExceptions, WithParameterizedListing


class ReaderCRUD(WithParameterizedListing[Reader], WithHTTPExceptions[Reader]):
    """Класс, предоставляющий CRUD операции для сущности Reader.

    Этот класс наследуется от:
    - `WithParameterizedListing[Reader]`: Предоставляет функциональность для параметризованного
      получения списка объектов Reader с поддержкой поиска, сортировки и пагинации.
    - `WithHTTPExceptions[Reader]`: Добавляет вызов HTTP-исключений при определенных ситуациях,
      которые возникают при исполнении CRUD операций.
    """

    pass


reader = ReaderCRUD(Reader)
