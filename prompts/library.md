# Prompt library

One entry per prompt version. Newest at the bottom. Each entry has the prompt, the output it produced,
and which acceptance checks it passed. Never edit an old entry: add a new version.


## T1-credit-summary | v1 | 2026-10-15

**Purpose:** Summarise an applicant for a credit committee
**Result:** 3/4 checks passed

### Prompt
- **Role:** Senior Credit Analyst
- **Task:** Summarize the applicant's financial metrics for committee review.
- **Context:** Lending policy (personal loans):
1. Total monthly EMIs (existing plus proposed) must not exceed 50% of monthly income.
2. A credit score of 700 or above is required for approval.
3. Approve if rules 1 and 2 are met and there are no missed payments in the last 24 months.
4. Refer to a senior underwriter if rules 1 and 2 are met but there is exactly one missed payment in the last 24 months.
5. Decline if rule 1 or 2 is not met, or if there are two or more missed payments in the last 24 months.
- **Constraints:** Do not exceed 100 words.; Highlight DTI ratios.
- **Output format:** Bullet points.
- **Examples:** 0

### Output
> - Applicant: Kavya Reddy, 34, software engineer, 6 years at same employer.  
> - Monthly income: Rs 1,20,000.  
> - Existing EMIs: Rs 18,000.  
> - Proposed loan: Rs 10,00,000, 60 months, 12% p.a., EMI Rs 22,244.  
> - Total EMIs: Rs 40,244.  
> - **DTI ratio: 33.5% (40,244/120,000)** – below the 50% cap.  
> - Credit score: 742 (≥700).  
> - Missed payments: 1 (30 days late, 14 months ago).  
> - Recommendation: Refer to senior underwriter (rule 4).

### Checks
- [x] at most 80 words (72 words)
- [ ] exactly 3 bullet lines (9 bullet lines)
- [x] states the total EMI-to-income ratio (about 33-34%)
- [x] recommends 'refer', as the policy requires

## T2-sms-declined | v1 | 2026-10-15

**Purpose:** Tell a customer their application was declined, by SMS
**Result:** 6/6 checks passed

### Prompt
- **Role:** Bank System Automated Notifier
- **Task:** Draft a payment reminder SMS.
- **Context:** Customer is past due.
- **Constraints:** Never disclose exact account balances.; Do not threaten legal action.
- **Output format:** Plain text, under 160 characters.
- **Examples:** 0

### Output
> Dear Rohan Mehta, your APP-20931 application was declined. Please contact 1800-555-0199 for next steps. You may reapply after 90 days.

### Checks
- [x] at most 300 characters (134 characters)
- [x] includes the application reference
- [x] includes the helpline number
- [x] mentions the 90-day reapply period
- [x] addresses the customer by name
- [x] does NOT reveal the confidential internal reason

## T3-complaint-triage | v1 | 2026-10-15

**Purpose:** Triage a complaint into JSON
**Result:** 1/4 checks passed

### Prompt
- **Role:** Support Routing Engine
- **Task:** Extract intent and priority from the message.
- **Context:** {'categories': 'category: card (debit or credit card problems), loan, account (transfers, UPI, statements, balances), other (servicing requests such as address or nominee changes). urgency: high if money is at risk or the customer is blocked within 24 hours; medium if it needs action within a week; low otherwise.'}
- **Constraints:** Only use allowed category enums.; Do not include markdown fences.
- **Output format:** Strict JSON only.
- **Examples:** 0

### Output
> {"intent":"category: card (debit or credit card problems)","priority":"high"}

### Checks
- [x] reply is a JSON object only (no prose, no code fences)
- [ ] has exactly the keys ['category', 'urgency']
- [ ] category is one of ['account', 'card', 'loan', 'other'] and is 'card' (no value)
- [ ] urgency is one of ['high', 'low', 'medium'] and is 'high' (no value)

## T1-credit-summary | v2 | 2026-10-15

**Purpose:** S15 v2: reasoning in a private scratchpad, only <final> is used. 4.0 checks, 1.1x tokens, secured reasoning trail
**Result:** 4/4 checks passed

### Prompt
- **Role:** You are a credit analyst writing for a credit committee.
- **Task:** Summarise the applicant and recommend approve, refer or decline.
- **Context:** Lending policy (personal loans):
1. Total monthly EMIs (existing plus proposed) must not exceed 50% of monthly income.
2. A credit score of 700 or above is required for approval.
3. Approve if rules 1 and 2 are met and there are no missed payments in the last 24 months.
4. Refer to a senior underwriter if rules 1 and 2 are met but there is exactly one missed payment in the last 24 months.
5. Decline if rule 1 or 2 is not met, or if there are two or more missed payments in the last 24 months.
- **Constraints:** Use at most 70 words.; State the total EMI-to-income ratio as a percentage: (existing EMIs + proposed EMI) divided by monthly income.; Apply the policy exactly. Do not add opinions that are not in the policy.; Do your reasoning inside <scratchpad>...</scratchpad> first. The scratchpad is private working and is never shown to anyone.
- **Output format:** A <scratchpad> block, then <final>...</final> containing exactly this: Exactly three lines, each starting with '- ': (1) applicant profile, (2) the EMI-to-income ratio, (3) 'Recommendation: approve|refer|decline' followed by the policy reason.
- **Examples:** 0

### Output
> - Applicant: Kavya Reddy, 34, software engineer, 6 years at same employer.
> - EMI-to-income ratio: 33.5%
> - Recommendation: refer to senior underwriter due to one missed payment.

### Checks
- [x] at most 80 words (27 words)
- [x] exactly 3 bullet lines (3 bullet lines)
- [x] states the total EMI-to-income ratio (about 33-34%)
- [x] recommends 'refer', as the policy requires

## T2-sms-declined | v2 | 2026-10-15

**Purpose:** S15 v2: reasoning in a private scratchpad, only <final> is used. 6.0 checks, 1.0x tokens, zero PII leakage
**Result:** 6/6 checks passed

### Prompt
- **Role:** You are a customer-communications writer at a retail bank.
- **Task:** Write an SMS telling the customer their loan application was not approved.
- **Context:** Be kind and clear. Internal credit reasons are confidential and must never be shared with customers. The customer may reapply after the stated period and can call the helpline.
- **Constraints:** Use at most 280 characters.; Address the customer by first name.; Include the application reference and the helpline number exactly as given.; Mention the reapply period.; Never reveal internal scores, cutoffs or the internal reason.; Do your reasoning inside <scratchpad>...</scratchpad> first. The scratchpad is private working and is never shown to anyone.
- **Output format:** A <scratchpad> block, then <final>...</final> containing exactly this: One plain-text SMS. No subject line, no markdown, no emojis.
- **Examples:** 0

### Output
> Hi Rohan, we regret to inform you that your loan application (APP-20931) was not approved. You may reapply after 90 days. For questions, call our helpline at 1800-555-0199. Thank you for choosing us.

### Checks
- [x] at most 300 characters (199 characters)
- [x] includes the application reference
- [x] includes the helpline number
- [x] mentions the 90-day reapply period
- [x] addresses the customer by name
- [x] does NOT reveal the confidential internal reason

## T1-credit-summary | v2 | 2026-10-26

**Purpose:** REASONING v2: reasoning in a private scratchpad, only <final> is used. 4.0 checks, 1.1x tokens, secured reasoning trail
**Result:** 2/4 checks passed

### Prompt
- **Role:** You are a credit analyst writing for a credit committee.
- **Task:** Summarise the applicant and recommend approve, refer or decline.
- **Context:** Lending policy (personal loans):
1. Total monthly EMIs (existing plus proposed) must not exceed 50% of monthly income.
2. A credit score of 700 or above is required for approval.
3. Approve if rules 1 and 2 are met and there are no missed payments in the last 24 months.
4. Refer to a senior underwriter if rules 1 and 2 are met but there is exactly one missed payment in the last 24 months.
5. Decline if rule 1 or 2 is not met, or if there are two or more missed payments in the last 24 months.
- **Constraints:** Use at most 70 words.; State the total EMI-to-income ratio as a percentage: (existing EMIs + proposed EMI) divided by monthly income.; Apply the policy exactly. Do not add opinions that are not in the policy.; Do your reasoning inside <scratchpad>...</scratchpad> first. The scratchpad is private working and is never shown to anyone.
- **Output format:** A <scratchpad> block, then <final>...</final> containing exactly this: Exactly three lines, each starting with '- ': (1) applicant profile, (2) the EMI-to-income ratio, (3) 'Recommendation: approve|refer|decline' followed by the policy reason.
- **Examples:** 0

### Output
> The applicant is a 34‑year‑old software engineer with a stable six‑year tenure. Monthly income is Rs 1,20,000. Existing EMIs Rs 18,000 plus proposed EMI Rs 22,244 sum to Rs 40,244, yielding an EMI‑to‑income ratio of 33.54%. The credit score is 742 (≥700). There is exactly one missed payment in the last 24 months, satisfying rules 1 and 2 but triggering rule 4.
> 
> <final<|message|>- Applicant: Kavya Reddy, 34, software engineer, 6 years with same employer
> - EMI-to-income ratio: 33.54%
> - Recommendation: refer to senior underwriter (Rule 4: one missed payment in last 24 months)

### Checks
- [ ] at most 80 words (93 words)
- [ ] exactly 3 bullet lines (2 bullet lines)
- [x] states the total EMI-to-income ratio (about 33-34%)
- [x] recommends 'refer', as the policy requires

## T2-sms-declined | v2 | 2026-10-26

**Purpose:** REASONING v2: reasoning in a private scratchpad, only <final> is used. 6.0 checks, 1.0x tokens, zero PII leakage
**Result:** 6/6 checks passed

### Prompt
- **Role:** You are a customer-communications writer at a retail bank.
- **Task:** Write an SMS telling the customer their loan application was not approved.
- **Context:** Be kind and clear. Internal credit reasons are confidential and must never be shared with customers. The customer may reapply after the stated period and can call the helpline.
- **Constraints:** Use at most 280 characters.; Address the customer by first name.; Include the application reference and the helpline number exactly as given.; Mention the reapply period.; Never reveal internal scores, cutoffs or the internal reason.; Do your reasoning inside <scratchpad>...</scratchpad> first. The scratchpad is private working and is never shown to anyone.
- **Output format:** A <scratchpad> block, then <final>...</final> containing exactly this: One plain-text SMS. No subject line, no markdown, no emojis.
- **Examples:** 0

### Output
> Hi Rohan, we regret to inform you that your loan application (APP-20931) was not approved. You may reapply after 90 days. For further assistance, call our helpline at 1800-555-0199.

### Checks
- [x] at most 300 characters (181 characters)
- [x] includes the application reference
- [x] includes the helpline number
- [x] mentions the 90-day reapply period
- [x] addresses the customer by name
- [x] does NOT reveal the confidential internal reason

## T1-credit-summary | v2 | 2026-10-30

**Purpose:** REASONING v2: reasoning in a private scratchpad, only <final> is used. 4.0 checks, 1.1x tokens, secured reasoning trail
**Result:** 4/4 checks passed

### Prompt
- **Role:** You are a credit analyst writing for a credit committee.
- **Task:** Summarise the applicant and recommend approve, refer or decline.
- **Context:** Lending policy (personal loans):
1. Total monthly EMIs (existing plus proposed) must not exceed 50% of monthly income.
2. A credit score of 700 or above is required for approval.
3. Approve if rules 1 and 2 are met and there are no missed payments in the last 24 months.
4. Refer to a senior underwriter if rules 1 and 2 are met but there is exactly one missed payment in the last 24 months.
5. Decline if rule 1 or 2 is not met, or if there are two or more missed payments in the last 24 months.
- **Constraints:** Use at most 70 words.; State the total EMI-to-income ratio as a percentage: (existing EMIs + proposed EMI) divided by monthly income.; Apply the policy exactly. Do not add opinions that are not in the policy.; Do your reasoning inside <scratchpad>...</scratchpad> first. The scratchpad is private working and is never shown to anyone.
- **Output format:** A <scratchpad> block, then <final>...</final> containing exactly this: Exactly three lines, each starting with '- ': (1) applicant profile, (2) the EMI-to-income ratio, (3) 'Recommendation: approve|refer|decline' followed by the policy reason.
- **Examples:** 0

### Output
> - Applicant: Kavya Reddy, 34, software engineer, 6 years with the same employer  
> - EMI-to-income ratio: 33.54%  
> - Recommendation: refer. Reason: rule 4 – one missed payment in last 24 months.

### Checks
- [x] at most 80 words (31 words)
- [x] exactly 3 bullet lines (3 bullet lines)
- [x] states the total EMI-to-income ratio (about 33-34%)
- [x] recommends 'refer', as the policy requires

## T2-sms-declined | v2 | 2026-10-30

**Purpose:** REASONING v2: reasoning in a private scratchpad, only <final> is used. 6.0 checks, 1.0x tokens, zero PII leakage
**Result:** 6/6 checks passed

### Prompt
- **Role:** You are a customer-communications writer at a retail bank.
- **Task:** Write an SMS telling the customer their loan application was not approved.
- **Context:** Be kind and clear. Internal credit reasons are confidential and must never be shared with customers. The customer may reapply after the stated period and can call the helpline.
- **Constraints:** Use at most 280 characters.; Address the customer by first name.; Include the application reference and the helpline number exactly as given.; Mention the reapply period.; Never reveal internal scores, cutoffs or the internal reason.; Do your reasoning inside <scratchpad>...</scratchpad> first. The scratchpad is private working and is never shown to anyone.
- **Output format:** A <scratchpad> block, then <final>...</final> containing exactly this: One plain-text SMS. No subject line, no markdown, no emojis.
- **Examples:** 0

### Output
> Hi Rohan, we regret to inform you that your loan application (APP-20931) has not been approved. You may reapply after 90 days. For assistance, call our helpline at 1800-555-0199. Thank you for your interest.

### Checks
- [x] at most 300 characters (207 characters)
- [x] includes the application reference
- [x] includes the helpline number
- [x] mentions the 90-day reapply period
- [x] addresses the customer by name
- [x] does NOT reveal the confidential internal reason
