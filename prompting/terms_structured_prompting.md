# Terms from Structured Prompting — what they are, and where they come back

| Term | What it is | Say it as |
|---|---|---|
| Delimiter | A marker (a tag, a fence, a quote mark) that shows where the customer's text starts and ends. | A fence around the data. |
| XML-style tags | Delimiters written as `<ticket> ... </ticket>`. Models read them clearly; they have no special power by themselves. | Named envelopes. |
| Instructions vs data | Instructions are what you want done; data is what you want done *to*. They must not be confused. | The letter and the envelope. |
| Tag escaping | Neutralising your own tag names inside customer text, so a customer cannot close your tag. | Don't let them type the envelope's flap. |
| Prompt template | A prompt with holes for variables, filled per request. | A mail-merge letter. |
| Jinja | A template language with variables, loops, conditions and filters. | The mail-merge engine. |
| Strict undefined | A setting that makes a missing variable an error instead of a blank. | Fail loudly. |
| System prompt | The standing instructions that define how the assistant behaves, sent before the user's message. | The behaviour contract. |
| Prompt file | A system prompt stored as a file with a version, loaded at runtime. | The SOP binder, not a sticky note. |
| Front matter | A small `---` block at the top of a file holding its name and version. | The label on the binder. |
| Few-shot example | A worked input and answer placed in the prompt to show the model what you mean. | Show, don't just tell. |
| Labelled set | Inputs with the correct answer attached, written by people. | The answer key. |
| Train / held-out split | Examples come from the training pool; accuracy is measured on tickets that never enter a prompt. | Practice papers and the real exam. |
| Leakage | A test item that also appears in the prompt, so the score is inflated. | Marking your own homework. |
| Held-out accuracy | The share of held-out tickets the classifier got right. | The honest number. |
| Confusion table | A grid of what a ticket really was against what the classifier said. | Where the mistakes go. |
