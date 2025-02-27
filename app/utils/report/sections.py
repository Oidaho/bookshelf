from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, List

from .builder import ReportBuilder
from .styles import TITLE_STYLE, TOTAL_STYLE, HEADER_STYLE, BOOK_STYLE, READER_STYLE


class Section(ABC):
    """Базовый абстрактный класс секции.

    Секция - определенный заготовленный патерн\\обьект, который
    будет размещен на листе ws.
    """

    @abstractmethod
    def render(self, builder: ReportBuilder) -> None:
        """Отрисовывает (размещает) секцию на текущем листе,
        используя методы класса-билдера.

        Args:
            builder (ReportBuilder): Инстанс класса-билдера.
        """
        pass


class TitleSection(Section):
    """Секция заголовка отчета."""

    def __init__(self, report_date: date) -> None:
        self.report_date = report_date

    def render(self, builder: ReportBuilder) -> None:
        title = f"Сведения о читателях, у которых наступил срок возврата на {self.report_date.strftime('%d.%m.%Y')} (ДД.ММ.ГГГГ)"
        builder.add_row([title], TITLE_STYLE)
        builder.merge_cells(1, 5)
        builder.set_row_height(30)


class TableHeaderSection(Section):
    """Секция заголовка таблицы отчета."""

    HEADERS = ["Телефон", "Автор", "Название книги", "Цена книги, тыс. руб.", "Дата выдачи"]

    def __init__(self, column_config: Dict[str, int]):
        self.column_config = column_config

    def render(self, builder: ReportBuilder):
        builder.add_row(self.HEADERS, HEADER_STYLE)
        builder.set_columns_width(self.column_config)


class ReaderSection(Section):
    """Секция читателя в таблице.

    Размещает строки с именем читателя, информацию
    по удержаным книгам и суммарное кол-во книг.
    """

    def __init__(self, reader_name: str, books: List[List[Any]]):
        self.reader_name = reader_name
        self.books = books

    def render(self, builder: ReportBuilder):
        # Заголовок читателя
        builder.add_row([f"Читатель: {self.reader_name}"], READER_STYLE)
        builder.merge_cells(1, 5)

        # Книги
        for book in self.books:
            builder.add_row(book, BOOK_STYLE)

        # Итого по читателю
        builder.add_row(["Итого книг у читателя:", len(self.books), "", "", ""], TOTAL_STYLE)
        builder.merge_cells(2, 5)
        builder.set_row_height(20)


class LibraryTotalSection(Section):
    """Секция суммарного кол-во удержаных книг по библиотеке."""

    def __init__(self, total: int):
        self.total = total

    def render(self, builder: ReportBuilder):
        builder.add_row(["Итого по библиотеке:", self.total, "", ""], TOTAL_STYLE)
        builder.merge_cells(2, 5)
        builder.set_row_height(20)
