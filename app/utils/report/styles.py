from openpyxl.styles import Alignment, Border, Font, Side


class CellStyle:
    def __init__(self, font: Font = None, alignment: Alignment = None, border: Border = None):
        self.font = font
        self.alignment = alignment
        self.border = border

    def apply(self, cell):
        if self.font:
            cell.font = self.font
        if self.alignment:
            cell.alignment = self.alignment
        if self.border:
            cell.border = self.border


TITLE_STYLE = CellStyle(
    font=Font(bold=True, size=14),
    alignment=Alignment(
        horizontal="left",
        vertical="center",
        wrap_text=True,
    ),
)

HEADER_STYLE = CellStyle(
    font=Font(bold=True),
    alignment=Alignment(horizontal="center"),
    border=Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    ),
)

READER_STYLE = CellStyle(
    font=Font(bold=True),
    alignment=Alignment(
        horizontal="left",
        vertical="bottom",
    ),
    border=Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    ),
)

BOOK_STYLE = CellStyle(
    alignment=Alignment(
        horizontal="center",
        vertical="center",
    ),
    border=Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    ),
)

TOTAL_STYLE = CellStyle(
    font=Font(bold=True),
    border=Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="double"),
    ),
    alignment=Alignment(
        horizontal="left",
        vertical="top",
    ),
)
