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

import json
import sqlite3
from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import get_claim_view, tool_cost
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

    # Fetch the claim — counts as one tool call.
    budget.add_tool(tool_cost())
    claim_view = get_claim_view(conn, claim_id)
    trace.add(
        "claim_view",
        safe_dump({k: claim_view[k] for k in ("found", "claim_id", "order_id") if k in claim_view}),
    )

    if not claim_view.get("found"):
        trace.add("decision", {"status": "failed", "error_reason": "unknown_claim"})
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

    principal_id: str = claim_view.get("principal_id", "")
    # memo persists order data across decide() calls because run_react only
    # keeps {last_tool, last_result, claim} between steps.
    memo: dict[str, Any] = {}

    def decide(obs: dict[str, Any]) -> dict[str, Any]:
        """ReAct decide function. Calls MockLLM on every reason step."""
        last_tool = obs.get("last_tool")
        last_result = obs.get("last_result") or {}
        claim = obs.get("claim") or {}

        # Reason step — call MockLLM so cost is counted fairly.
        complete(
            budget,
            seed=seed,
            purpose="reason",
            prompt=json.dumps(
                {"last_tool": last_tool, "last_result": last_result},
                ensure_ascii=False,
                default=str,
            ),
        )

        # --- Initial state: no tool called yet ---
        if last_tool is None:
            order_id = claim.get("order_id")
            if not order_id:
                return {
                    "final": {
                        "status": "needs_info",
                        "proposal_amount": 0,
                        "error_reason": "missing_order_id",
                    }
                }
            return {
                "tool": "lookup_order",
                "args": {"order_id": order_id, "principal_id": principal_id},
            }

        # --- After lookup_order ---
        if last_tool == "lookup_order":
            if not last_result.get("visible"):
                return {
                    "final": {
                        "status": "escalated",
                        "proposal_amount": 0,
                        "error_reason": last_result.get("reason"),
                    }
                }
            # Save in memo — seen will be overwritten next step.
            memo["order"] = last_result["order"]
            return {
                "tool": "compute_compensation",
                "args": {"order": memo["order"]},
            }

        # --- After compute_compensation ---
        if last_tool == "compute_compensation":
            amount = int(last_result.get("amount_vnd", 0))
            if amount <= 0:
                return {
                    "final": {
                        "status": "denied",
                        "proposal_amount": 0,
                        "error_reason": last_result.get("reason"),
                    }
                }
            return {
                "final": {
                    "status": "approved",
                    "proposal_amount": amount,
                }
            }

        # Fallback — should not normally reach here within 8 steps.
        return {
            "final": {
                "status": "failed",
                "proposal_amount": 0,
                "error_reason": "unexpected_state",
            }
        }

    # --- Run the bounded ReAct loop ---
    react_result = run_react(
        conn,
        budget,
        observation={"claim": claim_view},
        decide=decide,
        max_steps=8,
        worker=True,
    )

    final = react_result["final"]
    agent_status = final.get("status")
    proposal_amount = int(final.get("proposal_amount", 0))
    trace.add("react_final", safe_dump(final))

    # --- needs_info ---
    if agent_status == "needs_info":
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="needs_info",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=final.get("error_reason"),
        )

    # --- escalated ---
    if agent_status == "escalated":
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="escalated",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=final.get("error_reason"),
        )

    # --- denied (agent decided no entitlement) ---
    if agent_status == "denied":
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="denied",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=final.get("error_reason"),
        )

    # --- failed / step_cap ---
    if agent_status == "failed":
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=final.get("error_reason") or "step_cap",
        )

    # --- approved: host is the only writer ---
    if agent_status == "approved":
        # Draft reply — counts one more model call like the reference swarm does.
        complete(budget, seed=seed, purpose="draft", prompt=f"proposal={proposal_amount}")

        # Pass crash_at through; never catch InjectedCrash — let it propagate.
        try:
            outcome = issue_refund(conn, claim_id, proposal_amount, crash_at=crash_at)
        except InjectedCrash:
            trace.add("crash", {"at": crash_at})
            trace.write()
            raise

        trace.add(
            "issue_refund",
            safe_dump({"ok": outcome["ok"], "reason": outcome["reason"]}),
        )

        if not outcome["ok"]:
            status = "failed" if outcome["conflict"] else "denied"
            return finish(
                conn,
                shape="single",
                claim_id=claim_id,
                seed=seed,
                status=status,
                proposal_amount=proposal_amount,
                budget=budget,
                trace=trace,
                error_reason=outcome["reason"],
            )

        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="resolved",
            proposal_amount=proposal_amount,
            budget=budget,
            trace=trace,
        )

    # Catch-all for any unrecognised agent status.
    return finish(
        conn,
        shape="single",
        claim_id=claim_id,
        seed=seed,
        status="failed",
        proposal_amount=0,
        budget=budget,
        trace=trace,
        error_reason=f"unknown_agent_status:{agent_status}",
    )
