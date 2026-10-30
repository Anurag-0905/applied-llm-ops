# Chat state & memory windows

| Term | What it is | Say it as |
|---|---|---|
| **Conversation history (messages list)** | The growing, role-tagged list of every message so far, resent in full on every single call. As far as the model is concerned, this list IS the conversation - nothing else exists. | "A running transcript, handed over again in full every time." |
| **Turn** | One user message plus the assistant's reply to it. `RECALL_PROBE` scripts 17 of these. | "One exchange - you speak, they answer." |
| **Stateless call** | The model has zero memory of any previous API call, ever. "The assistant remembers" is not a model capability; it is your application code resending history. | "No memory of its own - the code remembers, not the model." |
| **Sliding window** | Keep only the most recent N messages, drop everything older - silently, with no warning. Flat cost forever; anything outside the window is simply gone. | "A rolling cutoff, like the last hour on a security camera." |
| **Summarization (compression)** | Periodically compress older turns into one short note, carried forward instead of the raw text. Recovers most recall, costs one extra model call per compression, and adds a new risk: the summary itself can be wrong. | "A running minutes-of-the-meeting note, rewritten every so often." |
| **Recall** | Whether a LATER turn can correctly use a fact stated in an EARLIER turn - checked on the model's visible reply only, nothing else. A precise, scripted, pass/fail check, decided before looking at results. | "Does it still know - yes or no, nothing in between." |
| **Context window** | The hard ceiling on how many tokens one call can hold, prompt and reply together. Past it, a call does not degrade - it fails outright. | "The size of the room everyone has to fit in." |

## One sentence per term
- Every call is stateless; "memory" is your code resending the list.
- A sliding window is cheap but silently forgets what falls outside it.
- Summarization remembers more but costs an extra call and can misremember.
- Recall is measured, not assumed - one exact fact, one exact check.
- The context window is a hard ceiling, not a soft slowdown.
