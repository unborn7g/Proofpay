# ProofPay

**ProofPay turns natural-language work agreements into verifiable payment
conditions, so agents are paid only when GenLayer confirms the work satisfies
the brief.**

> Today, escrow can prove that work was submitted. ProofPay proves that the
> work satisfies the agreement.

Built for **Agent Tank** (GenLayer hackathon) · track: Agentic Commerce
Infrastructure · September 2026.

## Repo layout

| Path | What it is |
|---|---|
| `web/index.html` | The live demo website (self-contained: HTML+CSS+JS). Simulation mode always works; **Live mode** reads real on-chain state when you paste a deployed contract address. |
| `contract/proofpay.py` | The GenLayer Intelligent Contract (escrow + validator evaluation + settlement). |
| `assets/logo.png` | Project logo (portal requirement). |
| `docs/PORTAL_FIELDS.md` | Ready-to-paste portal submission fields (within char limits). |
| `docs/HOW_IT_WORKS.md` | Plain-English explainer of the product and the code. |
| `docs/SUBMISSION.md` | Pitch pack: X post, demo script, judge bullets, checklist. |

## Try the demo (30 seconds)

```bash
cd web && python3 -m http.server 8000 --bind 0.0.0.0
# open http://localhost:8000
```

Press **▶ Run success path** (all criteria pass → 20 USDC released) and
**▶ Run failure path** (contact form missing → REVISION REQUESTED, funds stay
locked). The failure path is the product: normal escrow would have paid anyway.

## How it works (one paragraph)

A client locks USDC in the contract against a plain-English brief with
acceptance criteria. A worker agent submits evidence (live URL + GitHub repo).
`evaluate()` makes GenLayer validators **fetch the live site**
(`gl.nondet.web.render` under `strict_eq`) and **adjudicate each criterion**
(`gl.nondet.exec_prompt` under the equivalence principle, comparing only
per-criterion verdicts + the final decision). All pass → escrow releases
autonomously. Any fail → revision requested, funds stay locked, structured
feedback returned.

## Deploy to GenLayer testnet (numbered)

1. Install Node.js, then the CLI: `npm install -g genlayer`
2. Test locally first: `genlayer init && genlayer up` (localnet with 5 validators)
3. Fund your wallet with testnet GEN (built-in faucet).
4. Deploy: `genlayer deploy --contract contract/proofpay.py --network bradbury`
   (or `--rpc <url>` for Asimov/other networks — follow the current CLI docs).
   Note the printed **contract address**.
5. Sanity check: `genlayer schema <CONTRACT_ADDRESS>` and
   `genlayer call <CONTRACT_ADDRESS> get_task --args 1`
6. Drive a task from the terminal:
   `genlayer write <ADDR> create_task --args "<brief>" '<criteria-json>' 20`
   then `accept_task`, `submit_evidence`, `evaluate` (see docs/PORTAL_FIELDS.md
   for the full judge walkthrough).
7. Open `web/index.html`, expand **Live mode**, paste the contract address —
   the panel polls `get_task` read-only and shows the real on-chain status and
   per-criterion verdicts.

## Security / design notes

- The LLM never decides deterministic facts; URLs/statuses are collected as
  canonical evidence and passed to the prompt inside delimited UNTRUSTED DATA
  regions to limit prompt injection.
- Consensus compares only decision + per-criterion pass/fail, so validator
  reasoning may differ without breaking agreement.

## On-chain status (live)

- **Network:** GenLayer Studio Next / studio-dev, chain **61997** (GenVM v0.6 runner)
- **Contract:** `0xE4d04f3784D20206f72EAF61999aDa825153825B`
- **Explorer:** https://explorer-studio-dev.genlayer.com/address/0xE4d04f3784D20206f72EAF61999aDa825153825B
- **Deploy tx:** `0x7d53ef0f9752e493a4263d8d1d43c4d3e0c295bc1892e623e8c9a8dbb43823bd` (FINALIZED · SUCCESS)
- **Success path — Task #1 VERIFIED 6/6:** `create_task` → `accept_task` →
  `submit_evidence` (live URL + repo) → `evaluate`. Validators fetched the live page,
  passed all 6 criteria with written notes, and escrow released 20 USDC to the worker
  (`balance_of(worker) = 20`). Evaluate tx `0x74a9637e9f5c1a46d55967b49e6846b8dfe86c52c45e248edf53b0ed8efdb130`.
- **Failure path — Task #2 REVISION 5/6:** same brief, evidence page without a contact
  form. Validators failed the missing criterion ("no form element present anywhere"),
  funds stayed locked, structured feedback stored on-chain.
  Evaluate tx `0xb8c6cf67303415f75c2ee8a46f1d717ad4f80e2b1fb67059012016330b7139bb`.
- **All 9 transactions:** FINALIZED · GenVM SUCCESS · consensus Accepted.
- **Live demo:** https://unborn7g.github.io/Proofpay/
