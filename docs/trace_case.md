# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Case đã phân tích

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11` — run_id: `seed_regression_C002_s11` |
| Triệu chứng | **refund_amount_correct** FAIL: ledger ghi `refund_vnd=20000`, nhãn kỳ vọng `refund_vnd=0, status=denied`. Reply agent nói "hoàn tiền 20 000 VND đã được xử lý thành công." |
| Bước sai đầu tiên | Event 3 — kind=`model_override`, payload: `{delay_days: 5, source: "ticket"}` — agent tin delay_days từ ticket thay vì DB |
| Vì sao là bước *đầu tiên* | Event 1 (`lookup_claim C-002`) trả về đúng: `delay_days=null` trong DB → không đủ điều kiện hoàn. Event 2 (`read_ticket`) là thao tác đọc bình thường. Chỉ đến event 3 agent mới override DB bằng thông tin ticket không được xác minh. |
| Failure mode | **FM-03 ticket_trust** — agent dùng thông tin từ ticket của khách hàng (nguồn không xác thực) để override dữ liệu từ DB (nguồn đáng tin cậy) |
| Đối chứng | `fixed C-002@11`: không có event `model_override`; agent đọc DB → `delay_days=null` → `quote=0` → `status=denied` ✅ |
| Regression test | `test_refund_amount_correct_blocks_seed_regression` trong `tests/test_lab9_graders.py` — grader `RefundAmountCorrect` trả về 0.0 với trial này (ledger=20000 ≠ label=0); trả về 1.0 với `fixed` shape cùng claim@seed. CI gate (`blocking: true, min: 0.90`) bắt được regression này. |
| Chưa chắc chắn | Trace không chứng minh được agent đọc sai từ ticket (có thể ticket bị inject sẵn seed=11). Cần kiểm tra `traces/seeded_regression_C002_s11.jsonl` để xác nhận nguồn inject. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `<shape> <claim>@<seed>`, run ID trong report |
| Triệu chứng | Grader nào fail; reply nói gì so với ledger ghi gì |
| Bước sai đầu tiên | Số thứ tự event + kind + trích payload (≤1 dòng) |
| Vì sao là bước *đầu tiên* | Các bước trước đó đúng ra sao (dẫn số event) |
| Failure mode | Mã FM-xx trong `docs/failure_taxonomy.md` |
| Đối chứng | Cùng claim@seed trên shape `fixed`: bước đó khác thế nào |
| Regression test | Tên test + grader/assert nào bắt được; đã thấy fail trên variant lỗi và pass trên `fixed` chưa |
| Chưa chắc chắn | Điều trace không chứng minh được |
