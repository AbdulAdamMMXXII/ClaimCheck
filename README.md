# ClaimCheck

**README prose word count: approximately 800 words (commands and code excluded).**

ClaimCheck is a local-first prototype for **evaluating the reliability of
academic information produced by generative AI**. A student enters one
AI-generated claim and receives a transparent evidence trail, a cautious
verdict, a relevance indicator and limitations to consider before citing it.

## Project status

### Implemented and runnable

- Local Python HTTP service and browser interface.
- Markdown evidence corpus with source, section, date and DOI/URL metadata.
- Transparent lexical retrieval with relevance ranking.
- Three bounded outcomes: **Supported by retrieved evidence**, **Partially
  supported** and **Unable to verify**.
- Strict, balanced and exploratory checking modes, plus evidence-count control.
- Absolute-wording warning for terms such as *all*, *never*, *proves* and
  *guarantees*.
- Student controls to edit a claim, mark it unverified or record cautious use.
- Responsive interface, keyboard focus states, light/dark mode and adjustable
  text size.
- User-triggered Google Scholar fallback for an unverified claim.

### Simulated or deliberately bounded

- The relevance score is a ranking signal, not a probability that a claim is
  true.
- The system does not perform semantic entailment, peer-review assessment,
  causal analysis or contradiction detection.
- The local corpus represents a small evidence set; it is not a live academic
  index.
- “Mark unverified” and “Use cautiously” provide session feedback only; claims
  are not saved.
- Google Scholar is opened only through a user-selected external link. The
  local app does not query it.

### Planned or unfinished

- Curated scholarly API retrieval and source-accessibility checks.
- Structured comparison of a claim's population, method, result and limits.
- Citation parsing, duplicate/version handling and claim decomposition.
- Privacy-conscious saved claims and user testing with students.

These items are labelled as planned in the report and are not presented as
developed functionality.

## Technology stack

| Technology | Purpose |
|---|---|
| Python 3.10+ standard library | HTTP server, input validation, JSON API and filesystem access |
| HTML, CSS and browser JavaScript | Responsive interface, controls, live result rendering, theme and text-size settings |
| Markdown | Human-readable local evidence corpus and metadata |
| SVG | Architecture diagram and interaction storyboards in `Graphs/` |
| No runtime model | Deliberately preserves a reproducible boundary: ClaimCheck retrieves and displays evidence; the student judges it |

### AI tools used during development

The **Copilot SDK in VS Code** was used as a development assistant for
understanding requirements, comparing design options, drafting and improving
code and documentation, planning tests, and creating and refining graph
layouts and Mermaid instructions. It is not part of the deployed application:
ClaimCheck uses no AI model at runtime. A future scholarly retrieval provider
is still undecided because coverage, authority, rate limits, licensing and
privacy would need evaluation before implementation.

No external Python packages, database, API key or network request is required
for the core application. The only external option is the Google Scholar link
chosen by the user after an unverified result.

## Running and inspecting the work

Requirements: Python 3.10 or newer.

```bash
cd "ClaimCheck system"
python3 app.py
```

Open <http://localhost:8000>. Select **Try an example**, enter a single claim,
choose a checking mode and inspect the evidence trail. Use `--port 8001` for
another port:

```bash
python3 app.py --port 8001
```

The JSON endpoint accepts `POST /api/evaluate`:

```bash
curl -s http://localhost:8000/api/evaluate \
  -H 'Content-Type: application/json' \
  -d '{"claim":"Retrieval practice improves long-term retention.","mode":"balanced","evidence_limit":4}'
```

Inspect the retriever without starting the server:

```bash
cd "ClaimCheck system"
python3 -c "from retrieve import search; print(search('retrieval practice retention')[0])"
python3 -m py_compile app.py retrieve.py
```

Expected checks include a supported result for the retrieval-practice example,
a partial result for an exaggerated version, and **Unable to verify** for an
unrelated claim. The interface and API run offline; only the optional Scholar
search requires internet access.

## Development record

The public repository history is available at
[github.com/AbdulAdamMMXXII/ClaimCheck/commits/main](https://github.com/AbdulAdamMMXXII/ClaimCheck/commits/main).

- [Initial commit](https://github.com/AbdulAdamMMXXII/ClaimCheck/commit/1b725c1c8db0033c8571d48b9f798239a60b630a):
  established the ClaimCheck repository and prototype baseline.
- [Add files via upload](https://github.com/AbdulAdamMMXXII/ClaimCheck/commit/8efcc432f012c8701d7ce3aef840ed2ed39e6378):
  added the runnable project material and local evidence files.
- [Enhance README with detailed project overview](https://github.com/AbdulAdamMMXXII/ClaimCheck/commit/7061461cedf75822363d3919c60d1794b5f31fdc):
  documented the prototype, development decisions, evaluation plan and
  limitations.
- [Revise README with comprehensive project information](https://github.com/AbdulAdamMMXXII/ClaimCheck/commit/bcb3c40e9fad007e480ee010cbc7c8aad2880545):
  expanded the project details, usage instructions and evaluation plan.
- [Update README with detailed project information](https://github.com/AbdulAdamMMXXII/ClaimCheck/commit/b59b4c1019e532912c775a793bf2b42100e26f45):
  clarified the system functionality, project status, technology stack and
  usage instructions.

The significant implementation decisions were to keep retrieval lexical and
inspectable, refuse unsupported claims rather than invent answers, expose
relevance limits, and add recovery actions after the Lab 3 failure analysis.
These choices kept the prototype explainable and reproducible while making its
limitations visible to the student. Checks included Python compilation, the
three verdict paths, mode and evidence-limit validation, absolute-wording
detection, Scholar URL generation and an HTTP smoke test.

## AI assistance

AI assistance was provided by the **Copilot SDK in VS Code** throughout the
development process. It was used as a support tool to:

- understand and summarise the existing lab artefacts, requirements and
  constraints;
- explore and compare possible system structures, retrieval approaches,
  interaction choices and implementation trade-offs;
- help develop the local Python service, browser interface, evidence corpus
  handling and supporting documentation;
- suggest test cases, inspect test results, identify weaknesses and support
  iterative improvements to the system;
- draft, refine and explain the architecture and interaction graphs, including
  instructions for Mermaid diagrams and their layout and presentation; and
- improve the clarity of the README, report wording and user instructions.

The author remained responsible for the system and its academic content. The
author selected the scope and design decisions, supplied the requirements,
reviewed and tested all suggestions against the actual implementation,
corrected inaccuracies, rejected unsupported claims about live retrieval, and
made the final decisions about what was included. For example, suggestions
were constrained to lexical retrieval rather than presented as semantic
truth-detection, and generated graph layouts were checked against the actual
system flow before inclusion. AI assistance did not replace source evaluation
or author judgement, and no AI model is used at runtime by ClaimCheck.

## Additional files

- `app.py`, `retrieve.py`, `index.html`: runnable implementation.
- `corpus/`: evidence files; add Markdown with `source`, `section`, `updated`
  and optional `url` front matter.
- `Graphs/`: architecture diagram and normal/failure storyboards.

No additional ZIP file is required. Do not commit API keys, personal data or
generated secrets. If a future provider needs credentials, a reviewer should
supply their own through an environment variable or local secret store; no
credential belongs in this repository.
