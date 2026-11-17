# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |        |      |       |        |         |
|   2 | Đinh Quốc Việt | 2A202603885 | 26ai.vietdq3@vinuni.edu.vn | KemmVSAI | Single agent |
|   3 | Lê Sỹ Long Nhật | 2A202603881 | 26ai.nhatlsl@vinuni.edu.vn | longnhat2kruoi | Orchestrator + handoff |

| Người | Phần việc chính | Đầu ra và kiểm tra |
|---|---|---|
| **1 — Workflow + tích hợp** | Viết shape A trong [workflow.py](<D:/AI in action/Day 8/K5-L3B-DAY08-OXYZ-FromWorkflowsToAgents/src/lab8/shapes/workflow.py>); ghép code của các bạn, xử lý xung đột và kiểm tra toàn bộ bài. Phụ trách hoàn thiện `TEAM.md` và checklist nộp. | Workflow chạy đúng contract, có test riêng; chạy lại toàn bộ test và `check_submission` trước khi push. |
| **2 — Single agent** | Viết shape B trong [single.py](<D:/AI in action/Day 8/K5-L3B-DAY08-OXYZ-FromWorkflowsToAgents/src/lab8/shapes/single.py>): vòng ReAct tối đa 8 bước, model chỉ chọn tool đọc; code thực hiện hoàn tiền qua host. | Single qua bộ test của shape, có test riêng; phối hợp xử lý các tình huống approval, chạy lại và crash. |
| **3 — Orchestrator + handoff** | Viết shape C trong [orchestrator.py](<D:/AI in action/Day 8/K5-L3B-DAY08-OXYZ-FromWorkflowsToAgents/src/lab8/shapes/orchestrator.py>); đảm bảo investigator chỉ dùng tool đọc, handoff theo allowlist và trace không lộ secret/PII. | Orchestrator qua bộ test của shape, có test riêng; kiểm tra handoff, trace và các nhánh trả kết quả. |
| **4 — An toàn ledger + đánh giá** | Rà idempotency, approval và crash trên cả ba shape; chạy crash suite, benchmark và hỗ trợ nhóm đọc kết quả. Chủ trì `decision_adr.md`, `research_card.md` và tổng hợp báo cáo nhóm. | Crash safety **20/20**; benchmark đủ 4 shape, ít nhất 10 claim và 5 seed; có test riêng và số liệu thực tế trong báo cáo. Các lỗi trong shape chuyển lại người phụ trách sửa. |

Thứ tự phối hợp:
1. CP1: Cài môi trường, đọc contract, điền tên và vai trò vào TEAM.md.
2. CP2–CP3: Người 1–3 làm ba shape song song; người 4 chuẩn bị test an toàn và hỗ trợ kiểm tra crash, approval, handoff.
3. CP4: Cả nhóm xử lý ba điều kiện bắt buộc: approval hợp lệ, không lộ secret, crash không tạo refund trùng.
4. CP5: Người 4 chạy benchmark và tổng hợp số liệu; cả nhóm chọn kiến trúc dựa trên kết quả. Người 1 kiểm tra bài nộp, các thành viên hoàn thiện báo cáo cá nhân.
Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Lê Sỹ Long Nhật | Orchestrator + handoff | d64c2c3 | Chưa thêm test riêng cho shape orchestrator |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603881_LeSyLongNhat

### Phần việc phụ trách

- Shape C — Orchestrator + handoff: `src/lab8/shapes/orchestrator.py`.

### Đóng góp cụ thể

- Viết `run_claim` của shape orchestrator: tạo handoff qua `lab8.handoff.make_handoff` với allowlist chỉ tool đọc (`lookup_order`, `lookup_policy`, `compute_compensation`), chạy investigator qua `lab8.runtime.run_readonly_investigators`.
- Orchestrator trích quote từ `compute_compensation` và gọi `durability.issue_refund` với giá quote đầy đủ (host tự trừ refund trước trên cùng đơn).
- Xử lý trọn các nhánh trả kết quả: `needs_info` khi thiếu `order_id`, `escalated` khi investigator không thấy đơn, `denied` khi quote ≤ 0 hoặc host từ chối, `failed` khi conflict.
- Trace theo contract v1: ghi handoff đã sanitize (không secret/PII, không raw header, không claim row đầy đủ), mọi nhánh return đều sinh file trace với đúng `run_id`.

### Bằng chứng

- Commit `d64c2c3` — Implement Orchestrator Shape (PR #2), file `src/lab8/shapes/orchestrator.py`.
- Bộ test shape và crash suite của nhóm: chạy lại trước khi nộp (người 4 tổng hợp kết quả).
