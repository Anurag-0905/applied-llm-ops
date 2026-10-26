# Terms from Tokens

| Term | What it is | Say it as |
|---|---|---|
| Provider | Where the model runs: a cloud service (Groq) or your own machine (Ollama). Identified by `BASE_URL`. | A place. |
| Model | The trained weights that answer. Identified by `MODEL`. | A brain. |
| Token | The unit the model reads — a piece of text from a fixed dictionary; ~¾ of an English word. | Not a word, a dictionary entry. |
| Tokenizer | The dictionary that cuts text into tokens. Belongs to the model. | Different model, different cuts. |
| Encoding (`o200k_harmony`) | The name of one tokenizer dictionary; `tiktoken` ships it. | The dictionary's name. |
| `usage` | The field returned after every call: `prompt_tokens`, `completion_tokens`, `total_tokens`. | The truth after you send. |
| Context window | The maximum tokens a model can see at once; everything must fit. | A budget. |
| Embedding | A vector of numbers standing for a text's meaning. | Meaning as coordinates. |
| Vector | A list of numbers treated as a point or direction; "close" = pointing the same way. | A point on a map. |
| Embedding model | A model whose output is a vector, not text. Never answers. | Text in, numbers out. |
| PCA | Squashing many dimensions to two so humans can look. Pictures only. | For the picture, not the search. |
| Next-token prediction | How answers are produced: score every possible next token, pick one, repeat. | One token at a time. |
| Attention | How the model weighs which earlier tokens matter for the next one. | Looking back over the context. |
| Temperature | How much randomness in each pick; 0 = the most likely token every time. | The randomness dial. |
| Reasoning model | A model that spends hidden tokens thinking before the visible answer. | Thinks first; costs more. |
| Pre-training | Learning to predict the next token from a huge corpus → a base model. | Reading the internet. |
| Fine-tuning (instruction tuning) | Further training on instruction/answer pairs → a chat model. | Learning to follow instructions. |
| Preference tuning (RLHF) | Nudging toward human-preferred answers. | Learning manners. |
| Base model vs chat model | Pre-trained only vs fine-tuned to follow instructions. You call chat models. | Raw vs trained to talk. |
| Hugging Face | The public hub where open-weight models, datasets and tokenizers are published. Ollama and Groq run models from it. | Where open models come from. |
| Open-weight vs frontier | Downloadable weights (Llama, Qwen, gpt-oss) vs vendor-API-only (GPT, Claude, Gemini). | Can you run it yourself? |
