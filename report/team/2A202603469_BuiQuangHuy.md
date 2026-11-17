# Báo cáo cá nhân — Bùi Quang Huy

## 1. Thông tin thành viên

- Họ tên: Bùi Quang Huy
- MSSV: 2A202603469
- Email: 26ai.huybq2@vinuni.edu.vn
- GitHub: harveybui888-max

## 2. Phần việc phụ trách

Shape C — orchestrator và handoff an toàn. Phạm vi gồm tạo `handoff.v1`, chỉ cấp quyền đọc cho investigator, dùng quote từ dữ liệu đã tra cứu để đề xuất hoàn tiền qua host, và bảo đảm trace không ghi parent context hay dữ liệu nhạy cảm.

## 3. Đóng góp cụ thể

- Hoàn thiện `src/lab8/shapes/orchestrator.py`: tạo handoff bằng `make_handoff(..., facts={})` với ba tool chỉ đọc (`lookup_order`, `lookup_policy`, `compute_compensation`); investigator tự tra cứu qua runtime có scope.
- Dùng quote đầy đủ từ investigator khi gọi `durability.issue_refund`; chuyển tiếp `crash_at` và không nuốt `InjectedCrash`. Investigator không có quyền ghi tiền.
- Trace ghi handoff đã sanitize cùng các thông tin điều tra/quote cần thiết; không ghi ticket, parent secret, header, số điện thoại, địa chỉ, internal note hay tên hàng.
- Không sao chép `REFERENCE_WEAKNESS` của swarm. Shape C bỏ hai model call `peer` và `parse`, giữ call `draft` khi cần; đây là khác biệt về chi phí/cấu trúc có thể dùng để giải thích variance.
- Commit chính: `7d4779c5ad8809385a44d6149b96662e1fcb56f9` — `feat: implement shape C`.

## 4. Bằng chứng

- Lệnh `python -m pytest -q -m student -o addopts= -k orchestrator` (chạy trong `src/`): **62 passed, 240 deselected**.
- Lệnh `python -m pytest -q tests/test_handoff_secret.py` (chạy trong `src/`): **3 passed**.
- Các test trên kiểm tra ma trận public của orchestrator, handoff chống secret, và tình huống crash/idempotency trong ma trận.
- `git diff --check`: thành công.

## 5. Công cụ AI đã dùng

- Copilot trong VS Code: hỗ trợ đọc cấu trúc handoff/runtime, triển khai Shape C và rà soát ranh giới dữ liệu.
- Tự kiểm tra bằng cách đọc allowlist và quyền tool trong `src/lab8/handoff.py`, xem trace/test contract, rồi chạy hai lệnh pytest nêu trên. Không dùng model/API key thật; model call của shape dùng MockLLM.

## 6. Tự đánh giá

Điểm quan trọng nhất là ranh giới dữ liệu được thực thi bằng allowlist, không dựa vào việc nhờ LLM tóm tắt để “ẩn” thông tin. Ticket không được sao chép vào handoff (`facts={}`); nếu canary vẫn xuất hiện trong payload sau sanitize thì handoff bị từ chối. Thiết kế cũng tách quyền: investigator chỉ đọc, còn host chuyển quote sang `issue_refund`, nơi kiểm tra approval và giới hạn hoàn tiền.

Kết quả test hiện tại đạt yêu cầu public và secret handoff.
