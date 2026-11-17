# Bonus report: B3

- Topic + nguồn: B3 — Verifier/aggregator chống khuếch đại lỗi. Google Research 2026, error amplification (slide 17 Evaluator–optimizer, 22 Reflection, 42). Agent độc lập khuếch đại lỗi tới 17,2×, orchestration tập trung còn 4,4×.
- CLAIM của nguồn: thêm bước kiểm chứng sau agent giảm mạnh mức khuếch đại lỗi so với agent không kiểm chứng.
- BOUNDARY (model / dataset / setup): kết quả đo trên benchmark của họ với model thật; LogiX-VN dùng MockLLM và một kiểu lỗi duy nhất (tin chữ ticket thay vì cột `delay_days`), nên ở đây chỉ kiểm chứng được *xu hướng*, không kiểm chứng được hệ số 17,2×/4,4×.
- HYPOTHESIS trên LogiX: thêm verifier bằng code trước khi ghi (đối chiếu `delay_days`, `status`, `damage_verified`, `shipping_fee_vnd`, `paid_vnd` với order có cấu trúc, quote lại từ dữ liệu cấu trúc) sẽ đưa swarm về pass rate/pass⁵/variance của workflow (1.000/1.000/0) với cost/success tăng nhẹ (dự kiến +20–30% do 2 tool call thêm).
- Biến cố định / biến thay đổi: cố định MockLLM, tool allowlist, 4 shape chính, seed `11,22,33,44,55`, evaluator `lab8.metrics`, bảng giá `config/pricing.yaml`. Thay đổi duy nhất: bước verifier (tắt = `swarm`, bật = `swarm_verified` đăng ký qua `--extra-shape`, cùng corpus).
- Lệnh tái lập (copy-paste được, chạy trong `src/`):

```text
python -m lab8.benchmark --shapes workflow,swarm,swarm_verified --extra-shape swarm_verified=bonus.swarm_verified:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/bonus_public.json
python -m lab8.benchmark --shapes workflow,swarm,swarm_verified --extra-shape swarm_verified=bonus.swarm_verified:run_claim --cases bonus/cases.jsonl --world bonus/world.json --seeds 11,22,33,44,55 --out reports/bonus_adversarial.json
python -m pytest -q tests/test_bonus_swarm_verified.py
```

- File report + run id: `reports/bonus_public.json`, `reports/bonus_adversarial.json`; run dẫn chứng `R-swarm_verified-C-002-s55` (verifier_override công khai) và `R-swarm_verified-CB-2-s55`.

## Kết quả

Corpus public (14 claim × 5 seed = 70 trial/shape):

| shape | pass | pass⁵ | variance | cost/success (VND mô phỏng) |
| --- | --- | --- | --- | --- |
| workflow | 1.000 | 1.000 | 0.000000 | 28.79 |
| swarm | 0.986 | 0.929 | 0.000816 | 49.57 |
| swarm_verified | 1.000 | 1.000 | 0.000000 | 62.00 |

Corpus đối kháng tự viết (`bonus/cases.jsonl`, 11 claim × 5 seed = 55 trial/shape, nhãn viết tay theo luật README — nói quá delay, nhiều con số trong một câu, cộng dồn sai, hỏng hàng chưa verify, đã hoàn rồi, approval của claim khác, approval thấp hơn quote, principal lẫn, thiếu order_id):

| shape | pass | pass⁵ | variance | cost/success (VND mô phỏng) |
| --- | --- | --- | --- | --- |
| workflow | 1.000 | 1.000 | 0.000000 | 30.02 |
| swarm | 0.945 | 0.727 | 0.011901 | 55.09 |
| swarm_verified | 1.000 | 1.000 | 0.000000 | 64.08 |

Số lần verifier can thiệp (đếm từ trace): public 1/46 lần ghi sắp xảy ra (`verifier_override` tại C-002 seed 55, 45 lần `verifier_ok`); đối kháng 3/33 (CB-2, CB-3, CB-10 đều seed 55, 30 lần `verifier_ok`). Verifier chỉ chạy khi proposal > 0: denied không ghi gì nên không có gì để khuếch đại. Test: `tests/test_bonus_swarm_verified.py` (58 test xanh, gồm ma trận 11 claim × 5 seed và cặp đối chứng C-002 seed 55: swarm fail, swarm_verified pass kèm event `verifier_override`).

## Kết luận

Ủng hộ hypothesis về xu hướng: một bước verify bằng code trước khi ghi xóa sạch 3 trial fail của swarm (pass 0.945 → 1.000, pass⁵ 0.727 → 1.000, variance 0.0119 → 0) với tổng chi phí tăng ~16% trên corpus đối kháng (55.09 → 64.08 VND/success). Nhưng verifier không biến swarm thành lựa chọn tốt hơn workflow: workflow vẫn chính xác 1.000 với chi phí thấp hơn một nửa (30.02). Giá trị còn lại của swarm sau khi có verifier chỉ là cấu trúc giao việc (investigator, handoff) — còn *kết quả* thì do verifier quyết, đúng câu hỏi của topic. Điều kiện đảo ngược kết luận: khi tác vụ có phần việc thật sự cần nghị lực của model (ticket mơ hồ phải hỏi lại, phân loại phức tạp) mà workflow không cover được, hoặc khi fact không có trong world có cấu trúc khiến verifier-by-code không kiểm nổi — lúc đó "model kiểm lại model" (aggregator kiểu evaluator–optimizer) mới có chỗ đứng, với giá là thêm lần gọi model.

## Giới hạn

MockLLM chỉ mô phỏng LLM có seed; "lỗi" của swarm là khối `REFERENCE_WEAKNESS` cố ý, không phải hành vi model thật. Corpus đối kháng 11 claim là nhỏ, nhãn do nhóm viết tay theo luật (không sinh bằng code đang test). Cost là VND mô phỏng từ `config/pricing.yaml`, latency `unavailable`. Không thể suy ra hệ số 17,2×/4,4× của nguồn.
