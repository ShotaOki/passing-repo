from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from datetime import datetime
from validator import StrValidator, VALIDATE_PATTERN_YYYY_MM_DD, ErrorType
import os

# タイムゾーンを環境変数から参照する
timezone = os.environ.get("TIMEZONE", "Asia/Tokyo")

# Pydantic検証型: 開始日時
StartDateTime = Annotated[
    datetime,  # datetime型として扱う
    BeforeValidator(
        lambda x: StrValidator(x)
        .validate(  # YYYY-MM-DD形式であることを検証する
            pattern=VALIDATE_PATTERN_YYYY_MM_DD,
            error_type=ErrorType.DATE_TYPE,
            error_message="date format should be YYYY-MM-DD",
        )
        .to_start_date(timezone)  # 対象日の開始時間を参照する
    ),
]

# Pydantic検証型: 終了日時
EndDateTime = Annotated[
    datetime,  # datetime型として扱う
    BeforeValidator(
        lambda x: StrValidator(x)
        .validate(  # YYYY-MM-DD形式であることを検証する
            pattern=VALIDATE_PATTERN_YYYY_MM_DD,
            error_type=ErrorType.DATE_TYPE,
            error_message="date format should be YYYY-MM-DD",
        )
        .to_end_date(timezone)  # 対象日の終了時間を参照する
    ),
]
