# Báo cáo cá nhân — 2A202603384_HoangBaoNguyen

## 1. Thông tin thành viên

- Họ tên: Hoàng Bảo Nguyên
- MSSV: 2A202603384
- Email: (tự điền email trường)
- GitHub: Stormaka

## 2. Phần việc phụ trách

Nhóm trưởng. Theo phân công nhóm 4 người (gợi ý trong `TEAM.md`: workflow + integration), tôi phụ trách:

- **Shape A `workflow`** (`src/lab8/shapes/workflow.py`): toàn bộ quy trình cố định 7 bước — đọc claim qua `get_claim_view`, trả `needs_info` khi thiếu `order_id`, `escalated` khi không nhìn thấy đơn, quote bằng `compute_compensation` từ order row (bỏ qua số ngày trong ticket), `denied` không ghi ledger khi quote = 0, và `durability.issue_refund` với **quote đầy đủ** khi quote > 0.
- **Integration**: giữ cổng `python -m pytest -q` xanh sau mỗi lần merge phần của 3 thành viên còn lại; giải conflict; trình tự nộp bài (commit → `git rev-parse --short HEAD` → ghi hash vào ADR → commit lại → `check_submission` 0 FAIL).
- **Quyết định kiến trúc** (`report/team/decision_adr.md`): chọn `workflow` dựa trên số liệu benchmark.

## 3. Đóng góp cụ thể

- `src/lab8/shapes/workflow.py`: shape deterministic, 1 model call (chỉ draft câu trả lời), 3 tool call; mọi nhánh trả về đều có trace đúng contract v1; `crash_at` xuyên qua tới `issue_refund` và `InjectedCrash` được ném tiếp (T12).
- Quyết định kỹ thuật chính:
  - Truyền **quote đầy đủ** vào `issue_refund`, không tự trừ phần đơn đã hoàn — host trừ theo trần từng đơn; tự trừ trước sẽ bị trừ hai lần và sai T13/T14.
  - Trace chỉ ghi field đã qua allowlist (claim: 4 field an toàn; order: `ORDER_FIELDS`), không bao giờ ghi chữ ticket hay bất kỳ field nhạy cảm nào.
  - Các nhánh `needs_info`/`escalated`/`denied` khi quote = 0 **không** gọi `issue_refund`, để không sinh audit `policy_denied` sai nhãn.
- `report/team/decision_adr.md`: điền đủ các dòng máy đọc được (`- Shape chọn: workflow`, số liệu, hash) và 4 phần tự luận.

## 4. Bằng chứng

- Test phần tôi phụ trách: `python -m pytest -q -m student -o addopts= -k workflow` → **62 passed** (T01–T14 × 5 seed trên shape workflow), chạy trên repo nhóm.
- Run id dẫn chứng: `R-workflow-C-001-s11`; số liệu trong `reports/benchmark.json` của repo nhóm: workflow pass 1.000, pass⁵ 1.000, variance 0, cost/success 28.79 VND mô phỏng.
- Crash: T12 trên workflow (`--crash-at after_effect_before_checkpoint`) crash thật, resume xong đúng 1 dòng ledger + 1 audit `refund_committed`.
- Commit phần tôi trong repo nhóm: xem bảng đóng góp `TEAM.md` / `contributions` của repo nhóm; nhánh cá nhân này chứa đúng 2 artifact tôi tác giả: `src/lab8/shapes/workflow.py` và `report/team/decision_adr.md`.

## 5. Công cụ AI đã dùng

- Dùng trợ lý AI (ZCode — agent lập trình) để: soạn khung code cho `workflow.py` theo contract đã đọc, soạn ADR từ số liệu benchmark đã sinh bằng lệnh chuẩn của lab, và kiểm tra lại hiểu biết về các bẫy nghiệp vụ (trần theo đơn, approval đúng claim, trace contract).
- Cách tự kiểm tra: tôi đọc lại từng dòng `workflow.py` và đối chiếu với output contract trong README; tự chạy `pytest -q -m student -o addopts= -k workflow` (62 xanh), tự chạy lại T13/T14 bằng `python -m lab8.run` và mở file trace trong `traces/` để xác nhận không có field nhạy cảm; mọi số liệu trong ADR lấy nguyên từ `reports/benchmark.json` do `lab8.benchmark` sinh ra, không có con số nào do AI hoặc tôi tự bịa.

## 6. Tự đánh giá

Phần workflow là phần tôi hiểu sâu nhất trong repo: giải thích được vì sao chọn workflow (pass 1.000, rẻ nhất, variance 0), vì sao truyền quote đầy đủ, và vì sao trace cố ý không ghi chữ ticket. Điểm cần cải thiện: phần integration tôi nên chủ động giải conflict sớm hơn thay vì gom một commit lớn. Nếu giảng viên hỏi, tôi có thể trình bày 2 phút về quyết định ADR kèm số liệu so sánh 4 shape.
