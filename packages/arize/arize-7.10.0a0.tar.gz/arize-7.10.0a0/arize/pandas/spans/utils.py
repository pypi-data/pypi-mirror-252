import pandas as pd
import numpy as np
import json
from typing import Iterable, Dict, Any, List, Optional
from arize.utils.logging import logger


from .columns import (
    SPAN_ATTRIBUTES_EMBEDDING_EMBEDDINGS_COL_NAME,
    SPAN_ATTRIBUTES_LLM_INPUT_MESSAGES_COL_NAME,
    SPAN_ATTRIBUTES_LLM_OUTPUT_MESSAGES_COL_NAME,
    SPAN_ATTRIBUTES_RETRIEVAL_DOCUMENTS_COL_NAME,
    SPAN_ATTRIBUTES_RERANKER_INPUT_DOCUMENTS_COL_NAME,
    SPAN_ATTRIBUTES_RERANKER_OUTPUT_DOCUMENTS_COL_NAME,
    SPAN_ATTRIBUTES_LLM_PROMPT_TEMPLATE_VARIABLES_COL_NAME,
)

LIST_OF_OBJECT_COLS = [
    SPAN_ATTRIBUTES_EMBEDDING_EMBEDDINGS_COL_NAME,
    SPAN_ATTRIBUTES_LLM_INPUT_MESSAGES_COL_NAME,
    SPAN_ATTRIBUTES_LLM_OUTPUT_MESSAGES_COL_NAME,
    SPAN_ATTRIBUTES_RETRIEVAL_DOCUMENTS_COL_NAME,
    SPAN_ATTRIBUTES_RERANKER_INPUT_DOCUMENTS_COL_NAME,
    SPAN_ATTRIBUTES_RERANKER_OUTPUT_DOCUMENTS_COL_NAME,
]
OBJECT_COLS = [
    SPAN_ATTRIBUTES_LLM_PROMPT_TEMPLATE_VARIABLES_COL_NAME,
]


# NOTE(Kiko): This is a bit of a mess, some fields have dictionaries, some
# others have json strings...
# "attributes.embedding.embeddings",
# "attributes.llm.input_messages",
# "attributes.llm.output_messages",
# "attributes.retrieval.documents",
# "attributes.reranker.input_documents"
# "attributes.reranker.output_documents"
# And, inside each message
# "message.tool_calls", fortunately seems like it can be jsonifyed automatically as long as there is no numpy arrays


# NOTE(Kiko): Yet another problem: np arrays are not json serializable.
# Hence, I will assume the embeddings come as lists, not arrays
def jsonify_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col_name in OBJECT_COLS:
        if col_name not in df.columns:
            logger.debug(f"passing on {col_name}")
            continue
        logger.debug(f"jsonifying {col_name}")
        df[col_name] = df[col_name].apply(lambda d: _jsonify_dict(d))

    for col_name in LIST_OF_OBJECT_COLS:
        if col_name not in df.columns:
            logger.debug(f"passing on {col_name}")
            continue
        logger.debug(f"jsonifying {col_name}")
        df[col_name] = df[col_name].apply(
            lambda list_of_dicts: _jsonify_list_of_dicts(list_of_dicts)
        )
    return df


def _jsonify_list_of_dicts(
    list_of_dicts: Optional[Iterable[Dict[str, Any]]]
) -> Optional[List[str]]:
    if list_of_dicts is None:
        return None
    list_of_json = []
    for d in list_of_dicts:
        list_of_json.append(_jsonify_dict(d))
    return list_of_json


def _jsonify_dict(d: Optional[Dict[str, Any]]) -> Optional[str]:
    if d is None:
        return None
    new_d = {}
    for k, v in d.items():
        if isinstance(v, np.ndarray):
            new_d[k] = v.tolist()
        else:
            new_d[k] = v
    return json.dumps(new_d, ensure_ascii=False)
