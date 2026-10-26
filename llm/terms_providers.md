# Terms from Providers

| Term | What it is | Say it as |
|---|---|---|
| Messages list | The conversation sent to a model: a list of role/content pairs. | The whole conversation, not just the question. |
| system / user / assistant roles | Who is speaking in each message. system sets the model's behaviour; user is the human; assistant is the model's own prior replies. | Who said what. |
| temperature | How much randomness goes into picking the next token. 0 is close to deterministic. | The randomness dial. |
| top_p | An alternative way to shape the same randomness, by probability mass. | A different dial, same job. |
| max_tokens | A hard ceiling on how long the reply can be. | The answer's ceiling. |
| stop sequence | A string that ends generation the instant it appears. | A tripwire for the output. |
| Provider-agnostic code | Code that works unchanged against any provider because only config (BASE_URL, API_KEY, MODEL) changes. | Swap the plug, not the appliance. |
| OpenAI-compatible endpoint | An API that speaks the same request/response shape as OpenAI's, even from a different vendor. | Same language, different speaker. |