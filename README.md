## Self-Auditing Context Engine

This project demonstrates an explainable context-selection mechanism for AI systems.

### Problem
AI systems silently select some documents as context while ignoring others.
This project logs and explains those decisions.

### Approach
- TF-IDF + cosine similarity is used to compute relevance scores.
- A fixed threshold (0.15) determines document inclusion.
- Every decision is logged with a human-readable explanation.

### Output
The system generates a CSV audit log containing:
- Relevance scores
- Selection decisions
- Reasons for inclusion or exclusion
