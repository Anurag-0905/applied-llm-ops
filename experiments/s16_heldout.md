# Session 16: held-out results for the support classifier

Model: `openai/gpt-oss-20b` · Date: 2026-10-16 · system.md `40170083` · user.j2 `2782cade` · examples per label: 2

Held-out accuracy (structured): 25/25 = 100%
Baseline accuracy (one-line instruction): 16/25 = 64%

| # | Ticket | Expected | Structured | Baseline |
|---|---|---|---|---|
| H01 | My credit card statement shows a purchase in another country while I h | card | card ok | card ok |
| H02 | The chip on my debit card stopped working at the petrol pump. | card | card ok | card ok |
| H03 | Please block my card, my wallet was stolen yesterday. | card | card ok | card ok |
| H04 | I was charged an extra 2% on my card for a fuel purchase. | card | card ok | card ok |
| H05 | The reward points on my credit card were not added for last month's sp | card | card ok | card ok |
| H06 | The EMI of my personal loan was deducted twice in March. | loan | loan ok | loan ok |
| H07 | I need a no-dues certificate now that my vehicle loan is closed. | loan | loan ok | loan ok |
| H08 | My home loan statement shows an interest figure that does not match th | loan | loan ok | loan ok |
| H09 | The bank has not released the second instalment of my construction loa | loan | loan ok | loan ok |
| H10 | Please tell me how much I must pay to close my personal loan today. | loan | loan ok | loan ok |
| H11 | My account statement for September shows a balance that does not match | account | account ok | account ok |
| H12 | My net banking transfer to another bank shows success but the receiver | account | account ok | account ok |
| H13 | The cheque I deposited five days ago has still not been cleared. | account | account ok | account ok |
| H14 | My account balance dropped by Rs 590 and I cannot find any transaction | account | account ok | account ok |
| H15 | IMPS payment failed, but the amount was deducted from my savings accou | account | account ok | account ok |
| H16 | I tried to pay via UPI but the QR code did not scan. | upi | upi ok | other WRONG |
| H17 | My PhonePe scan failed but the money was still deducted. | upi | upi ok | other WRONG |
| H18 | It keeps saying my UPI PIN is invalid. | upi | upi ok | other WRONG |
| H19 | I accidentally approved a fraudulent UPI collect request. | upi | upi ok | other WRONG |
| H20 | My UPI transfer has been stuck on 'Pending' for two days. | upi | upi ok | other WRONG |
| H21 | Please correct the spelling of my name on my account. | other | other ok | account WRONG |
| H22 | How do I give feedback about the long queue at your Kukatpally branch? | other | other ok | other ok |
| H23 | I need to update the nominee on my home loan. | other | other ok | loan WRONG |
| H24 | Please change the mobile number linked to my credit card. | other | other ok | card WRONG |
| H25 | What documents do I need to open a fixed deposit? | other | other ok | account WRONG |

Mistakes of the structured version, and what I changed because of them:

- none
