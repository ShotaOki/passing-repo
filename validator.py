from pydantic_core import PydanticCustomError
from datetime import datetime
from re import match
import pytz
from enum import Enum


VALIDATE_PATTERN_YYYY_MM_DD = r"^\d{4}-\d{2}-\d{2}$"


class ErrorType(Enum):
    """
    異常時に例外として投げるデータタイプ
    """

    # 日時エラー
    DATE_TYPE = "date_type"


class StrValidator:
    """
    文字列を別のフォーマットに変換するバリデータ
    """

    # 対象文字列
    _value: str

    def __init__(self, value: str):
        self._value = value
        if not isinstance(value, str):
            """
            引数が文字列型でないのなら型エラーの例外を投げる
            """
            raise PydanticCustomError(
                "type_error",
                'expected datetime string, got "{wrong_value}"',
                dict(wrong_value=value),
            )

    def validate(self, pattern: str, error_type: ErrorType, error_message: str):
        """
        日時の形式を検証する
        """
        # フォーマットを検証する
        if not match(pattern, self._value):
            raise PydanticCustomError(
                error_type.value,
                '{error_message}, got "{wrong_value}"',
                dict(error_message=error_message, wrong_value=self._value),
            )
        return self

    def to_start_date(self, timezone: str):
        """
        日時文字列を対象日時の最初の秒に変換する
        """
        try:
            # タイムゾーンを参照する
            tz = datetime.strftime(datetime.now(tz=pytz.timezone(timezone)), "%z")
            # 日時を検証、datetime型に変換する
            return datetime.strptime(
                # 対象日の最初の秒を参照する
                self._value + "T00:00:00" + tz,
                # タイムゾーン付きのISOフォーマットとして扱う
                "%Y-%m-%dT%H:%M:%S%z",
            )
        except Exception:
            raise PydanticCustomError(
                ErrorType.DATE_TYPE.value,
                'string is not datetime, got "{wrong_value}"',
                dict(wrong_value=self._value),
            )

    def to_end_date(self, timezone: str):
        """
        日時文字列を対象日時の最後の秒に変換する
        """
        try:
            # タイムゾーンを参照する
            tz = datetime.strftime(datetime.now(tz=pytz.timezone(timezone)), "%z")
            # 日時を検証、datetime型に変換する
            return datetime.strptime(
                # 対象日の最後の秒を参照する
                self._value + "T23:59:59" + tz,
                # タイムゾーン付きのISOフォーマットとして扱う
                "%Y-%m-%dT%H:%M:%S%z",
            )
        except Exception:
            raise PydanticCustomError(
                ErrorType.DATE_TYPE.value,
                'string is not datetime, got "{wrong_value}"',
                dict(wrong_value=self._value),
            )
