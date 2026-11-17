# Team

## Thông tin nhóm

- Tên nhóm: OXYZ
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY08-OXYZ-FromWorkflowsToAgents`
- URL repo, nhánh nộp, commit chốt: `https://github.com/vtgiang213/K5-L3B-DAY08-OXYZ-FromWorkflowsToAgents`, nhánh `main`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vương Trường Giang | 2A202603834      | 26ai.giangvt@vinuni.edu.vn      | vtgiang213        |   Workflow + Integration  |
|   2 | Đinh Quốc Việt | 2A202603885 | 26ai.vietdq3@vinuni.edu.vn | KemmVSAI | Single agent |
|   3 | Vũ Quang Hải | 2A202603935 | haivq25@gmail.com | HaiVuQ | An toàn ledger + đánh giá |
|   4 | Lê Sỹ Long Nhật | 2A202603881 | 26ai.nhatlsl@vinuni.edu.vn | longnhat2kruoi | Orchestrator + handoff |

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Đinh Quốc Việt (`KemmVSAI`) | Single agent | `abff74b`, `dff1807` | `src/tests/test_team_shapes.py` |
| Vũ Quang Hải (`HaiVuQ`) | An toàn ledger + đánh giá | `61752ba` | `src/tests/test_team_shapes.py` |
| Vương Trường Giang | Workflow + tích hợp | `0655071`, `a50e2b3`, `1b0bdae` | `test_workflow_crash_before_effect_then_retry` (`src/tests/test_team_workflow.py`) |
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
