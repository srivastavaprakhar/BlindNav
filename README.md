# BlindNav 🦯

An accessibility-focused web application that uses **generative AI and NLP** to help visually impaired users navigate websites more easily and independently.

## What it does

BlindNav sits on top of any website and provides:
- **Spoken guidance** — converts page structure and content into voice-navigable audio cues
- **Content summarization** — distills dense web pages into concise, readable summaries
- **Natural language queries** — users can ask questions about page content and get spoken answers

## Tech Stack

- Python / FastAPI
- Generative AI (LLM-powered summarization and Q&A)
- NLP for content parsing and accessibility mapping
- Web speech APIs for text-to-speech output

## Motivation

Most accessibility tools are either screen readers that read everything verbatim (overwhelming) or require manual configuration. BlindNav uses AI to be selective and intelligent about what to surface — making the web genuinely more inclusive.

## Setup

```bash
git clone https://github.com/srivastavaprakhar/BlindNav.git
cd BlindNav
pip install -r requirements.txt
uvicorn main:app --reload
```

## License

MIT
