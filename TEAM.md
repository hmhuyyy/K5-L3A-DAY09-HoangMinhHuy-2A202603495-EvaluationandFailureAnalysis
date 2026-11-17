# Team

## Thông tin nhóm

- Tên nhóm: Vibeforlife
- Lớp: L3A
- Repo nhóm: `K5-L3A-Day08-Vibeforlife-From-Workflows-to-Agents`
- URL repo, nhánh nộp, commit chốt: https://github.com/Stormaka/K5-L3A-Day08-Vibeforlife-From-Workflows-to-Agents · nhánh `main` · commit chốt trùng `- Commit hash:` trong `report/team/decision_adr.md`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Hoàng Bảo Nguyên | 2A202603384 | 26ai.nguyenhb@vinuni.edu.vn | Stormaka | Nhóm trưởng — workflow + integration + ADR |
|   2 | Hoàng Minh Huy |2A202603495  |26ai.huyhm@vinuni.edu.vn |hmhuyyy | single (ReAct) |
|   3 | Bùi Quang Huy | 2A202603469 | 26ai.huybq2@vinuni.edu.vn | harveybui888-max | orchestrator + handoff |
|   4 | Lê Quang Vinh |2A202603363 | 26ai.vinhlq2@vinuni.edu.vn | lequangvinh21 | benchmark/crash/report + bonus B3 |

Phân vai theo gợi ý nhóm 4 người: workflow + integration (nhóm trưởng); single; orchestrator + handoff; eval/report + bonus.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Hoàng Bảo Nguyên | workflow + integration + ADR | commit chốt trên `main` (xem ADR); nhánh cá nhân `HoangBaoNguyen-2A202603384` | `tests/test_workflow_member.py` (6 test: từ chối ticket nói quá trên 5 seed; trace không chứa chữ ticket) |
| Hoàng Minh Huy | single ReAct | `526c06c` — nhánh `HoangMinhHuy_2A202603495`, đã merge vào `main` | `tests/test_single_member.py` (2 test: ReAct trong step cap; không mắc điểm yếu seed 55) |
| Bùi Quang Huy | orchestrator + handoff | `7d4779c` trên nhánh cá nhân `BuiQuangHuy-2A202603469` | `tests/test_orchestrator_member.py` (2 test: handoff sanitize trong trace; không lộ PII đơn của người khác) |
| Lê Quang Vinh | eval/report + bonus B3 | `2739d83` — nhánh `LeQuangVinh-2A202603363`, đã merge vào `main` | `tests/test_eval_integrity.py` (4 test: lưới benchmark, crash 20/20, số ADR khớp benchmark, bonus đủ 3 biến thể); kiểm chứng `tests/test_bonus_swarm_verified.py` (58 test) |

## Cá nhân

Báo cáo cá nhân nằm trong `report/team/`:

- `report/team/2A202603384_HoangBaoNguyen.md` — đã nộp
- `report/team/2A202603469_BuiQuangHuy.md` — đã nộp
- `report/team/2A202603495_HoangMinhHuy.md` — đã nộp
- `report/team/2A202603363_LeQuangVinh.md` — đã nộp
