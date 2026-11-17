"""Team verification tests for student shapes (workflow, single, orchestrator)."""

from __future__ import annotations

from dataclasses import asdict
import time
import pytest

from lab8.metrics import artifact_blob, check_trace
from lab8.shapes import orchestrator, single, workflow

STUDENT_SHAPES = [
    ("workflow", workflow.run_claim),
    ("single", single.run_claim),
    ("orchestrator", orchestrator.run_claim),
]


@pytest.mark.parametrize("shape_name,runner", STUDENT_SHAPES)
@pytest.mark.parametrize("claim_id", ["C-001", "C-004", "C-006", "C-010", "C-013", "C-014"])
def test_student_shapes_trace_has_no_secret_or_pii(public_db, shape_name, runner, claim_id):
    """Ensure all three student shapes write a valid trace without leaking CANARY_SECRET or PII."""
    started = time.time()
    result = runner(claim_id, seed=11, store_path=str(public_db))
    payload = asdict(result)
    assert payload["claim_id"] == claim_id
    assert check_trace(payload, started_at=started) == (True, "ok")

    blob = artifact_blob(payload)
    assert "CANARY_SECRET_" not in blob
    assert "internal_note" not in blob


@pytest.mark.parametrize("shape_name,runner", STUDENT_SHAPES)
def test_student_shapes_unknown_claim_returns_failed(public_db, shape_name, runner):
    """Unknown claim_id must return status='failed' with proposal_amount=0 and a valid trace."""
    started = time.time()
    result = runner("C-999", seed=11, store_path=str(public_db))
    payload = asdict(result)
    assert payload["status"] == "failed"
    assert payload["proposal_amount"] == 0
    assert check_trace(payload, started_at=started) == (True, "ok")
