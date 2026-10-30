# Terms from Reasoning

| Term | What it is | Say it as |
|---|---|---|
| Reasoning model | A model that produces hidden working before its visible answer, and bills you for it as output tokens. | A model that thinks before it speaks. |
| Reasoning tokens (thinking tokens) | The output tokens spent on that hidden working. Counted in the output total. | The tokens you pay for and never read. |
| Chain of thought (CoT) | Asking the model to write its steps before the answer. | Show your working. |
| Step-back prompting | First ask for the general rules or formulas, then solve with them in front of you. | Principles first, then the case. |
| Self-consistency | Ask the same step-by-step question several times and take the most common answer. | Take a vote. |
| Majority vote / agreement | The winning answer, and the share of valid votes it got. | How many of the five agree. |
| Temperature (above zero) | Randomness in sampling. Votes need it, so the samples can differ. | A little noise on purpose. |
| Reasoning effort | A setting (low, medium, high) on some models that trades cost and delay against care. | The thinking dial. |
| Ground truth | The one correct answer, worked out independently, that a result is checked against. | The answer key. |
| Token budget | The tokens you may spend: a daily limit, a per-minute limit, a monthly bill. | What you can afford to ask. |
| Rate limit (429) | The provider's "slow down" reply. A per-minute limit is waited out; a daily limit means stop. | Wait, or stop for today. |
| Cost per 1,000 questions | Tokens x price, scaled to a volume a business can compare. | The number finance asks for. |
| Scratchpad | Private working the model writes before the real reply, inside tags your code removes. | The back of the envelope. |
| `<final>` tag | The part of a reply that may be shown, checked and stored as the answer. | The only part that ships. |
| Prompt version 2 | A new library entry beside v1, with a reason in numbers; v1 is never edited. | Add v2, keep v1. |