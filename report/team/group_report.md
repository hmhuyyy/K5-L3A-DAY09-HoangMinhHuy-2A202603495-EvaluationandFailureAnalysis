# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: Vibeforlife (L3A)
- Thành viên: xem `TEAM.md` (4 người: workflow+integration, single, orchestrator+handoff, eval/report+bonus)
- Commit chốt (trùng `report/team/decision_adr.md`): f382ad0

## 2. Mục tiêu và cách tiếp cận

Bài toán: cùng một claims flow hoàn phí vận chuyển chạy trên bốn kiến trúc (A workflow, B single ReAct, C orchestrator, D swarm tham chiếu), đo trên cùng claim × cùng seed × cùng bảng giá mô phỏng, rồi chọn kiến trúc **ít tự chủ nhất mà vẫn làm được việc**.

Nhóm làm theo 5 checkpoint: CP1 cài đặt và thống nhất contract, CP2 viết 3 shape song song (mỗi người một file, cùng chữ ký `run_claim`), CP3 crash/handoff, CP4 must-pass và crash suite, CP5 benchmark + quyết định kiến trúc. Cả ba shape dùng chung 5 quy ước: (1) đọc claim qua `get_claim_view`, không bao giờ `SELECT *`; (2) `delay_days` chỉ lấy từ order row, không từ ticket; (3) truyền **quote đầy đủ** vào `durability.issue_refund` — host tự trừ trần theo đơn và cap theo approval/paid; (4) `crash_at` xuyên qua tới `issue_refund`, `InjectedCrash` được ghi trace rồi ném tiếp; (5) trace chỉ chứa field đã qua allowlist.

## 3. Giải pháp

| Shape | Đường đi | Model call | Tool call | Điểm khác biệt |
| --- | --- | --- | --- | --- |
| A `workflow` | claim → lookup_order → compute_compensation → issue_refund | 1 (draft) | 3 | Không đọc ticket để ra quyết định; mọi nhánh return qua `finish()` |
| B `single` | get_claim_view → ReAct 4 bước (lookup_order → lookup_policy → compute_compensation → final) → issue_refund | 5 (4 reason + 1 draft) | 4 | Mỗi bước ReAct một lần model; memo giữ order giữa các bước; cap 8 bước |
| C `orchestrator` | get_claim_view → make_handoff → run_readonly_investigators → issue_refund | 2 (plan + draft) | 5 | Investigator chỉ nhận handoff.v1 với 3 tool đọc; orchestrator là người ghi duy nhất |
| D `swarm` | tham chiếu, không sửa | 3 (peer + parse + draft) | 5 | Giữ nguyên `REFERENCE_WEAKNESS` seed 55 để đo variance |

Ranh giới code/model: tiền do `compute_compensation` tính, approval do host kiểm, ghi ledger chỉ nằm trong `durability.issue_refund`; model chỉ soạn câu chữ. Handoff `handoff.v1` tạo bằng `make_handoff` với `facts={}` — investigator tự đọc qua tool có scope theo principal, không có dữ liệu nào copy qua ranh giới; trace ghi bản handoff **sau khi** sanitize. Trace mỗi trial gồm các event `shape → claim → order/handoff → quote → refund` (kèm `decision`/`crash` ở nhánh tương ứng), không bao giờ chứa chữ ticket, secret, SĐT, địa chỉ, internal note hay tên hàng.

## 4. Kết quả

Từ `src/reports/benchmark.json` (4 shape × 14 public claim × 5 seed, mỗi trial một SQLite mới):

| shape | pass rate | pass⁵ | seed min–max | variance | cost/success (VND mô phỏng) |
| --- | --- | --- | --- | --- | --- |
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 28.79 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 38.86 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 47.79 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 |

Crash safety `20/20` (`src/reports/crash.json`). Ma trận student T01–T14 × 4 shape × 5 seed: 248/248 pass. Không có secret/PII leak hay approval bypass trên 280 trial public.

Tự kiểm trên bộ hidden `student_drop/` (40 claim × 5 seed, không nhãn, CP5): cả 3 shape chạy đủ 600 trial, `error` = 0, `leak_suspect` = 0, trace contract pass toàn bộ (xem `reports/hidden_selfcheck.json`). Ba kiến trúc độc lập cho phân bố kết quả giống hệt nhau (95 denied / 90 resolved / 5 needs_info / 10 escalated trên 200 trial mỗi shape) — đồng thuận 100% từng trial. Đối chiếu với swarm tham chiếu: lệch đúng 6 trial, tất cả ở seed 55 (5 lần trả tiền vì tin số ngày trong ticket, 1 lần từ chối vì ticket nói thiếu ngày) — khớp đúng điểm yếu cố ý đã ghi trong README và ước lượng pass 0.97 / pass⁵ 0.85 của giảng viên cho swarm. Kết quả chính thức do grader chấm.

Quyết định: chọn **workflow** — pass 1.000 như hai shape còn lại nhưng rẻ nhất (28,79 VND/success) và variance 0; task có luật đóng và nguồn sự thật có cấu trúc nên không cần model ra quyết định. Chi tiết và điều kiện đảo ngược: `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation 4-shape (R4): `report/team/research_card.md`. Bonus B3 (verifier bằng code trước khi ghi, kéo swarm từ 0.945 → 1.000 trên bộ 11 claim đối kháng tự viết): `report/team/bonus_report.md`.

## 5. Khó khăn và cách xử lý

- **Test ban đầu đếm sai refund lịch sử.** Test đếm `COUNT(*) FROM refund_ledger` kỳ vọng 0 nhưng world seed sẵn 2 dòng hoàn tiền cũ (O-505, O-515) để thử trần theo đơn. Sửa: chỉ đếm dòng của claim đang chạy — đúng cách grader dùng `unexpected_ledger_rows`.
- **Giữ cổng xanh khi tích hợp.** Nhiều file đổi cùng lúc dễ làm đỏ cổng host; nhóm trưởng merge theo từng phần và chạy `python -m pytest -q` sau mỗi merge.
- **Windows kẹt file `.sqlite`.** Connection chưa đóng làm benchmark không dọn được thư mục tạm; mọi shape mở `connect()` đều đóng trong `finally:` (đúng cảnh báo trong README). PowerShell chặn script activate → `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- **Hai bản starter khác cấu trúc.** Bản nhóm bắt đầu nằm ngoài `src/`, bản chấm cuối dùng `src/`; nhóm port toàn bộ bài sang cấu trúc mới, diff từng module lõi (`durability`, `policy`, `tools`, `handoff`, `runtime`) xác nhận giống hệt nên kết quả không đổi.

## 6. Tổng hợp đóng góp

Chi tiết từng người: bảng `## Bảng đóng góp` trong `TEAM.md` và báo cáo cá nhân `report/team/2A202603384_HoangBaoNguyen.md`, `report/team/2A202603469_BuiQuangHuy.md` (thành viên 2 và 4 bổ sung trước deadline). Mỗi shape một test riêng: `tests/test_workflow_member.py`, `tests/test_single_member.py`, `tests/test_orchestrator_member.py`; bonus có `tests/test_bonus_swarm_verified.py`.
