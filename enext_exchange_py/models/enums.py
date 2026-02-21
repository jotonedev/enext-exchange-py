import enum

__all__ = ["DownloadFormat", "DecimalSeparator", "DateFormat"]


class DownloadFormat(enum.StrEnum):
    MS_EXCEL = "xls"
    CSV = "csv"
    TXT = "txt"


class DecimalSeparator(enum.Enum):
    DOT = "."
    COMMA = ","


class DateFormat(enum.Enum):
    DD_MM_YYYY = "d/m/Y"
    MM_DD_YYYY = "m/d/Y"
