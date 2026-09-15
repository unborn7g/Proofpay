# Portal submission fields (ready to paste)

Portal: https://portal.genlayer.foundation/agent-tank/hackathon/submit
Deadline: **17 Sept 2026 · 15:30 UTC** · track: Agentic Commerce Infrastructure

- **Project name:** ProofPay
- **One-liner (160/180 chars):**
  ProofPay turns natural-language work agreements into verifiable payment conditions, so agents are paid only when GenLayer confirms the work satisfies the brief.
- **Description (972/1000 chars):**
  ProofPay is a programmable escrow layer for the agentic economy. A person or AI agent hires another agent for digital work - a website, code, research, data analysis, a campaign - and locks payment against a plain-English brief with acceptance criteria. When the worker submits evidence (live URL, GitHub repo, report, dataset), GenLayer validators independently evaluate whether the delivered outcome actually satisfies the brief - not merely whether a file was uploaded. If it passes, funds release autonomously; if it fails, the contract requests revision and the money stays locked. Today escrow can prove work was submitted; ProofPay proves it satisfies the agreement. The contract fetches live web evidence and adjudicates each criterion with LLMs under GenLayer's equivalence principle, turning subjective judgment into on-chain consensus. The MVP ships the website template as the showcase flow; the same rubric engine extends to research, data and marketing work.
- **Logo:** `assets/logo.png`
- **Public GitHub repo:** https://github.com/unborn7g/Proofpay (already uploaded ✔)
- **Live demo/website URL (required):** https://unborn7g.github.io/Proofpay/ (redirects to the demo; evidence site: /bluebird/)
- **Private judges' note (≤500 chars):** (superseded — use the FINAL STRINGS section at the bottom of this file)

## How-to steps (structured, numbered — paste into portal)

1. Open the live demo URL and press "▶ Run success path": brief → 20 USDC escrow → worker submits live URL + GitHub repo → 5 validators check 6 criteria → VERIFIED, funds released.
2. Press "▶ Run failure path": same flow but the contact form is missing → validators FAIL that criterion → REVISION REQUESTED, escrow stays locked.
3. Optional on-chain: `npm i -g genlayer`, then `genlayer deploy --contract contract/proofpay.py --network bradbury`.
4. `genlayer write <ADDR> create_task --args "One-page dark-theme coffee shop site with menu, contact form, mobile-friendly, public repo" '[{"id":"live","label":"Live deployed website"},{"id":"resp","label":"Mobile responsive"},{"id":"menu","label":"Menu section"},{"id":"contact","label":"Contact form"},{"id":"dark","label":"Dark theme"},{"id":"repo","label":"GitHub source repo"}]' 20`
5. `genlayer write <ADDR> accept_task --args 1` then `genlayer write <ADDR> submit_evidence --args 1 '{"url":"<live-url>","repo":"<repo-url>"}'`
6. `genlayer write <ADDR> evaluate --args 1` → returns per-criterion verdicts; `genlayer call <ADDR> get_task --args 1` shows status VERIFIED or REVISION. Paste the address into the site's Live mode to watch it on-chain.

---

## FINAL STRINGS (Sep 15 — after Studio Next lifecycles landed)

### Field 06 — Studio Next contract link (paste exactly)
https://explorer-studio-dev.genlayer.com/address/0xE4d04f3784D20206f72EAF61999aDa825153825B

### Expected verification outcome (499 chars — paste exactly)
(1) https://unborn7g.github.io/Proofpay/ - live demo, success + failure paths, no wallet; (2) GitHub repo with the Intelligent Contract + evidence pages; (3) Studio Next explorer: contract 0xE4d04f3784D20206f72EAF61999aDa825153825B, 9 FINALIZED txs = deploy + two full lifecycles (create_task, accept_task, submit_evidence, evaluate) vs live URLs. Task 1: validators rendered the page, 6/6 passed, VERIFIED, 20 USDC released. Task 2: no contact form - 5/6, REVISION, funds locked, feedback on-chain.

### Demo video field
After uploading proofpay-demo.mp4 to YouTube, paste that YouTube URL here.

### YouTube title (paste exactly)
ProofPay — Escrow That Proves Satisfaction, Not Submission (GenLayer Agent Tank)

### YouTube description (paste exactly)
ProofPay is a programmable escrow layer for the agentic economy: a client locks 20 USDC against a plain-English brief, a worker agent delivers the work, and GenLayer validators open the live evidence and judge every criterion against the brief. All pass → payment releases itself. Any fail → revision requested, funds stay locked, structured feedback returned. Escrow proves submission. ProofPay proves satisfaction.

In this demo:
0:00 The brief + 20 USDC locked in escrow
0:12 Worker agent delivers evidence (live URL + GitHub repo)
0:25 Validators judge the outcome → 6/6 VERIFIED, paid on proof
0:38 Failure path: missing contact form → REVISION REQUESTED, funds stay locked

Try it live: https://unborn7g.github.io/Proofpay/
Contract on Studio Next (chain 61997): https://explorer-studio-dev.genlayer.com/address/0xE4d04f3784D20206f72EAF61999aDa825153825B
Source: https://github.com/unborn7g/Proofpay

Built for the GenLayer Agent Tank hackathon — track: Agentic Commerce Infrastructure.

#GenLayer #ProofPay #AgenticCommerce #Escrow #AIagents #SmartContracts

### YouTube tags
GenLayer, ProofPay, agentic commerce, AI agents, escrow, intelligent contracts, web3, hackathon
