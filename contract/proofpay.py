# v0.1.0
# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }
import genlayer as gl
from genlayer import *
import json

"""
ProofPay — outcome-based escrow for the agentic economy.
Studio Next / studio-dev, chain 61997 (GenVM v0.6 runner).

A client locks funds against a plain-English brief. A worker agent submits
evidence of work (live URL + repo). GenLayer validators independently render
the page and judge every criterion against the brief; the equivalence
principle turns those non-deterministic calls into one consensus verdict.
Payment releases only when the brief is met — otherwise funds stay locked
and structured feedback goes back to the worker.
"""

TreeMap = gl.storage.TreeMap


class ProofPay(gl.contract.Contract):
    tasks: TreeMap[str, str]      # task id (str) -> task json
    balances: TreeMap[str, u256]  # address hex -> credited USDC units (escrow ledger)
    next_id: u256

    def __init__(self) -> None:
        self.next_id = 1

    # ------------------------------------------------------------------ client
    @gl.public.write
    def create_task(self, brief: str, criteria_json: str, amount: u256) -> u256:
        """Client creates a job and locks `amount` USDC in escrow."""
        if brief.strip() == "":
            raise gl.vm.UserError("brief is required")
        criteria = json.loads(criteria_json)
        if not isinstance(criteria, list) or len(criteria) == 0:
            raise gl.vm.UserError("criteria_json must be a non-empty JSON array")
        tid = self.next_id
        self.next_id = tid + 1
        task = {
            "id": int(tid),
            "client": gl.message.sender_address.as_hex,
            "brief": brief,
            "criteria": criteria,
            "amount": int(amount),
            "status": "FUNDED",          # FUNDED -> WORKING -> SUBMITTED -> VERIFIED | REVISION
            "worker": "",
            "evidence": {},
            "verdicts": [],
        }
        self.tasks[str(int(tid))] = json.dumps(task)
        return tid

    # ------------------------------------------------------------------ worker
    @gl.public.write
    def accept_task(self, tid: u256) -> None:
        t = json.loads(self.tasks[str(int(tid))])
        if t["status"] != "FUNDED":
            raise gl.vm.UserError("task not open")
        t["worker"] = gl.message.sender_address.as_hex
        t["status"] = "WORKING"
        self.tasks[str(int(tid))] = json.dumps(t)

    @gl.public.write
    def submit_evidence(self, tid: u256, evidence_json: str) -> None:
        t = json.loads(self.tasks[str(int(tid))])
        if t["status"] != "WORKING":
            raise gl.vm.UserError("task not in WORKING state")
        ev = json.loads(evidence_json)
        if not isinstance(ev, dict) or not ev.get("url"):
            raise gl.vm.UserError("evidence_json must include a live url")
        t["evidence"] = ev
        t["status"] = "SUBMITTED"
        self.tasks[str(int(tid))] = json.dumps(t)

    # -------------------------------------------------------------- validation
    @gl.public.write
    def evaluate(self, tid: u256) -> str:
        """Validators fetch the evidence and judge it against the brief.

        Every validator independently renders the URL and prompts an LLM;
        the equivalence principle turns these non-deterministic calls into
        one consensus verdict.
        """
        t = json.loads(self.tasks[str(int(tid))])
        if t["status"] != "SUBMITTED":
            raise gl.vm.UserError("nothing to evaluate")
        url = t["evidence"].get("url", "")
        repo = t["evidence"].get("repo", "")
        brief = t["brief"]
        criteria = t["criteria"]

        def judge() -> str:
            page_text = ""
            try:
                page = gl.nondet.web.get(url)
                page_text = str(getattr(page, "body", "") or "")[:6000]
            except Exception:
                page_text = ""
            prompt = (
                "You are an impartial audit judge for a work contract.\n"
                "BRIEF: " + brief + "\n"
                "ACCEPTANCE CRITERIA: " + json.dumps(criteria) + "\n"
                "EVIDENCE URL: " + url + "\nREPO: " + repo + "\n"
                "RENDERED PAGE TEXT:\n" + page_text + "\n"
                "Decide pass/fail for EACH criterion based on the evidence. "
                "Respond ONLY with JSON, no markdown: "
                '[{"id": "...", "pass": true, "note": "..."}]'
            )
            raw = gl.nondet.exec_prompt(prompt)
            if isinstance(raw, dict):
                return json.dumps(raw)
            text = str(raw).replace("```json", "").replace("```", "").strip()
            return text

        verdict_json = gl.eq_principle.prompt_comparative(
            judge,
            "Two verdicts match if every criterion id has the same pass/fail value.",
        )

        def parse_verdicts(x):
            if isinstance(x, list):
                return x
            if isinstance(x, dict):
                if isinstance(x.get("verdicts"), list):
                    return x["verdicts"]
                return [{"id": k, "pass": bool(v)} for k, v in x.items() if isinstance(v, bool)]
            if isinstance(x, str):
                text = x.replace("```json", "").replace("```", "").strip()
                try:
                    return parse_verdicts(json.loads(text))
                except Exception:
                    s = text.find("[")
                    e = text.rfind("]")
                    if s != -1 and e != -1:
                        try:
                            return json.loads(text[s:e + 1])
                        except Exception:
                            return []
            return []

        verdicts = parse_verdicts(verdict_json)
        all_pass = bool(verdicts) and all(bool(v.get("pass")) for v in verdicts if isinstance(v, dict))
        t["verdicts"] = verdicts

        if all_pass:
            t["status"] = "VERIFIED"
            cur = int(self.balances.get(t["worker"], 0))
            self.balances[t["worker"]] = cur + int(t["amount"])
        else:
            t["status"] = "REVISION"
            t["feedback"] = [v for v in verdicts if not v.get("pass")]
        self.tasks[str(int(tid))] = json.dumps(t)
        return json.dumps(t["verdicts"])

    @gl.public.write
    def refund(self, tid: u256) -> None:
        """Client refund path if the worker never delivers."""
        t = json.loads(self.tasks[str(int(tid))])
        if gl.message.sender_address.as_hex != t["client"]:
            raise gl.vm.UserError("only the client can refund")
        if t["status"] not in ("FUNDED", "WORKING", "REVISION"):
            raise gl.vm.UserError("task already settled")
        t["status"] = "REFUNDED"
        self.tasks[str(int(tid))] = json.dumps(t)

    # ------------------------------------------------------------------- views
    @gl.public.view
    def get_task(self, tid: u256) -> str:
        return self.tasks.get(str(int(tid))) or ""

    @gl.public.view
    def balance_of(self, who: str) -> u256:
        return self.balances.get(who, 0)
