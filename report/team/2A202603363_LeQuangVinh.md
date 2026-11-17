# Báo cáo cá nhân — Lê Quang Vinh

## 1. Thông tin thành viên

- Họ tên: Lê Quang Vinh
- MSSV: 2A202603363
- Email: 26ai.vinhlq2@vinuni.edu.vn
- GitHub: lequangvinh21

## 2. Phần việc phụ trách

QA, đo đạc và chứng từ: chạy crash suite và benchmark tái lập, kiểm tra tính nhất quán giữa số liệu trong `report/team/decision_adr.md` và file report do công cụ sinh ra, rà soát test của các shape thành viên khác, và sở hữu test tính toàn vẹn chứng từ `src/tests/test_eval_integrity.py`. Theo phân công nhóm, bonus B3 do nhóm thực hiện trên `main`; tôi làm thêm một biến thể B3 độc lập chạy cục bộ để đối chiếu chéo (mục 3).

## 3. Đóng góp cụ thể

- Viết `src/tests/test_eval_integrity.py` (4 test): lưới `reports/benchmark.json` đúng contract (4 shape × seed 11–55 × ≥ 10 claim, không trial chưa chấm); `reports/crash.json` là 20/20 và mọi scenario pass; **mọi con số ADR trích dẫn cho shape chọn lấy lại được từ benchmark.json** (pass rate, pass⁵, seed min–max, variance, cost/success — chống số gõ tay, phục vụ C6/C7); hai file bonus đủ 3 biến thể (workflow, swarm, swarm_verified).
- Chạy và tái lập các chứng từ chuẩn của nhóm: `lab8.crash_test` (20/20), `lab8.benchmark` 4 shape — kết quả identical từng trial với file đã commit.
- Kiểm chứng độc lập nhánh Orchestrator `BuiQuangHuy-2A202603469` trong worktree tạm: 62 student test + 3 test handoff secret + 54 test host đều pass; không sửa code của người phụ trách shape đó.
- Biến thể B3 độc lập (chạy cục bộ, corpus đối kháng tự viết khác corpus của nhóm): verifier đối chiếu fact với order có cấu trúc như bản của nhóm nhưng tính cost khác; kết quả cùng khớp kết luận — verifier đưa swarm về pass 1.000 / pass⁵ 1.000 / variance 0, với cost/success gần như không đổi (48.86–48.89 VND mô phỏng so với 49.57 của swarm). Đây là nhân rộng (replication) kết luận B3 trên một corpus khác; file benchmark của lần chạy này được tôi push kèm nhánh cá nhân nếu cần đối chiếu.

## 4. Bằng chứng

Các lệnh dưới đây chạy từ `src/`:

| Lệnh | Kết quả |
| --- | --- |
| `python -m pytest -q tests/test_eval_integrity.py` | 4 passed |
| `python -m pytest -q` | 126 passed, 248 deselected |
| `python -m lab8.crash_test --count 20 --out reports/crash.json` | `crash_safety 20/20` |
| `python -m pytest -q -m student -o addopts=` | 248 passed |
| Kiểm chứng nhánh `BuiQuangHuy-2A202603469` (worktree tạm) | 62 + 3 + 54 test pass |

Run id dẫn chứng: `R-workflow-C-001-s11` (benchmark chính thức), `R-swarm_verified-C-002-s55` (verifier_override công khai trên bản B3 của nhóm).

## 5. Công cụ AI đã dùng

Trợ lý AI (agent lập trình trong phiên của nhóm trưởng) soạn khung `test_eval_integrity.py` và nháp báo cáo. Tôi tự kiểm tra bằng cách: đọc lại từng assert và đối chiếu với `docs/metrics.md` và RUBRIC C6/C7; tự chạy 4 test đó và toàn bộ cổng `pytest -q` (126 passed). Không dùng AI bịa số liệu: mọi số trong báo cáo lấy từ file report do lệnh chuẩn sinh ra hoặc từ lần chạy cục bộ của tôi có output đính kèm.

## 6. Tự đánh giá

Phần có giá trị nhất của tôi là lớp test "chứng từ tự kiểm": từ giờ nếu ai sửa tay JSON trong `src/reports/` hoặc điền số không khớp benchmark vào ADR thì cổng host đỏ ngay. Điểm cần cải thiện: biến thể B3 độc lập của tôi phải push lên nhánh cá nhân sớm thay vì chỉ chạy cục bộ — kết quả đối chiếu chỉ có giá trị khi bằng chứng nằm trên repo.
