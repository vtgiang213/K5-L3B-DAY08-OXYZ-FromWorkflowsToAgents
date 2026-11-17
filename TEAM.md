# Team

## Thông tin nhóm

- Tên nhóm: OXYZ
- Lớp: L3B
- Repo nhóm: `https://github.com/vtgiang213/K5-L3B-DAY08-OXYZ-FromWorkflowsToAgents`
- URL repo, nhánh nộp, commit chốt: 

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vương Trường Giang | 2A202603834      | 26ai.giangvt@vinuni.edu.vn      | vtgiang213        |   Workflow + Integration  |
|   2 | Đinh Quốc Việt | 2A202603885 | 26ai.vietdq3@vinuni.edu.vn | KemmVSAI | Single agent |

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
| Vương Trường Giang | Workflow + tích hợp | `0655071`, `a50e2b3`, `1b0bdae` | `test_workflow_crash_before_effect_then_retry` (`src/tests/test_team_workflow.py`) |
| Đinh Quốc Việt | Single agent | abff74b, a8da06e | `src/tests/test_single_shape.py` |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
