# ClaimCheck

ClaimCheck is a small, local-first prototype for **evaluating the reliability of academic information produced by generative AI**. A student enters one AI-generated claim and receives a transparent evidence trail, a cautious verdict, a confidence indicator, and limitations to consider before citing the claim.

## What is included

- **Evidence-grounded checking:** a transparent lexical retriever searches `corpus/` and shows source, section, date, relevance score, and DOI/URL metadata.
- **Uncertainty by design:** related evidence is labelled *Partially supported* rather than being presented as proof. Unsupported claims produce *Unable to verify*.
- **Student control:** users can choose strict, balanced, or exploratory checking, choose how many evidence passages to inspect, edit the claim, mark it unverified, or record that it should be used cautiously.
- **Recoverable fallback:** an unverified claim provides a pre-filled Google Scholar search link. The local app does not call Google Scholar; the student chooses whether to leave the local workflow.
- **Human-in-the-loop workflow:** the next step tells the student to inspect the original source, its population, method, date, and limits.
- **Accessible interaction:** responsive layout, keyboard-friendly controls, visible focus states, semantic labels, live result updates, adjustable text size, and light/dark mode.
- **Privacy-friendly development:** standard-library Python only, no API key, no network request, and no user claims persisted by the app.

## Run it

Requirements: Python 3.10 or newer.

```bash
cd Project
python app.py
```

Open <http://localhost:8000>. Use **Try an example** or paste a single factual claim. To use another port:

```bash
python app.py --port 8001
```

The JSON endpoint is `POST /api/evaluate` with `{"claim": "..."}`. A claim is limited to 500 characters. The retriever can be checked independently:

```bash
python -c "from retrieve import search; print(search('retrieval practice retention')[0])"
```

## Development decisions

The prototype deliberately does not call a generative model. This keeps the demonstration reproducible and makes the model/system boundary clear: the system retrieves and displays evidence, while the student makes the final academic judgement. The relevance score is a ranking signal, **not a probability that a claim is true**.

The checking modes change the minimum relevance required before evidence is used:

- **Strict:** only stronger matches are included.
- **Balanced:** the recommended default.
- **Exploratory:** weaker passages can be inspected as leads, but should not be treated as support.

When a claim includes absolute wording such as “all”, “never”, “proves”, or
“guarantees”, the interface highlights that wording for human review. This is
an interaction warning, not an automatic correction.

To add evidence, create a Markdown file in `corpus/` with optional front matter:

```text
---
source: Author (year), Journal
section: Section name
updated: 2026-01-01
url: https://doi.org/...
---
One or more evidence paragraphs.
```

## Evaluation plan

For the project report, test at least:

1. A claim closely matching a source: it should be supported and show provenance.
2. A claim related to, but stronger than, a source: it should be partially supported.
3. An unrelated or absent claim: it should say unable to verify and recommend finding a current source.
4. Empty and overlong input: the interface should show an actionable validation error.
5. Narrow and wide screens plus dark mode: content must remain readable and controls usable by keyboard.

## Scope and limitations

This is a teaching/research prototype, not an automated fact checker. It does not assess study quality, source authority, contradictions across papers, citation correctness, or live web content. Lexical overlap can miss paraphrases and can retrieve a relevant passage that does not prove a claim. A production system would need curated scholarly APIs, duplicate/version handling, claim decomposition, stronger citation parsing, and user testing with students.
