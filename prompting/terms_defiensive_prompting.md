# Terms from Defensive Prompting — what they are, and where they come back

| Term | What it is | Say it as |
|---|---|---|
| Prompt injection | Text inside the data a model reads, written to be followed as an instruction instead. | A fake memo slipped into your inbox. |
| Direct injection | The attacker writes the malicious message themselves, in a field you know is attacker-controlled. | A stranger hands you a fake memo. |
| Indirect injection | The attack is hidden inside a document or page a trusted user asked the model to read. | A bomb hidden inside a book your boss asked you to read aloud. |
| Instruction hierarchy | A stated rule that only the system prompt counts as an instruction - nothing in the data overrides it, however it is phrased. | Only the signed contract changes the terms. |
| Scratchpad / final split | The model's reasoning goes in one tag; only the other tag is read, shown or checked - the code does the discarding. | A sealed envelope: only the signed letter ships. |
| Attack success | The visible answer is wrong or leaks something - never counted just because the model "noticed" an attempt. | Grade the exam, not the margin notes. |
| Leak marker | A known phrase from your own system prompt that should never appear in a normal reply. | A watermark on a photocopy. |
| Defense-in-depth | Several independent layers (hardened prompt, sealed scratchpad, output-side check) so one failing layer doesn't fail the whole system. | A vault with a lock, a guard, and a camera. |
