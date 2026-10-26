# Terms from Vision Structured

| Term | What it is | Say it as |
|---|---|---|
| Multimodal model | A model that accepts more than text — images, sometimes audio or video — alongside text. | Reads pictures too. |
| Vision model | A multimodal model used to understand images. | The one that reads pictures. |
| Base64 / data URL | A way of writing a file's bytes as plain text so it can travel inside a JSON message. | A picture written out as letters. |
| Image tokens | The tokens an image is billed as; often hundreds or more, depending on model and size. | A picture has a price. |
| OCR | Turning the text in an image into machine-readable text. Vision models do this implicitly. | Reading the words off a picture. |
| Structured output | Getting a model's reply in a fixed, machine-readable shape instead of free prose. | Data, not paragraphs. |
| JSON mode | Provider guarantee that the reply is valid JSON — of any shape. | Valid, but not necessarily what you wanted. |
| JSON Schema | A standard way of describing the exact shape JSON must have: keys, types, allowed values. | The blueprint for the reply. |
| Schema-enforced / strict mode | The provider constrains decoding so the reply must match your JSON Schema. | A contract on the shape. |
| Constrained decoding | The mechanism behind strict mode: invalid next tokens are simply not allowed. | The model can't type the wrong thing. |
| Pydantic validation | Python code that checks types *and business rules* on data after it arrives. | The contract on the meaning. |
| Retry with error feedback | On failure, send the exact error back to the model and ask again, a limited number of times. | Tell it what it got wrong, once. |
| Human-in-the-loop | Routing cases the system can't resolve to a person instead of guessing. | Know where automation stops. |
| Slot filling | Collecting the pieces of information a task needs, one conversation turn at a time. | Fill the blanks, ask for what's missing. |
