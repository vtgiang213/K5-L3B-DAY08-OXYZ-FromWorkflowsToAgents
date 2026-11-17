# Báo cáo cá nhân — 2A202603885_DinhQuocViet

## 1. Thông tin thành viên

- Họ tên: Đinh Quốc Việt
- MSSV: 2A202603885
- Email: 26ai.vietdq3@vinuni.edu.vn
- GitHub: KemmVSAI

## 2. Phần việc phụ trách

Shape B — Single agent: viết `run_claim` trong `src/lab8/shapes/single.py`, vòng ReAct tối đa 8 bước qua `lab8.runtime.run_react`; model chỉ được chọn tool đọc, code tính quote bằng `compute_compensation` và ghi hoàn tiền duy nhất qua `lab8.durability.issue_refund`.

## 3. Đóng góp cụ thể

- Cài vòng ReAct: `get_claim_view` → `lookup_order` → `compute_compensation` → `lookup_refund_history`, callback `decide` trả `final` và dừng trong cap 8 bước.
- Truyền quote đầy đủ vào `issue_refund`, không tự trừ trần theo đơn để host tự xử lý phần claim trước đã nhận (đúng T13, T14).
- Xử lý trọn các nhánh status: `needs_info`, `escalated`, `denied` khi quote 0, `denied` khi host từ chối (host tự ghi audit `policy_denied`), `failed` khi conflict số tiền hoặc claim không tồn tại.
- Truyền `crash_at` vào `issue_refund` và không bắt `InjectedCrash`, chỉ ghi trace rồi re-raise để crash suite chạy đúng.
- Trace theo contract v1: chỉ ghi field đã qua allowlist, không secret/PII, mọi nhánh return đều sinh file trace với đúng `run_id`.
- Gọi MockLLM đúng chuẩn: một lần `parse` từ ticket để lập kế hoạch, một lần `draft` câu trả lời cuối, đếm đầy đủ vào `Budget`.

## 4. Bằng chứng

- Bộ test shape single: `python -m pytest -q -m student -o addopts= -k "not workflow and not orchestrator and not swarm"` → 62 passed (T01–T14 × 5 seed, gồm T11 retry và T12 crash).
- Cổng host: `python -m pytest -q` → 54 passed.
- File chính: `src/lab8/shapes/single.py`.

## 5. Công cụ AI đã dùng

- Codex: đọc contract (`docs/business_rules.md`, `docs/contracts.md`), triển khai `single.py` và chạy test xác minh. Kết quả tự kiểm bằng 62 test student của shape single và 54 test cổng host, đều xanh.

## 6. Tự đánh giá

Phần single đã hoàn thành và pass đủ 62 test của shape, cổng host vẫn xanh. Phần còn lại của nhóm: workflow và orchestrator do người khác phụ trách, crash suite và benchmark do người 4 chạy trước khi nộp.
