from itertools import chain
from pandas.api.types import is_bool_dtype, is_numeric_dtype
from datetime import datetime

from typing import List, Optional, Any

import pandas as pd
import pyarrow as pa
from arize.pandas.spans.validation import errors as span_err
from arize.pandas.validation import errors as err
from arize.utils.logging import logger
from arize.utils.utils import log_a_list
from arize.utils.types import is_array_of, is_list_of, is_dict_of, is_json_str
from arize.pandas.spans.columns import (
    # All openinference columns
    SPAN_OPEN_INFERENCE_COLUMN_NAMES,
    # Columns with list of dictionaries in them
    LIST_OF_DICT_COLS,
    # Columns with dictionaries in them
    DICT_COLS,
    # Columns with JSON strings in them
    JSON_STR_COLS,
    # Columns with numbers in them
    NUM_COLS,
    # Columns with booleans in them
    BOOL_COLS,
    # Columns with times in them in many different format
    TIME_COLS,
)


# TODO(Kiko): Must validate
# times in ns
# status code values either strings or ints
def validate_argument_types(
    dataframe: pd.DataFrame,
    model_id: str,
    dt_fmt: str,
    model_version: Optional[str] = None,
) -> List[err.ValidationError]:
    return list(
        chain(
            _check_field_convertible_to_str(model_id, model_version),
            _check_dataframe_type(dataframe),
            _check_datetime_format_type(dt_fmt),
        )
    )


def validate_dataframe_form(
    dataframe: pd.DataFrame,
) -> List[err.ValidationError]:
    _warning_dataframe_column_names(dataframe)
    return list(
        chain(
            _check_dataframe_index(dataframe),
            _check_dataframe_column_content_type(dataframe),
        )
    )


def validate_dataframe_values(
    dataframe: pd.DataFrame,
) -> List[err.ValidationError]:
    logger.warning("validate_dataframe_values is not implemented")
    return list(chain())


def validate_arrow_types(
    pyarrow_schema: pa.Schema,
) -> List[err.ValidationError]:
    logger.warning("validate_arrow_types is not implemented")
    return list(chain())


# -------------------
# Direct Input Checks
# -------------------


def _check_field_convertible_to_str(
    model_id: str,
    model_version: str,
) -> List[err.InvalidFieldTypeConversion]:
    # converting to a set first makes the checks run a lot faster
    wrong_fields = []
    if model_id is not None and not isinstance(model_id, str):
        try:
            str(model_id)
        except Exception:
            wrong_fields.append("model_id")
    if model_version is not None and not isinstance(model_version, str):
        try:
            str(model_version)
        except Exception:
            wrong_fields.append("model_version")

    if wrong_fields:
        return [err.InvalidFieldTypeConversion(wrong_fields, "string")]
    return []


def _check_dataframe_type(
    dataframe: Any,
) -> List[span_err.InvalidTypeArgument]:
    if not isinstance(dataframe, pd.DataFrame):
        return [
            span_err.InvalidTypeArgument(
                wrong_arg=dataframe,
                arg_name="dataframe",
                arg_type="pandas DataFrame",
            )
        ]
    return []


def _check_datetime_format_type(
    dt_fmt: Any,
) -> List[span_err.InvalidTypeArgument]:
    if not isinstance(dt_fmt, str):
        return [
            span_err.InvalidTypeArgument(
                wrong_arg=dt_fmt,
                arg_name="dateTime format",
                arg_type="string",
            )
        ]
    return []


# ---------------------
# DataFrame Form Checks
# ---------------------


def _check_dataframe_index(dataframe: pd.DataFrame) -> List[err.InvalidDataFrameIndex]:
    if (dataframe.index != dataframe.reset_index(drop=True).index).any():
        return [err.InvalidDataFrameIndex()]
    return []


def _warning_dataframe_column_names(
    df: pd.DataFrame,
) -> None:
    extra_cols = [col for col in df.columns if col not in SPAN_OPEN_INFERENCE_COLUMN_NAMES]
    if extra_cols:
        logger.warning(
            "The following columns are not part of the Open Inference Specification "
            f"and will be ignored: {log_a_list(list_of_str=extra_cols, join_word='and')}"
        )
    return None


# TODO(Kiko): Performance improvements
# We should try using:
# - Pandas any() and all() functions together with apply(), or
# - A combination of the following type checker functions from Pandas, i.e,
#   is_float_dtype. See link below
# https://github.com/pandas-dev/pandas/blob/f538741432edf55c6b9fb5d0d496d2dd1d7c2457/pandas/core/dtypes/common.py
def _check_dataframe_column_content_type(
    df: pd.DataFrame,
) -> List[span_err.InvalidDataFrameColumnContentTypes]:
    wrong_lists_of_dicts_cols = []
    wrong_dicts_cols = []
    wrong_numeric_cols = []
    wrong_bools_cols = []
    wrong_timestamp_cols = []
    wrong_JSON_cols = []
    wrong_string_cols = []
    # TODO(Kiko): Must also skip the NaN values, not just None
    for col in SPAN_OPEN_INFERENCE_COLUMN_NAMES:
        if col not in df.columns:
            continue
        if col in LIST_OF_DICT_COLS:
            for row in df[col]:
                if row is None:
                    continue
                if not (is_list_of(row, dict) or is_array_of(row, dict)) or not all(
                    is_dict_of(val, key_allowed_types=str) for val in row
                ):
                    wrong_lists_of_dicts_cols.append(col)
                    break
        elif col in DICT_COLS:
            if not all(
                is_dict_of(row, key_allowed_types=str) if row is not None else True
                for row in df[col]
            ):
                wrong_dicts_cols.append(col)
        elif col in NUM_COLS:
            if not is_numeric_dtype(df[col]):
                wrong_numeric_cols.append(col)
        elif col in BOOL_COLS:
            if not is_bool_dtype(df[col]):
                wrong_bools_cols.append(col)
        elif col in TIME_COLS:
            # Accept strings and datetime objects
            if not all(
                isinstance(row, str) or isinstance(row, datetime) if row is not None else True
                for row in df[col]
            ):
                wrong_timestamp_cols.append(col)
        elif col in JSON_STR_COLS:
            # We check the correctness of the JSON strings when we check the values
            # of the data in the dataframe
            if not all(isinstance(row, str) if row is not None else True for row in df[col]):
                wrong_JSON_cols.append(col)
        else:
            if not all(isinstance(row, str) if row is not None else True for row in df[col]):
                wrong_string_cols.append(col)

    if (
        wrong_lists_of_dicts_cols
        or wrong_dicts_cols
        or wrong_numeric_cols
        or wrong_bools_cols
        or wrong_timestamp_cols
        or wrong_JSON_cols
        or wrong_string_cols
    ):
        wrong_cols = {
            "lists of dictionaries with string keys": wrong_lists_of_dicts_cols,
            "dictionaries with string keys": wrong_dicts_cols,
            "ints or floats": wrong_numeric_cols,
            "bools": wrong_bools_cols,
            "datetime objects or formatted strings": wrong_timestamp_cols,
            "JSON strings": wrong_JSON_cols,
            "strings": wrong_string_cols,
        }
        return [span_err.InvalidDataFrameColumnContentTypes(wrong_cols)]
    return []


# -----------------------
# DataFrame Values Checks
# -----------------------

# -----------------------
# Arrow Types Checks
# -----------------------
