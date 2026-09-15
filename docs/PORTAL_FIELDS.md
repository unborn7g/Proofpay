# Portal submission fields (ready to paste)

Portal: https://portal.genlayer.foundation/agent-tank/hackathon/submit
Deadline: **17 Sept 2026 · 15:30 UTC** · track: Agentic Commerce Infrastructure

- **Project name:** ProofPay
- **One-liner (160/180 chars):**
  ProofPay turns natural-language work agreements into verifiable payment conditions, so agents are paid only when GenLayer confirms the work satisfies the brief.
- **Description (972/1000 chars):**
  ProofPay is a programmable escrow layer for the agentic economy. A person or AI agent hires another agent for digital work - a website, code, research, data analysis, a campaign - and locks payment against a plain-English brief with acceptance criteria. When the worker submits evidence (live URL, GitHub repo, report, dataset), GenLayer validators independently evaluate whether the delivered outcome actually satisfies the brief - not merely whether a file was uploaded. If it passes, funds release autonomously; if it fails, the contract requests revision and the money stays locked. Today escrow can prove work was submitted; ProofPay proves it satisfies the agreement. The contract fetches live web evidence and adjudicates each criterion with LLMs under GenLayer's equivalence principle, turning subjective judgment into on-chain consensus. The MVP ships the website template as the showcase flow; the same rubric engine extends to research, data and marketing work.
- **Logo:** `assets/logo.png`
- **Public GitHub repo:** https://github.com/unborn7g/proofpay (create repo named `proofpay`, upload this folder)
- **Live demo/website URL (required):** ____________________ (host `web/` on GitHub Pages / Netlify / Vercel)
- **Private judges' note (≤500 chars):**
  Live contract on GenLayer studionet: 0xf668bD0594e107FdF6972295aaC54372CD689F1e (deploy tx 0x963b0a3e…effa5c); create_task/accept_task/evaluate executed via CLI, consensus ACCEPTED. Expected: coffee-shop evidence meeting all criteria => VERIFIED + escrow released; variant missing contact form => REVISION, funds locked. Web evidence via gl.nondet.web.render (strict_eq); criteria adjudicated via gl.nondet.exec_prompt under equivalence principle (verdicts compared for consensus).

## How-to steps (structured, numbered — paste into portal)

1. Open the live demo URL and press "▶ Run success path": brief → 20 USDC escrow → worker submits live URL + GitHub repo → 5 validators check 6 criteria → VERIFIED, funds released.
2. Press "▶ Run failure path": same flow but the contact form is missing → validators FAIL that criterion → REVISION REQUESTED, escrow stays locked.
3. Optional on-chain: `npm i -g genlayer`, then `genlayer deploy --contract contract/proofpay.py --network bradbury`.
4. `genlayer write <ADDR> create_task --args "One-page dark-theme coffee shop site with menu, contact form, mobile-friendly, public repo" '[{"id":"live","label":"Live deployed website"},{"id":"resp","label":"Mobile responsive"},{"id":"menu","label":"Menu section"},{"id":"contact","label":"Contact form"},{"id":"dark","label":"Dark theme"},{"id":"repo","label":"GitHub source repo"}]' 20`
5. `genlayer write <ADDR> accept_task --args 1` then `genlayer write <ADDR> submit_evidence --args 1 '{"url":"<live-url>","repo":"<repo-url>"}'`
6. `genlayer write <ADDR> evaluate --args 1` → returns per-criterion verdicts; `genlayer call <ADDR> get_task --args 1` shows status VERIFIED or REVISION. Paste the address into the site's Live mode to watch it on-chain.
