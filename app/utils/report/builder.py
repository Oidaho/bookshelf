from typing import Any, Dict, List

from openpyxl.worksheet.worksheet import Worksheet

from .styles import CellStyle


class ReportBuilder:
    def __init__(self, worksheet: Worksheet):
        self.ws = worksheet
        self.ws.title = "Отчет по срокам возврата"
        self.current_row = 1

    def add_row(self, data: List[Any], style: CellStyle = None) -> None:
        self.ws.append(data)
        if style:
            self._apply_style_to_row(self.current_row, style)
        self.current_row += 1

    def merge_cells(self, start_col: int, end_col: int) -> None:
        self.ws.merge_cells(
            start_row=self.current_row - 1,
            end_row=self.current_row - 1,
            start_column=start_col,
            end_column=end_col,
        )

    def set_row_height(self, height: int) -> None:
        self.ws.row_dimensions[self.current_row - 1].height = height

    def set_columns_width(self, config: Dict[str, int]) -> None:
        for col, width in config.items():
            self.ws.column_dimensions[col].width = width

    def _apply_style_to_row(self, row: int, style: CellStyle) -> None:
        for col in range(1, self.ws.max_column + 1):
            style.apply(self.ws.cell(row=row, column=col))
