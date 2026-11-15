"""Small, transparent evidence retriever for the ClaimCheck prototype."""
from __future__ import annotations

import math
import re
from pathlib import Path

CORPUS = Path(__file__).with_name("corpus")
STOP_WORDS = set(
    "a an and are as at be by for from how in is it of on or that the to was "
    "what when where which who with".split()
)


def _metadata_and_body(text: str) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {}
    body = text
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()
            body = text[end + 3 :]
    return metadata, body.strip()


def _words(text: str) -> list[str]:
    return [
        word
        for word in re.findall(r"[a-z0-9]+", text.lower())
        if word not in STOP_WORDS
    ]


def load_passages() -> list[dict]:
    passages: list[dict] = []
    for path in sorted(CORPUS.glob("*.md")):
        metadata, body = _metadata_and_body(path.read_text(encoding="utf-8"))
        for paragraph in (part.strip() for part in body.split("\n\n") if part.strip()):
            passages.append(
                {
                    "id": f"{path.name}-{len(passages)}",
                    "source": metadata.get("source", path.name),
                    "section": metadata.get("section", "Unsectioned"),
                    "date": metadata.get("updated", "Unknown"),
                    "text": " ".join(paragraph.split()),
                    "url": metadata.get("url", ""),
                }
            )
    return passages


def search(query: str, limit: int = 4) -> list[dict]:
    """Return the strongest lexical matches with a comparable 0..1 score."""
    query_words = set(_words(query))
    passages = load_passages()
    if not query_words or not passages:
        return []

    document_frequency = {
        word: sum(word in set(_words(passage["text"])) for passage in passages)
        for word in query_words
    }
    results = []
    for passage in passages:
        passage_words = _words(passage["text"])
        if not passage_words:
            continue
        matched = query_words.intersection(passage_words)
        score = sum(
            (math.log((len(passages) + 1) / (document_frequency[word] + 1)) + 1)
            for word in matched
        ) / (len(query_words) * 2)
        result = dict(passage)
        result["score"] = round(min(score, 1.0), 3)
        results.append(result)
    return sorted(results, key=lambda item: item["score"], reverse=True)[:limit]
