# Function calling - golden set, four ways

Model: `llama3.2:3b` · Date: 2026-10-29 · Golden set: 10 questions (6 need a tool, 4 need none)

| Way | Right tool (or none) | Args valid | Answer correct | Tokens |
|---|---|---|---|---|
| none | 5/10 | 1/6 | 6/10 | 17122 |
| prompt | 5/10 | 1/6 | 5/10 | 18997 |
| validate | 5/10 | 1/6 | 6/10 | 17372 |
| router | 7/10 | 1/6 | 6/10 | 16138 |

Per question (tool / args / answer, '-' = no tool needed):

| Question | none | prompt | validate | router |
|---|---|---|---|---|
| g1 | y/n/n | y/n/n | y/n/n | y/n/n |
| g2 | y/n/n | y/n/n | y/n/n | y/n/n |
| g3 | y/y/y | y/y/y | y/y/y | y/y/y |
| g4 | n/n/n | n/n/n | n/n/n | n/n/n |
| g5 | y/n/y | y/n/y | y/n/y | y/n/y |
| g6 | y/n/n | y/n/n | y/n/n | y/n/n |
| g7 | n/-/y | n/-/y | n/-/y | y/-/y |
| g8 | n/-/y | n/-/y | n/-/y | n/-/y |
| g9 | n/-/y | n/-/n | n/-/y | n/-/y |
| g10 | n/-/y | n/-/y | n/-/y | y/-/y |

Scores were decided before running: right tool means exactly the expected tools (none for a no-tool question); args valid counts tool questions only; answer correct checks the final text for the expected number or fact. A 10-question golden set is a smoke test - quote it with the model name.
