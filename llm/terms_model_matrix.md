# Terms from Model Matrix

| Term | What it is | Say it as |
|---|---|---|
| API (hosted API) | A service you call over the internet; the provider runs the model. | Someone else's machine. |
| Vendor API / closed model | A model only its vendor runs; weights not downloadable. | You rent it. |
| Frontier model | The most capable models available at a given time, mostly closed. | The top of the range. |
| Model family and tier | A vendor's line-up: flagship, mid-tier, economy — same brand, different size, price, speed. | Same family, different size. 
| Open-weight | The trained numbers (weights) are published and downloadable. | You can take it home.
| Open-source vs open-weight | Open-source would also release code and training data; open-weight releases only the weights, under a licence that may restrict use. | Read the licence. |
| Hosted open-weight | A provider (e.g. Groq) runs published weights for you. | Open model, rented compute. |
| Self-hosted / on-premises | You run the model on your own hardware, where the data lives. | You run it, you secure it. |
| Parameters | The learned numbers inside a model; 3B, 20B, 120B = billions of them. | Model size. |
| Mixture-of-experts (MoE) | Many parameters in total, only a fraction active per token. Fast for the size. | Big library, few books opened per question. |
| Max output tokens | A separate, smaller limit on how long one answer can be. | The answer's ceiling. |
| Time to first token (TTFT) | Delay before the first visible token. Includes hidden thinking for reasoning models. | How long until it starts. |
| Tokens per second | Output speed once it starts. | How fast it talks. |
| Price per million tokens | How providers bill; input and output priced separately. | Two prices, not one. |
| Cached input / batch API | Discounts: repeated prompt prefixes cost less; asynchronous batch jobs cost about half. | Ways to pay less for the same tokens. |
| Reasoning tokens | Hidden thinking tokens, billed as output. | You pay to think. |
| Benchmark / leaderboard | A public test score for models. Useful to shortlist; contamination and narrow tasks make it unreliable to decide. | A hint, not a verdict. |
| Hard constraint | A requirement that removes options before any scoring (residency, latency limit, capacity). | Pass or out. |
| Weighted score | Combining cost, speed and quality with weights that reflect the business. | Who chooses the weights matters. |
| Data residency | Rules on where data may be processed or stored. | Where may it go? |
