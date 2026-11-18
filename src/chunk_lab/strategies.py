from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str


def fixed_size(doc_id: str, text: str, size: int = 220, overlap: int = 40) -> list[Chunk]:
    clean = " ".join(text.split())
    if not clean:
        return []
    out: list[Chunk] = []
    step = max(size - overlap, 1)
    start = 0
    idx = 0
    while start < len(clean):
        end = min(start + size, len(clean))
        out.append(Chunk(f"{doc_id}:fix:{idx}", doc_id, clean[start:end]))
        if end == len(clean):
            break
        start += step
        idx += 1
    return out


def by_paragraph(doc_id: str, text: str, max_chars: int = 320) -> list[Chunk]:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not parts:
        parts = [text.strip()]
    out: list[Chunk] = []
    buf = ""
    idx = 0
    for part in parts:
        candidate = f"{buf}\n\n{part}".strip() if buf else part
        if len(candidate) <= max_chars:
            buf = candidate
            continue
        if buf:
            out.append(Chunk(f"{doc_id}:para:{idx}", doc_id, buf))
            idx += 1
        buf = part
    if buf:
        out.append(Chunk(f"{doc_id}:para:{idx}", doc_id, buf))
    return out


def by_sentence(doc_id: str, text: str, max_chars: int = 260) -> list[Chunk]:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    out: list[Chunk] = []
    buf = ""
    idx = 0
    for sentence in sentences:
        piece = sentence + "."
        candidate = f"{buf} {piece}".strip() if buf else piece
        if len(candidate) <= max_chars:
            buf = candidate
            continue
        if buf:
            out.append(Chunk(f"{doc_id}:sent:{idx}", doc_id, buf))
            idx += 1
        buf = piece
    if buf:
        out.append(Chunk(f"{doc_id}:sent:{idx}", doc_id, buf))
    return out


STRATEGIES = {
    "fixed": lambda doc_id, text: fixed_size(doc_id, text),
    "paragraph": lambda doc_id, text: by_paragraph(doc_id, text),
    "sentence": lambda doc_id, text: by_sentence(doc_id, text),
}
