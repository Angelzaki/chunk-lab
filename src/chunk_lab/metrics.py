from __future__ import annotations

import math
import re
from collections import Counter

from chunk_lab.strategies import Chunk

TOKEN = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text)]


def retrieval_hit(chunks: list[Chunk], query: str, expected_doc: str, k: int = 3) -> bool:
    if not chunks:
        return False
    tokenized = [tokenize(c.text) for c in chunks]
    df: Counter[str] = Counter()
    for tokens in tokenized:
        df.update(set(tokens))
    n = len(tokenized)
    idf = {t: math.log((n + 1) / (f + 1)) + 1.0 for t, f in df.items()}

    def vec(tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        length = len(tokens) or 1
        return {t: (c / length) * idf.get(t, 0.0) for t, c in tf.items()}

    def cosine(a: dict[str, float], b: dict[str, float]) -> float:
        keys = set(a) | set(b)
        if not keys:
            return 0.0
        dot = sum(a.get(x, 0.0) * b.get(x, 0.0) for x in keys)
        na = math.sqrt(sum(v * v for v in a.values()) or 1.0)
        nb = math.sqrt(sum(v * v for v in b.values()) or 1.0)
        return dot / (na * nb)

    q = vec(tokenize(query))
    ranked = sorted(
        ((cosine(q, vec(tokens)), chunk) for chunk, tokens in zip(chunks, tokenized)),
        key=lambda x: x[0],
        reverse=True,
    )
    return any(chunk.doc_id == expected_doc for _, chunk in ranked[:k])


def strategy_stats(chunks: list[Chunk]) -> dict:
    lengths = [len(c.text) for c in chunks]
    return {
        "chunks": len(chunks),
        "avg_len": round(sum(lengths) / len(lengths), 1) if lengths else 0,
        "min_len": min(lengths) if lengths else 0,
        "max_len": max(lengths) if lengths else 0,
    }
