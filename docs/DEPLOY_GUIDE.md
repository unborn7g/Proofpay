# ProofPay deploy guide — copy-paste edition (Windows first)

Goal: contract on GenLayer testnet → one real task through it → show it on the
site → submit the portal. ~30–45 min. Uses the **official CLI account flow** —
you never export or paste a private key. The CLI keeps it in your OS keychain.

## Step 1 — Install Node.js

```powershell
winget install OpenJS.NodeJS.LTS
```
(or nodejs.org → LTS). Close & reopen PowerShell, then: `node -v`

## Step 2 — Install the GenLayer CLI

```powershell
npm install -g genlayer
```

## Step 3 — Create a deployer account (no key handling needed)

```powershell
genlayer account create --name proofpay
genlayer account use proofpay
genlayer account show
```

`account show` prints **your address** — copy it. (This is a fresh deployer
account; your portal wallet stays untouched.)

## Step 4 — Pick the testnet + get faucet GEN

```powershell
genlayer network set testnet-bradbury
```

Faucet: **https://testnet-faucet.genlayer.foundation/** → paste your address →
claim. Wait ~a minute, then `genlayer account show` again to see the balance.

## Step 5 — Deploy the contract

```powershell
cd C:\path\to\proofpay
genlayer deploy --contract contract/proofpay.py
```

**Copy the printed contract address** (`<ADDR>` below).
Testnet sometimes throws `LEADER_TIMEOUT` / generic revert under load →
just retry the same command.

See it on the explorer (bookmark both):
- https://explorer-bradbury.genlayer.com/address/<ADDR>
- https://studio.genlayer.com/?import-contract=<ADDR>

## Step 6 — Run one real task (copy-paste block)

```powershell
genlayer schema <ADDR>

genlayer write <ADDR> create_task --args "One-page dark-theme site for a coffee shop: menu with prices, contact form, mobile responsive, public GitHub repo, deployed live" "[{\"id\":\"live\",\"label\":\"Live deployed website\"},{\"id\":\"resp\",\"label\":\"Mobile responsive\"},{\"id\":\"menu\",\"label\":\"Menu section\"},{\"id\":\"contact\",\"label\":\"Contact form\"},{\"id\":\"dark\",\"label\":\"Dark theme\"},{\"id\":\"repo\",\"label\":\"GitHub source repo\"}]" 20

genlayer write <ADDR> accept_task --args 1

genlayer write <ADDR> submit_evidence --args 1 "{\"url\":\"https://YOUR-LIVE-SITE\",\"repo\":\"https://github.com/unborn7g/proofpay\"}"

genlayer write <ADDR> evaluate --args 1

genlayer call <ADDR> get_task --args 1
```

The last line prints the on-chain task JSON (status + per-criterion verdicts).
**Copy that whole output.** If PowerShell quoting misbehaves, run these from
Git Bash or cmd instead.

## Step 7 — Put your links on the site

Open `web/index.html` in a code editor. At the top of the `<script>` there is
one `CONFIG` block — paste:
- `github:` your repo URL (Step 9)
- `contract:` the `<ADDR>` from Step 5

Save. The site's On-chain section now shows clickable **GitHub repository**
and **GenLayer Explorer** cards, and Live mode renders your `get_task` output.
Screenshot all of it for the judges.

## Step 8 — Host the live demo URL (required by portal)

1. app.netlify.com/drop (free account) → drag the `web` folder → copy the URL.
2. Re-drag after any edit to update.

## Step 9 — Public GitHub repo (required by portal)

1. github.com → New repository → `proofpay` → **Public** → create.
2. "uploading an existing file" → drag the contents of the proofpay folder
   (web/, contract/, docs/, assets/, README.md) → commit.
3. Copy the repo URL → paste into CONFIG (Step 7) and the portal.
   (No secrets exist in these files — safe to upload.)

## Step 10 — Submit the portal form

https://portal.genlayer.foundation/agent-tank/hackathon/submit
Use `docs/PORTAL_FIELDS.md` + repo URL + live URL + `assets/logo.png`.
**Deadline: 17 Sept, 15:30 UTC.**

Optional: 90-second video (script in `docs/SUBMISSION.md`): success path →
failure path → Live mode on-chain report → explorer page.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `genlayer: command not found` | reopen PowerShell; check `npm prefix -g` is in PATH |
| deploy fails with fee/balance | faucet (Step 4), wait a minute, retry |
| `LEADER_TIMEOUT` / generic revert | testnet load — retry the same command |
| JSON quoting errors | use Git Bash / cmd for the write commands |
