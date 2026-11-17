# Báo cáo cá nhân — 2A202603881_LeSyLongNhat

## 1. Thông tin thành viên

- Họ tên: Lê Sỹ Long Nhật
- MSSV: 2A202603881
- Email: 26ai.nhatlsl@vinuni.edu.vn
- GitHub: longnhat2kruoi

## 2. Phần việc phụ trách

Shape C — Orchestrator + handoff: viết `run_claim` trong `src/lab8/shapes/orchestrator.py`. Orchestrator tạo handoff với allowlist chỉ tool đọc, chạy investigator qua `lab8.runtime.run_readonly_investigators`, rồi tự gọi `lab8.durability.issue_refund` để ghi hoàn tiền. Investigator không có registry ghi.

## 3. Đóng góp cụ thể

- Tạo handoff qua `lab8.handoff.make_handoff` với `allowed_tools = ["lookup_order", "lookup_policy", "compute_compensation"]`; facts rỗng, không đưa `parent_secret`, raw header hay claim row đầy đủ vào handoff — dùng allowlist, không dùng tóm tắt LLM làm sanitizer.
- Orchestrator đọc kết quả investigator từ `lookup_order` và quote từ `compute_compensation`, truyền giá quote đầy đủ vào `issue_refund` để host tự trừ refund trước trên cùng đơn.
- Xử lý trọn các nhánh trả kết quả: `needs_info` khi thiếu `order_id`, `escalated` khi `lookup_order` không thấy đơn, `denied` khi quote ≤ 0 hoặc host từ chối, `failed` khi conflict; `unknown_claim` trả `failed` từ nhánh sớm.
- Truyền `crash_at` vào `issue_refund`, không bắt `InjectedCrash` — chỉ ghi trace rồi re-raise để crash suite chạy đúng.
- Trace theo contract v1: ghi handoff đã sanitize qua `safe_dump`, không secret/PII, mọi nhánh return đều sinh file trace với đúng `run_id` qua `lab8.trace.Trace`.
- Gọi MockLLM với `purpose="draft"` ở các nhánh quyết định, đếm đầy đủ vào `Budget`.

## 4. Bằng chứng

- Commit `d64c2c3` — Implement Orchestrator Shape (PR #2), file chính: `src/lab8/shapes/orchestrator.py`.
- Trace mẫu của shape orchestrator: file JSON do `lab8.trace.Trace` ghi trong run, chứa event `handoff`, `investigator`, `quote`, `decision` với đúng `run_id`.

## 5. Công cụ AI đã dùng

- Claude Code: đọc contract (`docs/contracts.md`, `docs/business_rules.md`), triển khai `orchestrator.py` theo khung shape. Kết quả tự kiểm bằng cách chạy bộ test shape và crash suite của nhóm trên các seed công khai; kết quả test tổng hợp ở báo cáo nhóm (người 4 phụ trách).

## 6. Tự đánh giá

Phần orchestrator đã hoàn thành: handoff chỉ mở tool đọc, refund đi qua host duy nhất một lần, trace không lộ secret/PII và mọi nhánh return đều sinh trace hợp lệ. Test riêng cho shape orchestrator chưa viết; cần bổ sung cùng người 4 trước khi chạy benchmark chốt bài.
