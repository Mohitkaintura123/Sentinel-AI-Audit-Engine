# generate_csv.py

import csv
from context_scoring import compute_relevance_scores

THRESHOLD = 0.65
PROJECT_LINK = "https://github.com/YourTeam/self-auditing-context-engine"

query = "What is the company data privacy policy?"

documents = [
    ("Doc_A", "Latest company data privacy policy from 2024"),
    ("Doc_B", "Archived privacy policy document from 2016"),
    ("Doc_C", "Marketing brochure describing company services"),
    ("Doc_D", "Legal compliance and GDPR guidelines"),
    ("Doc_E", "Internal employee handbook")
]

doc_ids = [d[0] for d in documents]
doc_texts = [d[1] for d in documents]

scores = compute_relevance_scores(query, doc_texts)

rows = []

for i in range(len(documents)):
    score = round(scores[i], 2)

    if score >= THRESHOLD:
        decision = "Included"
        reason = "High semantic relevance to the user query"
    else:
        decision = "Excluded"
        reason = "Relevance score below defined threshold"

    rows.append([
        query,
        doc_ids[i],
        doc_texts[i],
        score,
        THRESHOLD,
        decision,
        reason,
        PROJECT_LINK
    ])

output_path = "output/PS1_Context_Audit.csv"

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "query",
        "document_id",
        "document_summary",
        "relevance_score",
        "threshold",
        "decision",
        "reason",
        "project_link"
    ])
    writer.writerows(rows)

print(f"CSV generated at: {output_path}")
