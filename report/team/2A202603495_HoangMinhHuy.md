# Báo cáo cá nhân — 2A202603495_HoangMinhHuy

## 1. Thông tin thành viên

- Họ tên: Hoàng Minh Huy
- MSSV: 2A202603495
- Email: minhhuy108205@gmail.com
- GitHub: Stormaka

## 2. Phần việc phụ trách

Shape B – Single Agent (ReAct). File chính: `src/lab8/shapes/single.py`.

Phạm vi: triển khai vòng ReAct đúng quy chuẩn, bảo đảm agent không bao giờ gọi được write tool, host là writer duy nhất, không tin ticket text, truyền `crash_at` đúng, không nuốt `InjectedCrash`, giữ idempotency.

## 3. Đóng góp cụ thể

- Viết `run_claim` và `_run` trong `single.py`: mở store, đọc claim qua `get_claim_view` (chỉ 4 cột an toàn), xây `decide()` closure với 3 nhánh (initial → lookup_order → compute_compensation → final).
- `decide()` gọi MockLLM `purpose="reason"` ở mỗi bước để cost công bằng; sau vòng lặp gọi thêm `purpose="draft"` khi approved.
- `memo` lưu order giữa bước vì `run_react` chỉ giữ `{last_tool, last_result, claim}`.
- Host path: khi agent trả `approved`, gọi `durability.issue_refund(conn, claim_id, proposal_amount, crash_at=crash_at)`; `InjectedCrash` flush trace rồi raise lại, không nuốt.
- Không sửa `workflow.py`, `orchestrator.py`, `swarm_reference.py` hay bất kỳ test nào.

## 4. Bằng chứng

- Run id dẫn chứng: `R-single-C-001-s11`
- Lệnh test: `python -m pytest -q -m student -o addopts= -k "single and not workflow and not orchestrator"` → **122 passed**
- Lệnh crash: `python -m lab8.crash_test --count 20 --out reports/crash.json` → **crash_safety 20/20**
- Lệnh CLI: `python -m lab8.run --shape single --claim-id C-001 --seed 11 --db data/run.sqlite` → `status: resolved`, `proposal_amount: 35000`, `committed_audit_count: 1`
- Benchmark: `src/reports/benchmark.json` → single: pass_rate 1.000, pass^5 1.000, seed_min 1.000, seed_max 1.000, variance 0.000000, cost_per_success 31.31 VND, mean_steps 2.64
- Trace contract: `traces/R-single-C-001-s11.json` ghi events `[claim_view, react_final, issue_refund]`, không chứa CANARY_SECRET hay PII.

## 5. Công cụ AI đã dùng

- Claude Code (Sonnet 5.5) để: đọc code base, hiểu API của `run_react`/`dispatch`/`issue_refund`, viết `single.py`, chạy test và benchmark, điền các file báo cáo `decision_adr.md` / `research_card.md` / `TEAM.md` / báo cáo cá nhân này.
- Tự kiểm tra kết quả: chạy thật `pytest`, `lab8.run`, `lab8.benchmark`, `lab8.crash_test`, `lab8.check_submission`; đọc output JSON và so khớp số liệu trong báo cáo với số liệu trong file `src/reports/*.json` (không chép tay từ terminal). Không tự tạo kết quả test. Xem [RULES.md](../../RULES.md).

## 6. Tự đánh giá

- Đã hoàn thành toàn bộ phần Shape B; 122 test single xanh, không phá swarm (62 xanh), không sửa code ngoài phạm vi.
- Còn chờ: workflow và orchestrator do thành viên khác implement (hiện vẫn là stub). Repository chưa init git nên `Commit hash` trong `decision_adr.md` chưa điền được — sẽ điền sau khi commit thực tế.
- Còn chờ: email cá nhân — không phải AI điền được.
