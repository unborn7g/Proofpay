# ProofPay — Agent Tank Submission Pack

> Build window: 3–17 September · deadline **17 Sept, 12 PM UTC** · winners 25 Sept.
> Pack assembled 15 Sept 2026. Demo app: `web/index.html` · reference contract: `contract/proofpay.py` · portal fields: `PORTAL_FIELDS.md`.

---

## Final product definition

> **ProofPay is a programmable escrow layer for the agentic economy. It translates
> natural-language work agreements into verifiable outcome criteria, enabling
> autonomous payment only when independently validated work satisfies the original brief.**

## One-line pitch

> **ProofPay turns natural-language work agreements into verifiable payment
> conditions, so agents are paid only when GenLayer confirms the delivered
> outcome satisfies the brief.**

## Problem line (use everywhere)

> **Today, escrow can prove that work was submitted. ProofPay proves that the
> work satisfies the agreement.**

## Short description (portal form)

ProofPay is an outcome-based escrow layer for AI-agent work. A person or agent
hires another agent for digital work — a website, code, research, data analysis,
a campaign — and locks payment against a plain-English brief with acceptance
criteria. When the worker submits evidence (live URL, GitHub repo, report,
dataset), GenLayer validators independently evaluate whether the outcome
actually satisfies the brief — not merely whether a file was uploaded. If it
passes, funds release autonomously; if it fails, the contract requests revision
or resolves the dispute and the money stays safe. ProofPay makes it safe for
agents to transact for real work.

## X post (final)

> AI agents can hire each other — but today, escrow only proves work was
> submitted. It can't prove the work satisfies the agreement.
>
> **ProofPay** turns natural-language work agreements into verifiable payment
> conditions. A buyer locks funds against a plain-English brief. A worker agent
> delivers code, research, a dataset, a design. GenLayer validators
> independently evaluate whether the outcome meets the brief — then release
> payment only when it does.
>
> Not "proof a file was uploaded."
> **Proof the work is good enough to pay for.**
>
> #AgentTank #GenLayer #AgenticEconomy

---

## Demo script (60–90 s, record the live app)

1. **Brief (10 s)** — "A client writes a plain-English brief: a coffee-shop
   landing page with six acceptance criteria. Budget: 20 USDC." Click *Run*.
2. **Escrow (10 s)** — "Funds lock in an intelligent contract. Not paid on
   submission — paid on satisfaction."
3. **Work (15 s)** — "A worker agent accepts, builds, deploys, and submits a
   live URL plus the GitHub repo as evidence."
4. **Validation (25 s)** — "GenLayer validators fetch the live site and judge
   each criterion against the brief — this is what only GenLayer can do:
   consensus over subjective, natural-language outcomes."
5. **Success (10 s)** — "6/6 → VERIFIED. 20 USDC releases autonomously."
6. **Failure path (15 s)** — run the failure path: "Same brief, but no contact
   form. Traditional escrow would still pay — the file was submitted. ProofPay
   says REVISION REQUESTED. Funds stay locked. **Submission ≠ satisfaction.**"

### Demo result tables (mirror in slides/video)

| Requirement | Success | Failure |
|---|---|---|
| Live deployed website | ✅ | ✅ |
| Mobile responsive | ✅ | ✅ |
| Menu section | ✅ | ✅ |
| Contact form | ✅ | ❌ Not found |
| Dark theme | ✅ | ✅ |
| GitHub source repository | ✅ | ✅ |
| **Outcome** | **VERIFIED — 20 USDC released** | **REVISION — 20 USDC locked** |

---

## Why GenLayer (judge bullets)

- Only GenLayer's Intelligent Contracts can natively **fetch web evidence**
  (`gl.nondet.web.render`) and **call LLMs with consensus**
  (`gl.eq_principle`) — exactly what outcome verification needs.
- Deterministic chains can verify transactions; they cannot read a website and
  judge whether it meets a brief. ProofPay is GenLayer-native by construction.
- Directly serves the agentic economy: agents hiring agents with no trust.

## Framing: infrastructure, not a website app

ProofPay = programmable escrow for digital agent work. Templates apply the right
verification rubric per work type (website, research, data analysis, marketing,
custom). The hackathon MVP ships the **website template** as the polished
showcase flow — the sharp entry point, like Stripe's online payments.

---

## Last-48-hours build checklist (real testnet wiring)

- [ ] Deploy `contract/proofpay.py` with GenLayer Studio to testnet; verify in explorer.
- [ ] Swap the simulated balances for test-USDC via the payable pattern in GenLayer docs.
- [ ] Connect `web/index.html` to the deployed contract with the GenLayer JS SDK
      (create task → accept → submit evidence → evaluate → read verdicts).
- [ ] Pre-build the worker deliverable (coffee-shop site + public GitHub repo)
      and a broken variant for the failure path.
- [ ] Record the 90 s demo video using the script above; submit X post + link
      before 17 Sept, 12 PM UTC.
