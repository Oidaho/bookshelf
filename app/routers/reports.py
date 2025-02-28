from datetime import datetime

from db import get_db
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from utils import DateSearch, ListingSearch
from utils.report import ExpiredIssuancesReport
from utils.crud import issuance

router = APIRouter(prefix="/reports")


@router.get("", summary="Get a library report", tags=["Reports"])
async def get_readers(
    search: DateSearch = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Создает отчет об удержаных книгах по каждому читателю и по библиотеке в целом.
    Отправляет отчет в виде стрима флайла формата xslx. (Загрузка файла Excel)
    """
    report_date = datetime.strptime(search.date, "%Y-%m-%d")
    expired_issuances = await issuance.get_all(
        db,
        search=ListingSearch[str](
            search_by="expires_at",
            search_mode="less_than_or_equal",
            search_value=report_date,
        ),
    )

    # * Предаггрегация данных
    data = {}
    for expired_issuance in expired_issuances:
        reader = await expired_issuance.awaitable_attrs.reader
        if not data.get(reader.code):
            data[reader.code] = {"name": reader.full_name, "books": []}

        book = await expired_issuance.awaitable_attrs.book
        author = await book.awaitable_attrs.author

        issuance_data = [
            reader.phone,
            author.name,
            book.title,
            float(round(book.price / 1000, 3)),
            expired_issuance.issuanced_at.strftime("%d.%m.%Y"),
        ]
        data[reader.code]["books"].append(issuance_data)

    # * Создание отчета
    report = ExpiredIssuancesReport(report_date)
    report.construct_report(data)

    # * Стриминг файла в качестве ответа (Загрузка )
    return StreamingResponse(
        report.get_filestream(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=report_{report_date.date()}.xlsx"},
    )
