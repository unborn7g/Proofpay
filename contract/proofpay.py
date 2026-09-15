# { "Depends": "py-genlayer:latest" }
#
# ProofPay — outcome-based escrow for the agentic economy.
# Reference Intelligent Contract for the Agent Tank hackathon build.
#
# This mirrors the demo in ../index.html with the real GenVM SDK shape
# (gl.nondet web/LLM access + eq_principle consensus). Adapt names/payment
# calls to the current GenLayer testnet docs when wiring real test-USDC.

from genlayer import *
import json


class ProofPay(gl.Contract):
    """
    A client locks funds against a plain-English brief.
    A worker agent submits evidence of work.
    GenLayer validators independently evaluate the outcome against the brief.
    Payment releases only when the brief is met.
    """

    tasks: TreeMap[int, str]      # task id -> task json
    balances: TreeMap[str, int]   # address hex -> credited USDC units (ledger)
    next_id: int

    def __init__(self):
        self.next_id = 1

    # ------------------------------------------------------------------ client
    @gl.public.write
    def create_task(self, brief: str, criteria_json: str, amount: int) -> int:
        """Client creates a job and locks `amount` USDC in escrow.

        NOTE (testnet build): make this payable and transfer test-USDC into
        the contract per the GenLayer docs; the ledger below models escrow.
        """
        tid = self.next_id
        self.next_id += 1
        task = {
            "id": tid,
            "client": gl.message.sender_address.as_hex,
            "brief": brief,
            "criteria": json.loads(criteria_json),
            "amount": amount,
            "status": "FUNDED",          # FUNDED -> SUBMITTED -> VERIFIED | REVISION
            "worker": "",
            "evidence": {},
            "verdicts": [],
        }
        self.tasks[tid] = json.dumps(task)
        return tid

    # ------------------------------------------------------------------ worker
    @gl.public.write
    def accept_task(self, tid: int) -> None:
        t = json.loads(self.tasks[tid])
        assert t["status"] == "FUNDED", "task not open"
        t["worker"] = gl.message.sender_address.as_hex
        t["status"] = "WORKING"
        self.tasks[tid] = json.dumps(t)

    @gl.public.write
    def submit_evidence(self, tid: int, evidence_json: str) -> None:
        """Worker submits proof of work: {url, repo, report, ...} per template."""
        t = json.loads(self.tasks[tid])
        assert gl.message.sender_address.as_hex == t["worker"], "not the worker"
        assert t["status"] == "WORKING", "not in work phase"
        t["evidence"] = json.loads(evidence_json)
        t["status"] = "SUBMITTED"
        self.tasks[tid] = json.dumps(t)

    # -------------------------------------------------------------- validation
    @gl.public.write
    def evaluate(self, tid: int) -> str:
        """Validators fetch the evidence and judge it against the brief.

        Every validator independently renders the page and prompts an LLM;
        the eq_principle turns these non-deterministic calls into consensus.
        """
        t = json.loads(self.tasks[tid])
        assert t["status"] == "SUBMITTED", "nothing to evaluate"

        # 1) deterministic-ish shared evidence: all validators render the URL
        url = t["evidence"].get("url", "")

        def fetch_page() -> str:
            _u = url  # capture for closure
            def get() -> str:
                return gl.nondet.web.render(_u, mode="text")
            return gl.eq_principle.strict_eq(get)

        page_text = fetch_page() if url else ""

        # 2) judgment: per-criterion pass/fail against the natural-language brief
        prompt = (
            "You are an impartial audit judge for a work contract.\n"
            f"BRIEF: {t['brief']}\n"
            f"ACCEPTANCE CRITERIA: {json.dumps(t['criteria'])}\n"
            f"EVIDENCE URL: {url}\nREPO: {t['evidence'].get('repo', '')}\n"
            f"RENDERED PAGE TEXT:\n{page_text[:6000]}\n"
            "Decide pass/fail for EACH criterion based on the evidence. "
            "Reply ONLY with JSON: [{\"id\": \"...\", \"pass\": true, \"note\": \"...\"}]"
        )

        def call_llm() -> str:
            return gl.nondet.exec_prompt(prompt)

        verdict_json = gl.eq_principle.prompt_comparative(
            call_llm,
            "Two verdicts match if every criterion has the same pass/fail value.",
        )

        verdicts = json.loads(verdict_json)
        all_pass = all(v["pass"] for v in verdicts)
        t["verdicts"] = verdicts

        # ------------------------------------------------------------------ settle
        if all_pass:
            t["status"] = "VERIFIED"
            # release escrow to worker (testnet build: transfer test-USDC out)
            cur = int(self.balances.get(t["worker"], "0"))
            self.balances[t["worker"]] = str(cur + t["amount"])
        else:
            # funds stay locked; structured feedback goes back to the worker
            t["status"] = "REVISION"
            t["feedback"] = [v for v in verdicts if not v["pass"]]

        self.tasks[tid] = json.dumps(t)
        return verdict_json

    @gl.public.write
    def refund(self, tid: int) -> None:
        """Client refund path if the worker never submits (add deadline logic)."""
        t = json.loads(self.tasks[tid])
        assert gl.message.sender_address.as_hex == t["client"]
        assert t["status"] in ("FUNDED", "WORKING", "REVISION")
        t["status"] = "REFUNDED"
        self.tasks[tid] = json.dumps(t)

    # ------------------------------------------------------------------- views
    @gl.public.view
    def get_task(self, tid: int) -> str:
        return self.tasks.get(tid, "")

    @gl.public.view
    def balance_of(self, who: str) -> str:
        return self.balances.get(who, "0")
