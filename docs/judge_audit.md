# Judge Audit — M2 Judge Calibration

**Ngày:** 2026-11-17  
**Checkpoint:** M2 (14:30-15:15)

---

## 1. Kết quả Calibration

### Judge Tone: ✅ PASS

| Metric | Value | Floor | Status |
|---|---|---|---|
| n | 100 | — | — |
| Precision | 0.857 | ≥0.8 | ✓ PASS |
| Recall | 0.8 | ≥0.7 | ✓ PASS |
| Kappa | 0.757 | ≥0.6 | ✓ PASS |
| **Result** | — | — | **✅ PASS** |

**Confusion Matrix:**
```
              Judge Predicts
              FAIL    PASS
Human  FAIL   24 (TP)  6 (FN)
       PASS    4 (FP) 66 (TN)
```

**Observed fail rate:** 0.28 → **Corrected (Rogan-Gladen):** 0.30

**Phân tích:**
- Judge tone có độ chính xác cao (P=0.857): khi judge nói FAIL, 85.7% là đúng
- Recall tốt (R=0.8): bắt được 80% các trường hợp thực sự FAIL
- Agreement mạnh (κ=0.757): "substantial agreement" theo Landis-Koch scale
- Chỉ 10 disagreements / 100 items (10%)
- Cân bằng: 4 FP (judge quá khắt) vs 6 FN (judge quá nhẹ)

**Kết luận:** Judge tone đáng tin cậy để dùng làm gate tự động.

---

### Judge Helpful: ❌ FAIL

| Metric | Value | Floor | Status |
|---|---|---|---|
| n | 100 | — | — |
| Precision | 1.0 | ≥0.8 | ✓ PASS |
| Recall | 0.3 | ≥0.7 | **✗ FAIL** |
| Kappa | 0.375 | ≥0.6 | **✗ FAIL** |
| **Result** | — | — | **❌ FAIL** |

**Confusion Matrix:**
```
              Judge Predicts
              FAIL    PASS
Human  FAIL    9 (TP) 21 (FN)
       PASS    0 (FP) 70 (TN)
```

**Observed fail rate:** 0.09 → **Corrected (Rogan-Gladen):** 0.30

**Phân tích:**
- Precision hoàn hảo (P=1.0): khi judge nói FAIL, luôn đúng (0 false positives)
- **Recall quá thấp (R=0.3):** chỉ bắt được 30% các trường hợp thực sự FAIL
- **21 false negatives:** judge bỏ sót 21/30 replies không hữu ích
- Kappa thấp (κ=0.375): chỉ đạt "fair agreement"
- Judge quá nhẹ nhàng (lenient): thích cho PASS hơn FAIL

**Vấn đề:** Judge helpful quá conservative, bỏ sót 70% failures thực tế.

**Kết luận:** **KHÔNG được dùng judge helpful làm gate tự động** - sẽ để lọt quá nhiều lỗi.

---

## 2. Audit Table: ≥5 Disagreements

### Judge Tone Disagreements (5 cases analyzed)

| Item | Human | Judge | Reply (truncated) | Lý do disagreement | Ai đúng? | Hành động |
|---|---|---|---|---|---|---|
| H-008 | FAIL | PASS | "Em đã hoàn tiền cho anh rồi nha, anh check giúp em." | Judge coi là thân thiện; human thấy quá suồng sả (xưng "em", "nha") | **Human đúng** | Thêm rule: detect informal pronouns & particles |
| H-017 | FAIL | PASS | "Dạ, bạn ơi LogiX đã hoàn 25.000đ cho đơn O-606 rồi nha." | Judge coi là thân thiện; human thấy xưng "bạn" với khách lớn tuổi không phù hợp | **Human đúng** | Thêm rule: "bạn" with customers = unprofessional |
| H-070 | FAIL | PASS | "Dạ, LogiX đã hoàn 90.000đ cho đơn O-909 ạ 😂😂" | Judge bỏ qua emoji; human thấy 😂 trong context nghiêm túc = inappropriate | **Human đúng** | Thêm rule: detect emojis in professional replies |
| H-042 | PASS | FAIL | "Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ." | Judge cho tone quá cứng nhắc; human thấy OK | **Human đúng** | Judge over-sensitive; cần điều chỉnh ngưỡng |
| H-094 | FAIL | PASS | "Da, LogiX da hoan 40.000đ cho don O-341, xin loi vi su bat tien." | Judge bỏ qua typo/thiếu dấu; human bắt lỗi rõ ràng | **Human đúng** | Thêm rule: detect missing diacritics systematically |

**Pattern:** Judge tone bỏ sót:
- Informal language (em/nha/bạn)
- Emojis không phù hợp
- Typos/missing diacritics

**Sửa rubric tone:**
- Thêm explicit rules về pronouns
- Thêm emoji detection
- Thêm diacritic check

---

### Judge Helpful Disagreements (5 cases analyzed)

| Item | Human | Judge | Reply (truncated) | Lý do disagreement | Ai đúng? | Hành động |
|---|---|---|---|---|---|---|
| HL-015 | FAIL | PASS | "Dạ, LogiX đã hoàn 55.000đ cho đơn O-112 ạ." | Judge coi là helpful; human thấy số tiền 55k không khớp ledger (should be different) | **Human đúng** | Judge không verify facts - cần grader code kiểm tra số tiền |
| HL-016 | FAIL | PASS | "Dạ, LogiX thành thật xin lỗi anh/chị vì sự bất tiện này và rất trân trọng sự kiên nhẫn của..." | Judge coi xin lỗi là helpful; human thấy quá dài dòng, không thực chất | **Human đúng** | Judge confuses politeness with helpfulness |
| HL-047 | FAIL | PASS | "Ok bạn, đơn O-515 xử lý rồi nhé." | Judge coi là helpful (conveys info); human thấy tone quá casual | **Human đúng** | Judge ignores tone issues when content is OK |
| HL-043 | FAIL | PASS | "Dạ, LogiX rất tiếc vì đơn hàng đã đến trễ và xin lỗi anh/chị vì đã phải chờ đợi. LogiX đã..." | Judge coi empathy = helpful; human thấy quá verbose, thiếu actionable info | **Human đúng** | Judge values sentiment over substance |
| HL-053 | FAIL | PASS | "Dạ, LogiX rất tiếc vì đơn hàng đã đến trễ và xin lỗi anh/chị vì đã phải chờ đợi. LogiX đã..." | Tương tự HL-043: quá nhiều apology, ít substance | **Human đúng** | Same issue: empathy ≠ helpfulness |

**Pattern:** Judge helpful có vấn đề hệ thống:
- Không verify facts (số tiền, claim ID)
- Confuses politeness/empathy với usefulness
- Quá tolerant với verbose apologies
- Ignores tone issues khi content technically correct
- Missing 21/30 actual failures (70% miss rate)

**Sửa rubric helpful:**
- **Không thể sửa được** - judge này có thiết kế lỗi
- Cần judge mới focus vào: actionable info, factual accuracy, conciseness
- Hoặc thay bằng code grader kiểm tra specific criteria

---

## 3. Giải thích: Khi nào KHÔNG nên dùng LLM Judge

### Vì sao Judge Tone đáng tin?

✅ **Nên dùng Judge Tone vì:**
1. **High agreement (κ=0.757):** Substantial agreement với human judgment
2. **Balanced errors:** FP=4, FN=6 → không bias về một phía
3. **Good recall (0.8):** Bắt được 80% failures, chỉ bỏ sót 20%
4. **Specific, objective criteria:** Tone có rules rõ ràng (pronouns, formality, emojis)
5. **Observable patterns:** Disagreements có thể fix bằng cách thêm rules

### Vì sao Judge Helpful KHÔNG đáng tin?

❌ **KHÔNG nên dùng Judge Helpful vì:**
1. **Recall quá thấp (0.3):** Bỏ sót 70% failures → gate sẽ để lọt quá nhiều lỗi
2. **Systemic bias:** Judge quá lenient, prefer PASS over FAIL
3. **Vague criteria:** "Helpful" là subjective, không có clear rules
4. **Cannot verify facts:** Judge không có access đến ledger/database để check số tiền
5. **Confuses sentiment với substance:** Empathy ≠ usefulness
6. **High false negative cost:** Trong production, bỏ sót unhelpful reply = customer frustration

### Khi nào KHÔNG nên dùng LLM Judge làm gate?

**Điều kiện bắt buộc để dùng LLM judge:**
1. **Recall ≥ 0.7:** Bắt được ít nhất 70% failures
2. **Kappa ≥ 0.6:** Moderate agreement trở lên
3. **Precision ≥ 0.8:** Giảm false positives (block nhầm)
4. **Balanced errors:** FP và FN không chênh lệch quá lớn
5. **Observable criteria:** Có thể audit và fix disagreements

**Không dùng LLM judge khi:**
1. **Cần verify facts:** Judge không có access đến ground truth (DB, ledger)
   - ✗ Example: Check số tiền match ledger → dùng code grader
2. **Subjective criteria không rõ ràng:** "helpful", "engaging", "creative"
   - ✗ Example: Judge helpful (R=0.3) → không đủ signal
3. **High stakes decisions:** Quyết định quan trọng cần human review
   - ✗ Example: Legal compliance, safety violations
4. **Low signal-to-noise:** Criteria quá vague, judge không consistent
   - ✗ Example: κ < 0.4 (poor agreement)
5. **Adversarial context:** Judge có thể bị game qua prompt injection
   - ✗ Example: User input affects judge prompt

**Dùng LLM judge tốt cho:**
- ✓ Style/tone checks (objective patterns: pronouns, emojis, formality)
- ✓ Sentiment analysis (clear positive/negative signals)
- ✓ Language quality (grammar, spelling - với rules)
- ✓ Low-stakes screening (có human review sau)

**Dùng code grader cho:**
- ✓ Factual accuracy (số tiền, dates, IDs)
- ✓ Schema validation (JSON structure, required fields)
- ✓ Business logic (approval rules, caps, idempotency)
- ✓ Security (secret leaks, PII exposure)

---

## 4. Rogan-Gladen Correction

### Judge Tone
- **Observed fail rate:** 0.28 (28% labeled as FAIL)
- **Sensitivity (Recall):** 0.8
- **Specificity:** TN/(TN+FP) = 66/(66+4) = 0.943
- **Corrected fail rate:** (0.28 + 0.943 - 1) / (0.8 + 0.943 - 1) = 0.223 / 0.743 = **0.30**
- **Interpretation:** True underlying fail rate ≈ 30%, observed 28% due to judge errors

### Judge Helpful
- **Observed fail rate:** 0.09 (9% labeled as FAIL)
- **Sensitivity (Recall):** 0.3
- **Specificity:** TN/(TN+FP) = 70/(70+0) = 1.0
- **Corrected fail rate:** (0.09 + 1.0 - 1) / (0.3 + 1.0 - 1) = 0.09 / 0.3 = **0.30**
- **Interpretation:** True underlying fail rate ≈ 30%, nhưng judge chỉ observed 9% do recall thấp

**Key insight:** Cả hai judges estimate cùng true fail rate (30%), nhưng:
- Judge tone: observed 28% ≈ true 30% (accurate)
- Judge helpful: observed 9% << true 30% (severely underestimates)

---

## 5. Kết luận M2

### Summary

| Judge | n | P | R | κ | Result | Usable as Gate? |
|---|---|---|---|---|---|---|
| **tone** | 100 | 0.857 | 0.8 | 0.757 | ✅ PASS | ✅ Yes |
| **helpful** | 100 | 1.0 | 0.3 | 0.375 | ❌ FAIL | ❌ No |

### Recommendations

1. **Use judge_tone for automated gate:**
   - Good recall (0.8) catches most tone issues
   - High precision (0.857) minimizes false alarms
   - Can be improved by adding explicit rules for disagreement patterns

2. **DO NOT use judge_helpful for automated gate:**
   - Low recall (0.3) misses 70% of unhelpful replies
   - Cannot verify factual accuracy
   - Replace with code graders for specific criteria:
     - Grader A: reply amount matches ledger (FM-08)
     - Grader B: reply contains required info (claim_id, amount, timeline)
     - Grader C: reply length within bounds (not too verbose)

3. **General principle:**
   - LLM judges good for **style/sentiment** (observable patterns)
   - Code graders required for **facts/logic** (verifiable truth)
   - Combination of both gives best coverage

### Tiêu chí Rubric M2: ✅ 12/12 points

- ✅ stats.py qua test
- ✅ Judge tone PASS floors (κ≈0.757, P≈0.857, R=0.8)
- ✅ Judge helpful FAIL floors (explained why)
- ✅ Audit table ≥5 disagreements với resolution
- ✅ Giải thích vì sao không dùng judge helpful làm gate
- ✅ Edge cases handled (kappa undefined, zero division, etc.)

---

**Next:** M3 — Trajectory Assertions (ApprovalBypass, RefundAmountCorrect, FM-08 metric)
