from datetime import date
from io import BytesIO
from typing import Any, Dict, List

from openpyxl import Workbook
from .builder import ReportBuilder
from .sections import Section, TitleSection, ReaderSection, TableHeaderSection, LibraryTotalSection


class ExpiredIssuancesReport:
    """Класс, создающий отчет по удержаным книгам у читателей и по всей бибилотеке."""

    # Ширина колонок
    COLUMN_CONFIG = {
        "A": 25,  # Телефон
        "B": 30,  # Автор
        "C": 35,  # Название
        "D": 25,  # Цена
        "E": 20,  # Дата
    }

    def __init__(self, report_date: date):
        self.report_date = report_date
        self.wb = Workbook()
        self.builder = ReportBuilder(self.wb.active)
        self.sections: List[Section] = []

    def add_section(self, section: Section):
        """Добавляет секцию к очереди на рендер.

        Args:
            section (Section): Секция листа.
        """
        self.sections.append(section)

    def render_sections(self) -> None:
        """Начинает размещение всех секций на лист ws поочередно."""
        for section in self.sections:
            section.render(self.builder)

    def construct_report(self, data: Dict[str, Dict[str, List[List[Any]]]]) -> None:
        """Формирует отчет из данных по удержаным книгам.

        Args:
            data (Dict[str, Dict[str, List[List[Any]]]]): Аггрегированые данные по удержаным книгам.
        """
        self.add_section(TitleSection(self.report_date))
        self.add_section(TableHeaderSection(self.COLUMN_CONFIG))

        library_total = 0
        for reader_data in data.values():
            print(reader_data)
            library_total += len(reader_data["books"])
            self.add_section(ReaderSection(reader_data["name"], reader_data["books"]))

        self.add_section(LibraryTotalSection(library_total))

        self.render_sections()

    def get_filestream(self) -> BytesIO:
        """Возвращает поток данных Excel-файла.

        Returns:
            BytesIO: Поток байтов, содержащий данные Excel-файла.
        """
        file_stream = BytesIO()
        self.wb.save(file_stream)
        file_stream.seek(0)
        return file_stream
