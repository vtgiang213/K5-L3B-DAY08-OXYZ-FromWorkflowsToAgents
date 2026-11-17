# Báo cáo cá nhân — 2A202603834_VuongTruongGiang

## 1. Thông tin thành viên

- Họ tên: Vương Trường Giang
- MSSV: 2A202603834
- Email: 26ai.giangvt@vinuni.edu.vn
- GitHub: vtgiang213

## 2. Phần việc phụ trách

- Phụ trách shape A (`workflow.py`): xây dựng quy trình xử lý claim theo các bước cố định.
- Phụ trách tích hợp code của nhóm, xử lý xung đột, kiểm tra toàn bộ bài, hoàn thiện `TEAM.md` và checklist nộp bài.

## 3. Đóng góp cụ thể

- Triển khai đọc claim, kiểm tra đơn và tính tiền hoàn từ dữ liệu order; trả kết quả theo từng trường hợp nghiệp vụ.
- Gọi `issue_refund` với quote đầy đủ và truyền `crash_at` để host xử lý approval, chống ghi trùng và kiểm tra crash.
- Dùng `Trace` và `finish()` để ghi trace và tạo kết quả; chỉnh lại thông tin lỗi ở các nhánh xử lý.
- Cập nhật branch cá nhân theo `main`
- Thêm test `test_workflow_crash_before_effect_then_retry` để kiểm tra workflow crash trước khi ghi refund, sau đó chạy lại chỉ tạo một refund và một audit `refund_committed`.

## 4. Bằng chứng

- Commit trên branch hiện tại: `0655071` (triển khai workflow), `a50e2b3` (chỉnh thông tin lỗi).
- Code: `src/lab8/shapes/workflow.py`; test mới: `src/tests/test_team_workflow.py`. Test `test_workflow_crash_before_effect_then_retry` đã chạy pass; cần bổ sung hash commit sau khi commit.
- Trước khi thêm test mới, nhóm đã chạy test host: 54 passed; test student: 248 passed; crash suite: 20/20.

## 5. Công cụ AI đã dùng

- Dùng Codex để giải thích yêu cầu, gợi ý code workflow, viết test crash, đọc lỗi pytest và hỗ trợ xử lý xung đột Git.
## 6. Tự đánh giá

- Đã thực hiện phần workflow và bước đầu xử lý tích hợp.
