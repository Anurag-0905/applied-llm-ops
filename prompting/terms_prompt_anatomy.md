# Terms from Prompt Anatomy

| Term | What it is | Say it as |
|---|---|---|
| Prompt | The text (and examples) sent to a model to get a behaviour. | Your instruction, plus everything it needs. |
| System message | The message that sets standing rules for the whole conversation. | The model's job description. |
| User message | The message carrying this request's task, context and input. | The job on today's desk. |
| Role | The part of a prompt saying who the model is and who it writes for. | Who is speaking, to whom. |
| Task | The one-sentence instruction, starting with a verb. | What to do. |
| Context | Facts and rules the model cannot know, supplied in the prompt. | What it must be told. |
| Constraints | Limits on length, content, and what must never be revealed. | The fence around the answer. |
| Output format | The exact shape of the reply (bullets, a word, JSON keys). | The shape of the answer. |
| Zero-shot / one-shot / few-shot | A prompt with no, one, or several worked examples. | Show it how, in 0, 1 or a few examples. |
| House convention | A rule obvious inside your organisation but invisible to a model, taught best by examples. | Your bank's own rules of thumb.
| Acceptance check | A small piece of code that tests whether an output is good enough. | A test for an answer. |
| Prompt library | A file of every prompt version, its output and its check results, kept in version control. | The prompt's history. |
| Prompt versioning | Adding a new version instead of editing an old one. | Never overwrite; add v2. |
| Work repository | Your own Git repository, where you push your work. | Your folder on GitHub. |
| Commit / push | Recording a snapshot locally / sending your snapshots to GitHub. | Save a version, then hand it in. |
| Remote / origin | The GitHub copy of a repository that your local copy is linked to. | The online twin. |