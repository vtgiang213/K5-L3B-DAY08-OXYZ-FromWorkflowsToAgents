# Báo cáo cá nhân — 2A202603935_VuQuangHai

## 1. Thông tin thành viên

- Họ tên: Vũ Quang Hải
- MSSV: 2A202603935
- Email: haivq25@gmail.com
- GitHub: HaiVuQ

## 2. Phần việc phụ trách

Người 4 — An toàn ledger + đánh giá (CP4–CP5): thiết lập môi trường kiểm thử chuẩn (`Python 3.12.10` trong `src/.venv`), rà soát an toàn trace/secret/PII, chạy crash suite và benchmark cho cả 4 shape, bổ sung test kiểm tra cho 3 shape học viên viết, chủ trì `decision_adr.md`, `research_card.md` và tổng hợp `group_report.md`.

## 3. Đóng góp cụ thể

- Thiết lập môi trường Python `3.12.10` (`src/.venv`) và chạy xác minh `lab8.smoke`, cổng host (`pytest -q`), ma trận student (`pytest -q -m student -o addopts=`).
- Viết bổ sung `src/tests/test_team_shapes.py` (21 test case) kiểm tra cả 3 shape `workflow`, `single`, `orchestrator`: đảm bảo trace đúng Trace contract v1, không rò rỉ `CANARY_SECRET_*` hay `internal_note`, và xử lý claim không tồn tại (`C-999`) trả về `status="failed"`, `proposal_amount=0`.
- Chạy crash suite 20 kịch bản (`lab8.crash_test`) sinh `src/reports/crash.json` đạt `20/20`.
- Chạy benchmark đầy đủ 4 shape × 14 claim × 5 seed (`11,22,33,44,55`, tổng 280 trial) sinh `src/reports/benchmark.json`.
- Hoàn thiện `report/team/decision_adr.md` (chọn `workflow`), `report/team/research_card.md` (R3 + URL arXiv:2509.10769 + kết quả ablation), `report/team/group_report.md` và `TEAM.md`.

## 4. Bằng chứng

- Cổng host (gồm test bổ sung): `python -m pytest -q` → `75 passed, 248 deselected`.
- Ma trận student: `python -m pytest -q -m student -o addopts=` → `248 passed, 54 deselected`.
- Crash suite: `python -m lab8.crash_test --count 20 --out reports/crash.json` → `crash_safety 20/20` (`src/reports/crash.json`).
- Benchmark: `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json` → `workflow` đạt `pass_rate = 1.000`, `pass^5 = 1.000`, `seed_variance = 0.000000`, `cost/success = 27.86 VND` (`src/reports/benchmark.json`).
- Kiểm tra nộp bài: `python -m lab8.check_submission` → `0 FAIL`.

## 5. Công cụ AI đã dùng

- Antigravity / Gemini: hỗ trợ thiết lập môi trường Python 3.12, chạy kiểm thử và tổng hợp số liệu từ `benchmark.json` và `crash.json` vào các báo cáo. Toàn bộ kết quả được tự kiểm chứng trực tiếp bằng `pytest`, `crash_test`, `benchmark` và `check_submission`.

## 6. Tự đánh giá

Đã hoàn thành đầy đủ phần việc của người 4: xác minh 3 shape đạt chuẩn an toàn (không lộ secret/PII, crash safety `20/20`), hoàn tất số liệu benchmark và toàn bộ hồ sơ nộp bài (`decision_adr.md`, `research_card.md`, `group_report.md`, `TEAM.md`, báo cáo cá nhân).
