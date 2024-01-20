from itertools import chain
from typing import List, Optional

import pandas as pd
import pyarrow as pa
from arize.pandas.validation import errors as err
from arize.pandas.spans.validation import errors as span_err


# TODO(Kiko): Must validate
# times in ns
# status code values either strings or ints
class SpansValidator:
    def validate_direct_input_types(
        self,
        dataframe: pd.DataFrame,
        model_id: str,
        model_version: Optional[str] = None,
    ) -> List[err.ValidationError]:
        return list(
            chain(
                self._check_field_convertible_to_str(model_id, model_version),
                self._check_dataframe_type(dataframe),
            )
        )

    def validate_dataframe_form(
        self,
        dataframe: pd.DataFrame,
    ) -> List[err.ValidationError]:
        return list(
            chain(
                self._check_dataframe_index(dataframe),
                self._check_dataframe_column_names(dataframe),
                self._check_dataframe_column_content_type(dataframe),
            )
        )

    def validate_dataframe_values(
        self,
        dataframe: pd.DataFrame,
    ) -> List[err.ValidationError]:
        # raise NotImplementedError
        return list(chain())

    def validate_arrow_types(
        self,
        pyarrow_schema: pa.Schema,
    ) -> List[err.ValidationError]:
        # raise NotImplementedError
        return list(chain())

    # -------------------
    # Direct Input Checks
    # -------------------

    @staticmethod
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

    @staticmethod
    def _check_dataframe_type(
        dataframe: pd.DataFrame,
    ) -> List[span_err.InvalidDataFrameType]:
        if not isinstance(dataframe, pd.DataFrame):
            return [span_err.InvalidDataFrameType(dataframe)]
        return []

    # ---------------------
    # DataFrame Form Checks
    # ---------------------

    @staticmethod
    def _check_dataframe_index(dataframe: pd.DataFrame) -> List[err.InvalidDataFrameIndex]:
        if (dataframe.index != dataframe.reset_index(drop=True).index).any():
            return [err.InvalidDataFrameIndex()]
        return []

    @staticmethod
    def _check_dataframe_column_names(
        dataframe: pd.DataFrame,
    ) -> List[span_err.InvalidDataFrameColumnNames]:
        # raise NotImplementedError
        return []

    @staticmethod
    def _check_dataframe_column_content_type(
        dataframe: pd.DataFrame,
    ) -> List[span_err.InvalidDataFrameColumnContentTypes]:
        # raise NotImplementedError
        return []

    # -----------------------
    # DataFrame Values Checks
    # -----------------------

    # -----------------------
    # Arrow Types Checks
    # -----------------------
