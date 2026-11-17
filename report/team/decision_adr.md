# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 61752ba
- Run id dẫn chứng: R-workflow-C-001-s11
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000-1.000 / 0.000000
- Cost per success (mô phỏng, VND): 27.86
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0 (public benchmark & test_team_shapes.py)

## Vì sao shape này

Trên cùng bộ 14 claim public (`data/public_claims.jsonl`) và 5 seed (`11, 22, 33, 44, 55`, tổng 70 trial mỗi shape), cả ba shape `workflow`, `single`, và `orchestrator` đều đạt `pass_rate = 1.000`, `pass^5 = 1.000`, và `seed_variance = 0.000000`. Trong đó `workflow` đạt chi phí mô phỏng thấp nhất (`27.86 VND/success`, trung bình `1.86` bước và `0` lần gọi model) so với `single` (`35.67 VND/success`, `5.36` bước) và `orchestrator` (`47.36 VND/success`, `4.71` bước), đồng thời tuân thủ nguyên tắc chọn kiến trúc ít tự chủ nhất mà vẫn hoàn thành đúng luật nghiệp vụ và ranh giới host.

## Có đáng đổi lấy multi-agent không

Không đáng trong bài toán này: `swarm` vừa có `pass_rate` thấp hơn (`0.986`, `pass^5 = 0.929`, `seed_variance = 0.000816`, fail T02 ở seed 55 do tin số ngày trễ trong ticket), vừa có chi phí cao nhất (`49.57 VND/success`). `orchestrator` đạt `1.000` nhưng tốn chi phí gần gấp đôi `workflow` (`47.36` vs `27.86 VND`). Quyết định chỉ đảo lại khi tác vụ có nhiều nhánh điều tra không cố định trước được hoặc cần tách quyền đọc dữ liệu nhạy cảm giữa nhiều nguồn độc lập mà luồng tuần tự cố định không biểu diễn được.

## Trace và bằng chứng

Trace ghi các event tối thiểu qua `lab8.trace.Trace`: `quote`, `decision`, `error` (và ở `single`/`orchestrator` có thêm `claim_view`, `parse`, `tool`, `handoff`, `investigator`, `crash`). Nhóm cố ý **không** ghi dòng claim thô (`parent_secret`), dòng order thô (`phone`, `address`, `item_name`, `internal_note`), hay context chưa qua allowlist. Đội security kiểm chứng bằng `artifact_blob` (quét `trace_path` và mọi file `<run_id>*` cùng thư mục) và test tự động trong `src/tests/test_team_shapes.py` để đảm bảo không có `CANARY_SECRET_*` hay `internal_note` xuất hiện.

## Giới hạn

MockLLM không phải model sản xuất. Latency để `unavailable`. Không sửa JSON cho đủ 0.75.
