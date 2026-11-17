"""Shape C — orchestrator plus read-only investigators. Student work.

1. Build a handoff with `lab8.handoff.make_handoff`. Allowed tools are read-only.
   Never put parent_secret, raw headers, or the full claim row into facts.
2. `lab8.runtime.run_readonly_investigators` runs those tools.
3. The orchestrator quotes from the investigator's order view and calls
   `durability.issue_refund`. Investigators have no write registry.
   Pass the full quote; the host subtracts earlier refunds on the same order.
   `lookup_refund_history` is a read-only tool you may hand to an investigator.
4. Trace the sanitized handoff, not the parent context.

An LLM summary of the parent context is not a sanitizer. Use the allowlist.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

import sqlite3

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.handoff import make_handoff
from lab8.mock_llm import complete
from lab8.runtime import run_readonly_investigators
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace

INVESTIGATOR_TOOLS = ["lookup_order", "lookup_policy", "compute_compensation"]


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(conn: sqlite3.Connection, claim_id: str, *, seed: int, crash_at: str | None) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id("orchestrator", claim_id, seed))
    budget.add_tool(tool_cost())

    claim_view = get_claim_view(conn, claim_id)
    if not claim_view["found"]:
        trace.add("error", {"reason": "unknown_claim"})
        return _finish(conn, trace, claim_id, seed, status="failed", proposal=0, budget=budget, error="unknown_claim")
    trace.add("claim", {key: claim_view[key] for key in ("found", "claim_id", "order_id") if key in claim_view})

    if not claim_view["order_id"]:
        complete(budget, seed=seed, purpose="draft", prompt="needs_info")
        trace.add("decision", {"status": "needs_info"})
        return _finish(conn, trace, claim_id, seed, status="needs_info", proposal=0, budget=budget, error="missing_order_id")

    handoff = make_handoff(
        request_id=f"REQ-{claim_id}",
        claim_id=claim_id,
        task="check_applicable_policy",
        facts={},
        allowed_tools=INVESTIGATOR_TOOLS,
    )
    trace.add("handoff", safe_dump(handoff))

    investigated = run_readonly_investigators(conn, budget, handoff, principal_id=claim_view["principal_id"])
    tools = investigated["tools"]
    order_view = tools.get("lookup_order") or {}
    trace.add(
        "investigator",
        {
            "lookup_order": order_view,
            "policy_count": len((tools.get("lookup_policy") or {}).get("policies") or []),
        },
    )

    if not order_view.get("visible"):
        complete(budget, seed=seed, purpose="draft", prompt="escalated")
        trace.add("decision", {"status": "escalated"})
        return _finish(conn, trace, claim_id, seed, status="escalated", proposal=0, budget=budget, error=order_view.get("reason"))

    quote_payload = tools["compute_compensation"]
    proposal = int(quote_payload["amount_vnd"])
    trace.add("quote", quote_payload)
    complete(budget, seed=seed, purpose="draft", prompt=f"proposal={proposal}")

    if proposal <= 0:
        trace.add("decision", {"status": "denied", "reason": quote_payload.get("reason")})
        return _finish(conn, trace, claim_id, seed, status="denied", proposal=0, budget=budget, error=quote_payload.get("reason"))

    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    if not outcome["ok"]:
        status = "failed" if outcome["conflict"] else "denied"
        trace.add("decision", {"status": status, "reason": outcome["reason"]})
        return _finish(conn, trace, claim_id, seed, status=status, proposal=proposal, budget=budget, error=outcome["reason"])

    trace.add("decision", {"status": "resolved"})
    return _finish(conn, trace, claim_id, seed, status="resolved", proposal=proposal, budget=budget, error=None)


def _finish(
    conn: sqlite3.Connection,
    trace: Trace,
    claim_id: str,
    seed: int,
    *,
    status: str,
    proposal: int,
    budget: Budget,
    error: str | None,
) -> RunResult:
    return finish(
        conn,
        shape="orchestrator",
        claim_id=claim_id,
        seed=seed,
        status=status,
        proposal_amount=proposal,
        budget=budget,
        trace=trace,
        error_reason=error,
    )
