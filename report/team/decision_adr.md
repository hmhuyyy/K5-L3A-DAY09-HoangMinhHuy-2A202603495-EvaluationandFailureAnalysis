# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: f382ad0
- Run id dẫn chứng: R-workflow-C-001-s11 (reports/benchmark.json)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000 (70 trial, reports/benchmark.json)
- Cost per success (mô phỏng, VND): 28.79 (reports/benchmark.json)
- Crash safety: 20/20 (reports/crash.json)
- Secret leak / approval bypass: 0 / 0 trên 280 trial public (4 shape × 14 claim × 5 seed, forbid_substrings pass toàn bộ)

## Vì sao shape này

Trên cùng 14 public claim × 5 seed × cùng MockLLM × cùng bảng giá, workflow đạt pass rate 1.000, pass⁵ 1.000, seed variance 0 — ngang bằng single và orchestrator nhưng rẻ nhất (28.79 VND/success so với 38.86, 47.79 và 49.57). Task hoàn phí này có luật nghiệp vụ đóng và nguồn sự thật có cấu trúc (cột `delay_days`, `damage_verified`, policy `is_current`), nên mọi phán đoán cần thiết đều dịch được thành code; phần duy nhất model làm tốt hơn (đọc ticket tự nhiên) lại là phần không được tin theo luật. Swarm tham chiếu fail đúng ở chỗ dự đoán: seed 55 tin "trễ 5 ngày" trong ticket của C-002 và trả 20.000 thay vì từ chối (pass 0.986, pass⁵ 0.929, variance 0.000816). Chọn kiến trúc ít tự chủ nhất mà vẫn làm được việc: workflow.

## Có đáng đổi lấy multi-agent không

Không, trên task này. Cả ba shape nhóm viết đều 1.000 — multi-agent không thêm độ chính xác nào, chỉ thêm 35–72% cost/success và thêm bề mặt lỗi (bước parse/peer của swarm chính là chỗ rò dữ liệu ticket vào quyết định). Điều kiện đảo lại quyết định: (1) khi xuất hiện claim mà workflow phải trả `needs_info`/`escalated` với tỷ lệ đáng kể nhưng một agent đọc ngữ cảnh rộng hơn vẫn xử được đúng (ticket mơ hồ thật sự, nhiều đơn trong một thread); (2) khi nguyên liệu quyết định không còn nằm trong world có cấu trúc (policy dạng văn bản dài phải diễn giải); (3) khi cần độ chính xác cao trên văn bản đối kháng mà verifier-by-code không kiểm nổi — khi đó orchestrator + verifier (xem `report/team/bonus_report.md`) là bước lên đầu tiên đáng tiền, chứ không phải swarm thuần.

## Trace và bằng chứng

Trace mỗi trial là một file JSON `traces/<run_id>.json` gồm các event: `shape`, `claim` (chỉ 4 field an toàn: found, claim_id, order_id, principal_id), `order`/`investigator` (view đã qua allowlist `ORDER_FIELDS`), `quote`, `refund`, `decision`/`crash` tùy nhánh; shape B thêm `step` và `policy_read`. Cố ý KHÔNG ghi: chữ ticket (dữ liệu người dùng, có thể chứa số liệu sai và ở bộ hidden có thể chứa canary), `parent_secret`, `raw_headers`, SĐT/địa chỉ/internal note/tên hàng — vì trace là một phần ranh giới bảo mật và grader quét toàn bộ file `<run_id>*`. Mọi file shape ghi ra đều nằm trong `traces/` đúng contract v1, nên scanner của grader phủ hết; không có output nào ra stdout ngoài kết quả trả về của CLI chuẩn.

## Giới hạn

MockLLM không phải model sản phẩm — cost là VND mô phỏng theo `config/pricing.yaml`, latency để `unavailable`. Số liệu trên là bộ public 14 claim × 5 seed; kết quả chính thức trên hidden 40 × 5 do grader chấm, nhưng logic của workflow là deterministic theo world có cấu trúc nên không phụ thuộc seed. Không sửa JSON trong `src/reports/`; mọi file do lệnh chuẩn của lab sinh ra.
