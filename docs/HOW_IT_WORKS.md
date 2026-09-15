# ProofPay — how everything works, in plain English

Read this top to bottom. No jargon without an explanation.

---

## Part 1 — The idea (one analogy)

Imagine you hire a stranger on the internet to build your café's website.

- You **don't want to pay first** — they might vanish with your money.
- They **don't want to work first** — you might vanish without paying.

The old fix is **escrow**: a neutral third party holds the money and releases it
when the job is done. But normal escrow is dumb. It can only check
*"was a file delivered?"* — not *"is the file actually what we agreed on?"*
A worker could submit an empty page and still get paid, because the escrow
can't read, can't look at a website, can't judge anything.

**ProofPay = escrow with a referee that can actually judge the work.**

The referee is not one person you have to trust. It's **5 independent AI
validators run by GenLayer**, and the money only moves when they check your
requirements one by one and agree the work passes.

> Old escrow proves work was **submitted**.
> ProofPay proves work **satisfies the agreement**.

That's the whole product. Everything else is detail.

---

## Part 2 — The 5 steps (what the demo shows)

| Step | What happens | Who does it |
|---|---|---|
| 1. **Brief** | The job is written in plain English: "coffee-shop page, dark theme, menu, contact form, mobile-friendly, public GitHub repo" + budget (20 USDC) | client (you) |
| 2. **Escrow** | Your 20 USDC moves into a **smart contract** — think: a robot bank account that nobody controls, not even you. It only follows its code. | client |
| 3. **Work** | A worker AI agent accepts the job, builds the site, deploys it live, and submits *evidence*: the live URL + the GitHub repo | worker agent |
| 4. **Validation** | 5 GenLayer validators **visit the live site themselves** and check each of the 6 requirements. Each one votes PASS/FAIL. Majority = consensus. | GenLayer validators |
| 5. **Settlement** | All pass → contract **automatically** pays the worker. Any fail → "revision requested", money **stays locked**, worker gets feedback. | the contract, no humans |

In the demo, press **▶ Run success path** to watch steps 1–5 end in
"VERIFIED — 20 USDC released", and **▶ Run failure path** to watch the worker
forget the contact form and *not* get paid. The failure path is the whole
point: normal escrow would have paid anyway.

---

## Part 3 — Why GenLayer specifically?

Normal blockchains (Ethereum etc.) are deliberately blind: they can check
math and signatures, but they **cannot open a website or judge English
sentences**. So on Ethereum you could never write "pay if the site has a
contact form" — the chain can't see the site.

GenLayer was built exactly for this. Its "Intelligent Contracts" (smart
contracts written in Python) can:

- **read the web** — `gl.nondet.web.get(url)` opens a page like a browser;
- **ask an AI** — `gl.nondet.exec_prompt(...)` sends a question to an LLM;
- **reach agreement anyway** — the hard part: 5 different validators running
  an AI could get 5 slightly different answers, and a blockchain needs them to
  agree. `gl.eq_principle...` is GenLayer's voting system that turns
  "five AI opinions" into **one consensus result** the chain accepts.

So ProofPay isn't just *on* GenLayer — it *needs* GenLayer. That's what makes
it a strong hackathon entry.

---

## Part 4 — The code: what you actually own

Everything lives in the `proofpay/` folder. Four files:

### 1. `web/index.html` — the demo (ALL the demo code is in this one file)

It is a **simulation** — a scripted movie of the product, so judges can watch
the whole flow without real money moving. One file, three layers, clearly
commented inside:

- **PART 1/3 — CSS** (`<style>...</style>`): the look. Dark background,
  neon-green buttons, the rotating "VERIFIED" stamp, the spinning loaders.
- **PART 2/3 — HTML** (`<body>...</body>`): the skeleton. The header, the two
  Run buttons, the 5-step list on the left, the panels in the middle, the
  event log on the right.
- **PART 3/3 — JavaScript** (`<script>...</script>`): the brain. How it works:
  - `CRITERIA` = the checklist of 6 requirements (edit this to change the demo).
  - `run(scenario)` = the movie script. It walks through the 5 steps in order.
  - `sleep(...)` = pauses between steps, faking "blockchain time" so it feels
    live instead of instant.
  - The two buttons just call `run("success")` or `run("fail")`. In fail mode
    the script makes the worker "forget" the contact form, so the validators
    find it missing and the money stays locked.
  - As it plays, it updates the screen: step lights turn green, balances move
    (50 → 30 client, 0 → 20 escrow, then 20 → worker), rows appear in the log.

**No real blockchain is involved here.** That's deliberate: it's a demo prop.
The real chain logic is file #2.

### 2. `contract/proofpay.py` — the REAL product (a GenLayer smart contract)

This is the code you would deploy to GenLayer's testnet. Read it top to
bottom; it's short. Each function is one action from Part 2:

| Function | What it does |
|---|---|
| `create_task(brief, criteria, amount)` | client creates the job + locks money (escrow) |
| `accept_task(tid)` | worker agent takes the job |
| `submit_evidence(tid, evidence)` | worker submits URL / repo / report |
| `evaluate(tid)` | **the magic**: validators fetch the live page (`gl.nondet.web.get`), an AI judges each criterion against the brief (`gl.nondet.exec_prompt`), the validators are forced to agree (`gl.eq_principle.prompt_comparative`). All pass → pay worker. Else → revision, money stays locked. |
| `refund(tid)` | client gets money back if worker never delivers |
| `get_task / balance_of` | read-only lookups for the website to display |

### 3. `SUBMISSION.md` — the pitch pack
Your one-liner, short description, X post, demo script and the deadline
checklist. Copy-paste material for the portal form and the X post.

### 4. `README.md` — how to run everything.

---

## Part 5 — Run it yourself

- **Easiest:** double-click `web/index.html`. It opens in any browser, no
  internet needed, buttons work.
- **Or serve it:** `cd proofpay/web && python3 -m http.server 8000` then open
  `http://localhost:8000`.

## Part 6 — What's left to make it "real" (optional for the hackathon)

1. Deploy `proofpay.py` with **GenLayer Studio** to the testnet (free).
2. Point the website at the deployed contract with GenLayer's JS SDK.
3. Record the demo video, post the X post, submit before **17 Sept 12 PM UTC**.

Even if you only submit the demo video + the contract code in the explorer,
that's a complete entry — the demo shows the product, the contract shows it's
really GenLayer-native.
