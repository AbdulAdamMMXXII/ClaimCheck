"""Run the local ClaimCheck prototype with: python app.py."""
from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote_plus, urlparse

from retrieve import search

ROOT = Path(__file__).parent
MINIMUM_EVIDENCE_SCORE = 0.18
CHECK_MODES = {
    "strict": {"threshold": 0.30, "label": "Strict"},
    "balanced": {"threshold": 0.18, "label": "Balanced"},
    "exploratory": {"threshold": 0.08, "label": "Exploratory"},
}


def _normalise_claim(claim: str) -> str:
    return re.sub(r"\s+", " ", claim).strip()


def evaluate_claim(claim: str, mode: str = "balanced", evidence_limit: int = 4) -> dict:
    """Evaluate one claim and expose the reasoning boundary to the interface."""
    claim = _normalise_claim(claim)
    if not claim:
        raise ValueError("Enter an academic claim to check.")
    if len(claim) > 500:
        raise ValueError("Keep the claim to 500 characters or fewer.")
    if mode not in CHECK_MODES:
        raise ValueError("Choose a valid checking mode.")
    if evidence_limit not in (2, 4, 6):
        raise ValueError("Choose a valid evidence limit.")

    threshold = CHECK_MODES[mode]["threshold"]
    evidence = search(claim, limit=evidence_limit)
    usable = [item for item in evidence if item["score"] >= threshold]
    scholar_url = "https://scholar.google.com/scholar?q=" + quote_plus(claim)
    strong_terms = re.findall(
        r"\b(always|all|none|never|proves?|guarantees?|certainly|definitively)\b",
        claim.lower(),
    )
    wording_note = (
        "The wording includes absolute terms (" + ", ".join(sorted(set(strong_terms)))
        + "). Check whether the source really supports that strength."
        if strong_terms
        else None
    )
    if not usable:
        return {
            "verdict": "Unable to verify",
            "status": "unknown",
            "confidence": 0.0,
            "summary": (
                "No sufficiently relevant source was found in the local evidence set "
                f"using {CHECK_MODES[mode]['label'].lower()} checking."
            ),
            "next_step": "Find a current scholarly source and compare its methods and context.",
            "evidence": evidence,
            "limitations": [
                "This prototype cannot assess claims outside its supplied evidence set.",
                "Google Scholar opens an external search and is not queried by this local app.",
            ],
            "scholar_url": scholar_url,
            "wording_note": wording_note,
            "mode": mode,
        }

    top = usable[0]
    confidence = round(min(top["score"] * 1.35, 0.95), 2)
    claim_words = set(retrieve_words(claim))
    evidence_words = set(retrieve_words(top["text"]))
    overlap = len(claim_words.intersection(evidence_words)) / max(len(claim_words), 1)
    if overlap >= 0.65:
        verdict, status = "Supported by retrieved evidence", "supported"
        summary = "The claim shares substantial wording with the retrieved source. Check the original study before citing it."
    else:
        verdict, status = "Partially supported", "partial"
        summary = "The evidence is related, but it does not establish every part of the claim."
    return {
        "verdict": verdict,
        "status": status,
        "confidence": confidence,
        "summary": summary,
        "next_step": "Read the original source and confirm population, date, method, and limits.",
        "evidence": usable,
        "limitations": [
            "Retrieval relevance is not the same as truth or causal evidence.",
            "The result is a decision aid, not a substitute for academic judgement.",
        ],
        "scholar_url": scholar_url,
        "wording_note": wording_note,
        "mode": mode,
    }


def retrieve_words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        if urlparse(self.path).path != "/":
            self._send(404, b"Not found", "text/plain; charset=utf-8")
            return
        self._send(200, (ROOT / "index.html").read_bytes(), "text/html; charset=utf-8")

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/evaluate":
            self._send(404, b"Not found", "text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError("Request body must be a JSON object.")
            result = evaluate_claim(
                body.get("claim", ""),
                mode=body.get("mode", "balanced"),
                evidence_limit=body.get("evidence_limit", 4),
            )
            self._send(200, json.dumps(result).encode(), "application/json")
        except (ValueError, json.JSONDecodeError, TypeError) as error:
            self._send(400, json.dumps({"error": str(error)}).encode(), "application/json")

    def log_message(self, *_args) -> None:
        return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run ClaimCheck locally.")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    print(f"ClaimCheck running at http://localhost:{args.port}")
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
