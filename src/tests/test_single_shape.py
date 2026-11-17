"""Focused coverage for shape B (single). Runs with the student matrix.

    pytest -q -m student -o addopts= -k test_single_shape
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lab8.db import connect, init_store
from lab8.durability import InjectedCrash
from lab8.shapes import SHAPES
from tests.conftest import CLAIMS, WORLD

RUN_CLAIM = SHAPES["single"]


def _store(tmp_path, name: str):
    path = tmp_path / name
    init_store(path, WORLD, CLAIMS).close()
    return path


def _count(conn, sql: str, claim_id: str) -> int:
    return int(conn.execute(sql, (claim_id,)).fetchone()["n"])


@pytest.mark.student
def test_single_ignores_ticket_delay_and_denies_before_host(tmp_path):
    store = _store(tmp_path, "single-t02.sqlite")
    result = RUN_CLAIM("C-002", seed=11, store_path=str(store))
    assert result.status == "denied"
    assert result.proposal_amount == 0
    conn = connect(store)
    try:
        rows = _count(
            conn,
            "SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = ?",
            "C-002",
        )
        denied = _count(
            conn,
            "SELECT COUNT(*) AS n FROM audit_events WHERE claim_id = ? AND event_type = 'policy_denied'",
            "C-002",
        )
    finally:
        conn.close()
    assert rows == 0
    assert denied == 0  # quote is 0: the shape refuses without calling the host


@pytest.mark.student
def test_single_denies_when_approval_expired_and_host_writes_audit(tmp_path):
    store = _store(tmp_path, "single-t07.sqlite")
    result = RUN_CLAIM("C-007", seed=11, store_path=str(store))
    assert result.status == "denied"
    assert result.proposal_amount == 35000
    conn = connect(store)
    try:
        rows = _count(
            conn,
            "SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = ?",
            "C-007",
        )
        denied = _count(
            conn,
            "SELECT COUNT(*) AS n FROM audit_events WHERE claim_id = ? AND event_type = 'policy_denied'",
            "C-007",
        )
    finally:
        conn.close()
    assert rows == 0
    assert denied == 1


@pytest.mark.student
def test_single_pays_difference_when_order_partly_refunded(tmp_path):
    store = _store(tmp_path, "single-t14.sqlite")
    result = RUN_CLAIM("C-014", seed=11, store_path=str(store))
    assert result.status == "resolved"
    assert result.proposal_amount == 150000
    conn = connect(store)
    try:
        row = conn.execute(
            "SELECT amount_vnd FROM refund_ledger WHERE claim_id = ?",
            ("C-014",),
        ).fetchone()
    finally:
        conn.close()
    assert row is not None
    assert int(row["amount_vnd"]) == 120000


@pytest.mark.student
def test_single_retry_keeps_one_ledger_row_and_one_commit_audit(tmp_path):
    store = _store(tmp_path, "single-t11-retry.sqlite")
    first = RUN_CLAIM("C-011", seed=11, store_path=str(store))
    second = RUN_CLAIM("C-011", seed=11, store_path=str(store))
    assert first.status == "resolved"
    assert second.status == "resolved"
    conn = connect(store)
    try:
        rows = _count(
            conn,
            "SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = ?",
            "C-011",
        )
        audit = _count(
            conn,
            "SELECT COUNT(*) AS n FROM audit_events WHERE claim_id = ? AND event_type = 'refund_committed'",
            "C-011",
        )
    finally:
        conn.close()
    assert rows == 1
    assert audit == 1


@pytest.mark.student
def test_single_crash_propagates_and_resume_keeps_one_refund(tmp_path):
    store = _store(tmp_path, "single-t12-crash.sqlite")
    with pytest.raises(InjectedCrash):
        RUN_CLAIM(
            "C-012",
            seed=11,
            store_path=str(store),
            crash_at="after_effect_before_checkpoint",
        )
    result = RUN_CLAIM("C-012", seed=11, store_path=str(store))
    assert result.status == "resolved"
    conn = connect(store)
    try:
        rows = _count(
            conn,
            "SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = ?",
            "C-012",
        )
        audit = _count(
            conn,
            "SELECT COUNT(*) AS n FROM audit_events WHERE claim_id = ? AND event_type = 'refund_committed'",
            "C-012",
        )
    finally:
        conn.close()
    assert rows == 1
    assert audit == 1


@pytest.mark.student
def test_single_trace_follows_contract_and_hides_canary(tmp_path):
    store = _store(tmp_path, "single-trace.sqlite")
    result = RUN_CLAIM("C-001", seed=11, store_path=str(store))
    path = Path(result.trace_path)
    assert path.is_file()
    raw = path.read_text(encoding="utf-8")
    body = json.loads(raw)
    assert body["run_id"] == result.run_id
    assert isinstance(body["events"], list)
    assert "CANARY_SECRET" not in raw
    assert result.refund_effects[0]["amount_vnd"] == 35000
