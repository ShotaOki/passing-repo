from pydantic import BaseModel, ConfigDict
from pydantic import ValidationError
from type_validator import StartDateTime, EndDateTime


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start_date: StartDateTime
    end_date: EndDateTime


try:
    input = Input(start_date="2021-01-01", end_date="2021-01-01")
    Input.model_validate({"start_date": "2012-01-01", "end_date": "2022-10-01"})

    print(input.start_date.isoformat())
    print(input.end_date.isoformat())

    # print(Input(start_date=2021, end_date="2021-01-01"))
    print(Input(start_date="2021-01-99", end_date="2021-01-01"))
except ValidationError as e:
    err = e.errors()
    print(err[0])
