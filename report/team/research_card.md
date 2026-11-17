# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R3 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | AgentArch: A Comprehensive Benchmark to Evaluate Agent Architectures in Enterprise, AACL 2026, https://arxiv.org/abs/2509.10769, benchmark |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Với các tác vụ có quy trình nghiệp vụ xác định, việc tăng mức tự chủ hoặc phức tạp topology làm tăng chi phí và số bước mà không chắc cải thiện độ chính xác so với workflow kiểm soát chặt. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Giới hạn trong setup mô phỏng của lab: `MockLLM`, 14 claim public (`data/public_claims.jsonl`), 5 seed cố định (`11,22,33,44,55`), giá mô phỏng trong `config/pricing.yaml`. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Khi giữ nguyên `MockLLM`, tool manifest, corpus và bảng giá, việc chuyển topology từ `workflow` → `single` → `orchestrator` → `swarm` sẽ làm `cost/success` tăng dần (khoảng +25% đến +80%) và `mean_steps` tăng, trong khi `pass_rate` không tăng thêm (thậm chí `swarm` có thể giảm nhẹ nếu tin dữ liệu ticket). |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Biến giữ cố định: `MockLLM`, `tools.manifest.v1.1.yaml`, `seeds=[11,22,33,44,55]`, `data/public_claims.jsonl`, `config/pricing.yaml`, `lab8.metrics`. Biến duy nhất thay đổi: topology (`workflow`, `single`, `orchestrator`, `swarm`). |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: `swarm` fail T02 ở seed 55 (`status resolved != denied`) do tin số ngày trễ trong ticket; đo bằng `pass_rate`, `pass^5`, `seed_variance`, `cost_per_success_vnd`, `mean_steps`. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `src/reports/benchmark.json` (ví dụ trial `R-workflow-C-001-s11`, `R-single-C-001-s11`, `R-orchestrator-C-001-s11`, `R-swarm-C-002-s55`)
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: **Đúng một phần.** `workflow` đạt `pass_rate = 1.000`, `pass^5 = 1.000`, `var = 0.000000`, `cost/success = 27.86 VND`, `steps = 1.86`. `single` giữ `pass_rate = 1.000`, với `cost/success = 35.67 VND` (+28.0% so với workflow) và `steps = 5.36`. `orchestrator` giữ `pass_rate = 1.000`, với `cost/success = 47.36 VND` (+70.0%) và `steps = 4.71`. `swarm` đạt `pass_rate = 0.986`, `pass^5 = 0.929`, `var = 0.000816`, `cost/success = 49.57 VND` (+77.9%) và `steps = 2.80`; swarm fail 1 trial T02 ở seed 55 (`status resolved != denied`). Chi phí tăng theo thứ tự giả thuyết, nhưng số bước không tăng dần: từ single sang orchestrator và swarm, `mean_steps` giảm.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
