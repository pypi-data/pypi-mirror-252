from __future__ import annotations

from dataclasses import dataclass
from logging import getLogger
from time import sleep
from typing import Any, List, Callable, Optional

from openai import Embedding as OpenAIEmbedding
from openai.embeddings_utils import cosine_similarity
from openai.error import RateLimitError


@dataclass
class SearchItem:
    item: Any
    embedding: Embedding


@dataclass
class SearchResult:
    item: Any
    similarity: float


Embedding = List[float]


def embedding(
        input_: str,
        model: str = 'text-embedding-ada-002',
        **kwargs
) -> Embedding:
    try:
        full_response = OpenAIEmbedding.create(
            model=model,
            input=input_,
            **kwargs
        )
        response = full_response['data'][0]
    except RateLimitError:
        getLogger("models.basic").info("Retrying due to rate limit")
        sleep(5)
        return embedding(model, input_, **kwargs)
    log_embedding_response(input_)
    return response['embedding']


def search_by_embedding(
        embedding_: Embedding,
        items: List[Any],
        embedding_key: Callable = embedding,
        min_similarity: float = 0,
        max_items: Optional[int] = None
) -> List[SearchResult]:
    results = []
    for item in items:
        item_embedding = embedding_key(item)
        similarity = cosine_similarity(item_embedding, embedding_)
        if similarity > min_similarity:
            results.append(SearchResult(item, similarity))
    sorted_ = sorted(results, key=lambda result: -result.similarity)
    if max_items is None:
        return sorted_
    return sorted_[:max_items]


def search_text_by_text(query: str, items: List[str]) -> List[SearchResult]:
    items = [
        SearchItem(item, text_document_for_text_search_embedding(item))
        for item in items
    ]
    query_embedding = text_query_for_text_search_embedding(query)
    return search_by_embedding(query_embedding, items)


def text_query_for_text_search_embedding(text: str, **kwargs) -> Embedding:
    return embedding('text-search-babbage-query-001', text, **kwargs)


def text_document_for_text_search_embedding(text: str, **kwargs) -> Embedding:
    return embedding('text-search-babbage-doc-001', text, **kwargs)


def search_code_by_text(
        text: str,
        items: List[Any],
        key: Callable = lambda item: item
) -> List[SearchResult]:
    items = [
        SearchItem(item, code_document_for_code_search_embedding(key(item)))
        for item in items
    ]
    query_embedding = text_query_for_code_search_embedding(text)
    return search_by_embedding(query_embedding, items)


def text_query_for_code_search_embedding(text: str, **kwargs) -> Embedding:
    return embedding('code-search-babbage-text-001', text, **kwargs)


def code_document_for_code_search_embedding(code: str, **kwargs) -> Embedding:
    return embedding('code-search-babbage-code-001', code, **kwargs)


def classify_text(text: str, classes: List[str]) -> str:
    if not classes:
        raise ValueError("There must be at least one class")
    results = search_text_by_text(text, classes)
    return results[0].item


def log_embedding_response(input_: str):
    getLogger("models.basic").debug("Embedding")
    getLogger("models.basic").debug(f"Input: {input_}")
