# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: OXYZ
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`): 61752ba

## 2. Mục tiêu và cách tiếp cận

Bài toán xử lý yêu cầu hoàn phí vận chuyển (claim) cho LogiX-VN yêu cầu cùng một quy trình nghiệp vụ được triển khai trên bốn kiến trúc có mức tự chủ tăng dần: `workflow` (A), `single` (B), `orchestrator` (C), và `swarm` (D, có sẵn để đối chứng). Nhóm chia việc theo từng shape và kiểm thử an toàn:

1. **CP1:** Cài môi trường Python 3.12 trong `src/.venv`, chạy `lab8.smoke` và cổng host `pytest -q`.
2. **CP2–CP3:** Triển khai `workflow.py`, `single.py`, `orchestrator.py` tuân thủ `docs/business_rules.md` và `docs/contracts.md`: tính tiền bằng `compute_compensation`, truyền quote đầy đủ vào `durability.issue_refund(..., crash_at=crash_at)` và không bắt `InjectedCrash` (trừ việc ghi trace rồi re-raise ở `single` và `orchestrator`).
3. **CP4–CP5:** Chạy `lab8.crash_test` (20 kịch bản), `lab8.benchmark` (4 shape × 14 claim × 5 seed), bổ sung test bảo mật/contract trong `src/tests/test_team_shapes.py`, rồi chọn kiến trúc ít tự chủ nhất đạt yêu cầu.

## 3. Giải pháp

- **Shape A (`workflow` — `src/lab8/shapes/workflow.py`):** Luồng Python tuần tự cố định: `get_claim_view` → kiểm tra `order_id` (`needs_info`) → `lookup_order` (`escalated` nếu không visible) → `compute_compensation` (`denied` nếu quote ≤ 0) → `durability.issue_refund` với quote đầy đủ → `finish()`. Không gọi `MockLLM`, giữ `mean_steps = 1.86` và `cost/success = 27.86 VND`.
- **Shape B (`single` — `src/lab8/shapes/single.py`):** Sử dụng `lab8.runtime.run_react` với `max_steps = 8`. Callback `decide` chỉ gọi các tool đọc (`lookup_order`, `compute_compensation`, `lookup_refund_history`); `MockLLM` chỉ dùng để `parse` ticket và `draft` phản hồi. Sau vòng ReAct, code Python gọi `issue_refund` và re-raise `InjectedCrash` sau khi ghi trace.
- **Shape C (`orchestrator` — `src/lab8/shapes/orchestrator.py`):** Orchestrator tạo gói `handoff` qua `lab8.handoff.make_handoff` với `facts={}` và danh sách tool chỉ đọc `["lookup_order", "lookup_policy", "compute_compensation"]`, chạy `run_readonly_investigators`, rồi tự gọi `issue_refund` với quote đầy đủ.
- **Ranh giới bảo mật & Trace:** Cả 3 shape chỉ ghi các trường qua allowlist vào `lab8.trace.Trace`, tuyệt đối không ghi `parent_secret` (`CANARY_SECRET_*`), SĐT, địa chỉ hay `internal_note`.

## 4. Kết quả

Bảng so sánh 4 shape trên bộ public (`src/reports/benchmark.json`, 14 claim × 5 seed `11, 22, 33, 44, 55` = 70 trial/shape):

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND) | Mean steps | P95 steps |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `workflow` | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 27.86 | 1.86 | 2.0 |
| `single` | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 35.67 | 5.36 | 6.0 |
| `orchestrator` | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 47.36 | 4.71 | 5.0 |
| `swarm` | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 | 3.0 |

- **Crash safety (`src/reports/crash.json`):** `20/20` (`CR-01` đến `CR-20`, gồm `before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`, `amount_conflict_on_retry`, `retry_without_approval`).
- **Tự kiểm hidden:** Không có thư mục `student_drop/` trong repo tại thời điểm chạy CP5.

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

- **Phiên bản Python trên máy:** Khi chạy `python -m lab8.smoke` bằng Python hệ thống (`3.10.0`), lab báo `Python 3.10.0 quá cũ. Cần Python 3.11+`. Nhóm đã cài đặt Python `3.12.10`, tạo virtualenv `src/.venv` và cài `requirements.txt` để chạy đầy đủ `smoke`, `pytest`, `crash_test`, `benchmark` và `check_submission`.
- **Timeout mạng khi cài pip:** Lần cài đầu gặp `ReadTimeoutError` từ `files.pythonhosted.org`; xử lý bằng cờ `--default-timeout=120`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`. Các số đo chi phí là VND mô phỏng theo `src/config/pricing.yaml`, chưa phản ánh độ trễ mạng hay chi phí prompt thực tế của LLM. Hướng cải thiện: đánh giá thêm trên bộ hidden `student_drop/` khi có dữ liệu và kiểm thử với LLM thật có cơ chế rate-limit/retry.

## 8. Tài liệu tham khảo

- `README.md`, `CHECKPOINTS.md`, `RUBRIC.md`, `RULES.md`, `SUBMISSION.md`
- `docs/business_rules.md`, `docs/contracts.md`, `docs/architecture.md`, `docs/metrics.md`
