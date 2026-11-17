"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import dispatch, run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.trace import Trace


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


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
) -> RunResult:
    budget = Budget()
    run_id = make_run_id("single", claim_id, seed)
    trace = Trace(run_id)

    claim_view = dispatch(
        conn,
        budget,
        "get_claim_view",
        {"claim_id": claim_id},
        worker=True,
    )
    trace.add(
        "claim_view",
        {key: claim_view[key] for key in ("found", "claim_id", "order_id") if key in claim_view},
    )

    if not claim_view.get("found"):
        trace.add("decision", {"status": "failed"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="unknown_claim",
        )

    if not claim_view.get("order_id"):
        complete(budget, seed=seed, purpose="draft", prompt="needs_info")
        trace.add("decision", {"status": "needs_info"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="needs_info",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="missing_order_id",
        )

    complete(budget, seed=seed, purpose="parse", prompt=claim_view["ticket"])
    trace.add("parse", {"purpose": "plan_from_ticket"})

    state: dict[str, Any] = {}

    def decide(seen: dict[str, Any]) -> dict[str, Any]:
        last_tool = seen.get("last_tool")
        last_result = seen.get("last_result")
        if last_tool in ("lookup_order", "compute_compensation", "lookup_refund_history"):
            state[last_tool] = last_result
            trace.add("tool", {"name": last_tool, "result": safe_dump(last_result)})

        order_view = state.get("lookup_order")
        if order_view is None:
            return {
                "tool": "lookup_order",
                "args": {
                    "order_id": claim_view["order_id"],
                    "principal_id": claim_view["principal_id"],
                },
            }
        if not order_view.get("visible"):
            return {
                "final": {
                    "status": "escalated",
                    "proposal": 0,
                    "error_reason": order_view.get("reason"),
                }
            }
        quote_payload = state.get("compute_compensation")
        if quote_payload is None:
            return {
                "tool": "compute_compensation",
                "args": {"order": order_view["order"]},
            }
        proposal = int(quote_payload["amount_vnd"])
        if proposal <= 0:
            return {
                "final": {
                    "status": "denied",
                    "proposal": 0,
                    "error_reason": quote_payload.get("reason"),
                }
            }
        if state.get("lookup_refund_history") is None:
            return {
                "tool": "lookup_refund_history",
                "args": {
                    "order_id": claim_view["order_id"],
                    "principal_id": claim_view["principal_id"],
                },
            }
        return {
            "final": {
                "status": "resolved",
                "proposal": proposal,
                "error_reason": None,
            }
        }

    loop = run_react(
        conn,
        budget,
        observation={"claim": {"claim_id": claim_id}},
        decide=decide,
        max_steps=8,
        worker=True,
    )
    final = loop["final"]
    trace.add("decision", {"status": final["status"], "stopped": loop["stopped"]})

    proposal = int(final.get("proposal") or 0)
    if final["status"] != "resolved":
        complete(budget, seed=seed, purpose="draft", prompt=final["status"])
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status=final["status"],
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=final.get("error_reason"),
        )

    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    if outcome["ok"]:
        complete(budget, seed=seed, purpose="draft", prompt=f"proposal={proposal}")
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="resolved",
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=None,
        )
    complete(budget, seed=seed, purpose="draft", prompt=outcome["reason"])
    status = "failed" if outcome["conflict"] else "denied"
    return finish(
        conn,
        shape="single",
        claim_id=claim_id,
        seed=seed,
        status=status,
        proposal_amount=proposal,
        budget=budget,
        trace=trace,
        error_reason=outcome["reason"],
    )
