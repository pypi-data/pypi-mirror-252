from typing import Any

from arize.pandas.validation.errors import ValidationError

# -------------------
# Direct Input Checks
# -------------------


class InvalidDataFrameType(ValidationError):
    def __repr__(self) -> str:
        return "Invalid_DataFrame_Type"

    def __init__(self, wrong_input: Any) -> None:
        self.wrong_input = wrong_input

    def error_message(self) -> str:
        return (
            "The dataframe must be of type pandas DataFrame. ",
            f"Found {type(self.wrong_input)}",
        )


# ---------------------
# DataFrame Form Checks
# ---------------------


class InvalidDataFrameColumnNames(ValidationError):
    def __repr__(self) -> str:
        return "Invalid_DataFrame_Column_Names"

    def __init__(self, column_names: Any) -> None:
        self.column_names = column_names

    def error_message(self) -> str:
        raise NotImplementedError
        return (f"Found {type(self.column_names)}",)


class InvalidDataFrameColumnContentTypes(ValidationError):
    def __repr__(self) -> str:
        return "Invalid_DataFrame_Column_Content_Types"

    def __init__(self, wrong_cols: Any) -> None:
        self.wrong_cols = wrong_cols

    def error_message(self) -> str:
        raise NotImplementedError
        return (f"Found {type(self.wrong_cols)}",)


# -----------------------
# DataFrame Values Checks
# -----------------------

# -----------------------
# Arrow Types Checks
# -----------------------
