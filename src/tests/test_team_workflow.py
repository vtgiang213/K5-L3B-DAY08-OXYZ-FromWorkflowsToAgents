import pytest

from lab8.db import connect
from lab8.durability import InjectedCrash, committed_audit_count, get_refund
from lab8.shapes.workflow import run_claim


def test_workflow_crash_before_effect_then_retry(public_db):
    claim_id = "C-001"

    with pytest.raises(InjectedCrash):
        run_claim(claim_id, seed=11, store_path=str(public_db), crash_at="before_effect")

    conn = connect(public_db)
    try:
        assert get_refund(conn, claim_id) is None
        assert committed_audit_count(conn, claim_id) == 0
    finally:
        conn.close()

    result = run_claim(claim_id, seed=11, store_path=str(public_db))

    conn = connect(public_db)
    try:
        count = conn.execute(
            "SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = ?", (claim_id,)
        ).fetchone()["n"]
        effect = get_refund(conn, claim_id)
        assert result.status == "resolved"
        assert count == 1
        assert effect["amount_vnd"] == 35000
        assert committed_audit_count(conn, claim_id) == 1
    finally:
        conn.close()
