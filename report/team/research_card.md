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
| CÂU | R1 / R2 / R3 / R4 | R4 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* (slide 44, 59); benchmark paper, bằng chứng dạng benchmark |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | "Hiệu năng MAS" trong nhiều benchmark có thể đến từ cách thiết kế benchmark chứ không phải kiến trúc; phải so với single-agent và baseline đơn giản trong khi cố định runtime, model và tool |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Kết luận trong phạm vi các benchmark MAS được khảo sát; không phát biểu cho production hay task ngoài benchmark |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Cố định model/tool/seed/corpus/evaluator và chỉ đổi topology: workflow, single, orchestrator đều đạt pass 1.000; swarm fail đúng 1 trial (C-002 seed 55) → pass 0.986, pass⁵ 0.929, variance ≠ 0; cost/success tăng dần workflow (≈29) < single (≈39) < orchestrator (≈48) < swarm (≈50) VND mô phỏng |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Cố định: MockLLM seeded, cùng tool allowlist, seed 11/22/33/44/55, cùng 14 public claim, `config/pricing.yaml`, `lab8.metrics`, mỗi trial một SQLite mới (`fresh_sqlite_per_trial`). Thay đổi duy nhất: topology shape (A workflow → B single → C orchestrator → D swarm) |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass⁵, variance, cost/success, leak, bypass | Lỗi dự kiến: swarm tin số ngày trong ticket ở seed chia hết cho 5 (C-002: trả 20.000 thay vì denied). Đo bằng pass rate 0.986, pass⁵ 0.929, seed variance 0.000816, min 0.929 / max 1.000 (so với 1.000/1.000/0 của 3 shape còn lại); leak đo bằng forbid_substrings = 0; bypass đo bằng approval_ok=false mà có refund = 0 |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn, chạy trong `src/`):

```text
python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
```

- Run id / file report: `reports/benchmark.json`; run dẫn chứng `R-swarm-C-002-s55` (trial fail duy nhất của swarm) và `R-workflow-C-002-s55` (cùng trial, đúng).
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: **đúng**. pass rate: workflow/single/orchestrator 1.000, swarm 0.986; pass⁵: 1.000 / 1.000 / 1.000 / 0.929; seed variance: 0 / 0 / 0 / 0.000816 (min 0.929, max 1.000); cost/success: 28.79 / 38.86 / 47.79 / 49.57 VND mô phỏng — đúng thứ tự và đúng magnitudes dự đoán. Chênh lệch duy nhất về accuracy nằm đúng ở topology tin dữ liệu tự nhiên (swarm) — mọi biến khác cố định, nên chênh lệch quy được về topology chứ không phải prompt/tool/seed.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`, corpus public chỉ 14 claim (70 trial/shape) nên khác biệt 0.014 về pass rate chỉ là 1 trial — không đủ sức thống kê để khái quát ngoài corpus này.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem `docs/bonus_topics.md`. Nhóm chọn B3 (verifier/aggregator): kết quả ở `report/team/bonus_report.md`, đúng tinh thần R4 — bật/tắt đúng một thành phần (verifier) trên cùng mọi biến còn lại.
