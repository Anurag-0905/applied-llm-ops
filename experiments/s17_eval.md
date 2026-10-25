# Session 17: prompt evaluation - v1 baseline vs v2 structured

Answering model: `openai/gpt-oss-20b` · Judge model: `openai/gpt-oss-20b` · Date: 2026-10-25

| Criterion | v1 (S14 baseline) | v2 (S16 structured) |
|---|---|---|
| Correct label | 16/25 = 64% | 25/25 = 100% |
| Cites the right house rule | 15/25 = 60% | 21/25 = 84% |
| Follows the reply format | 25/25 = 100% | 25/25 = 100% |
| Invents no policy | 25/25 = 100% | 25/25 = 100% |
| **All four criteria** | **15/25 = 60%** | **21/25 = 84%** |

Tickets graded: v1 25/25 · v2 25/25 (a ticket the judge could not parse is not counted, and is listed below).

Human spot-check: judge and human agreed on 20/20 = 100% of graded criteria (20/20).
