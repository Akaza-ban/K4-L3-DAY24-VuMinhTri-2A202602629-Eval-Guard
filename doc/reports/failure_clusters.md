# Phân tích lỗi Phase A

Nhóm: K4-L3-DAY24-VuMinhTri-Eval-Guard

Người phụ trách: Vũ Minh Trí - MSSV 2A202602629

Nguồn: `artifacts/ragas_50q.json`; run timestamp: 2026-10-12T04:17:57.388092+00:00.
Generation mode/fallback và điều kiện chạy: Chạy trực tiếp qua mô hình ngôn ngữ deepseek-flash kết hợp Hybrid Search (BM25 + Semantic chunks).
Models generation/evaluator: Generation dùng deepseek-flash; Evaluator dùng deepseek-flash.

## Điểm theo distribution

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---|---|---|
| faithfulness | 0.9500 | 0.8300 | 0.7700 |
| answer_relevancy | 0.7800 | 0.6125 | 0.7700 |
| context_precision | 0.7650 | 0.6350 | 0.7200 |
| context_recall | 0.6475 | 0.5500 | 0.7000 |
| avg_score | 0.7856 | 0.6569 | 0.7400 |

## Bottom 10 và nguyên nhân

| Rank | Question ID | Distribution | Avg Score | Worst Metric | Diagnosis | Suggested Fix |
|---|---|---|---|---|---|---|
| 1 | 7 | factual | 0.1000 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 2 | 27 | multi_hop | 0.1750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 3 | 26 | multi_hop | 0.2000 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 4 | 50 | adversarial | 0.2000 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 5 | 33 | multi_hop | 0.2250 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 6 | 1 | factual | 0.2500 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 7 | 22 | multi_hop | 0.2500 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 8 | 31 | multi_hop | 0.2500 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 9 | 47 | adversarial | 0.2500 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 10 | 9 | factual | 0.2750 | answer_relevancy | Answer doesn't match question | Improve prompt template |

Đối chiếu answer, contexts và reference của các câu đại diện:
- Câu 1 và 7: Ở câu hỏi về số ngày nghỉ phép khi kết hôn và nghỉ không lương, retrieval lấy được các đoạn văn bản về công tác phí hoặc lưu ý chứng từ nhưng thiếu đoạn quy định trực tiếp số ngày nghỉ cụ thể dẫn đến câu trả lời 'Không tìm thấy' hoặc suy đoán sai.
- Câu 26, 27, 33 (multi-hop): Các câu hỏi suy luận đa bước đòi hỏi phải tổng hợp thông tin từ nhiều điều khoản (thâm niên, quy chế ngày ốm, phiên bản chính sách năm 2024). Context trả về từ bước tìm kiếm ban đầu không đủ bao quát cả 2 nguồn tài liệu dẫn đến context_recall thấp và LLM tự suy diễn sai số liệu (hallucination).

## Matrix và nhóm yếu nhất

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---|---|---|
| faithfulness | 7 | 7 | 4 |
| context_recall | 7 | 5 | 2 |
| context_precision | 4 | 4 | 4 |
| answer_relevancy | 2 | 4 | 0 |

Nhóm yếu theo mean thấp nhất: multi_hop; mean: 0.6569.
Worst metric xuất hiện nhiều nhất: faithfulness; số câu: 18 câu.

Phân tích nguyên nhân:
Nhóm multi_hop có điểm trung bình thấp nhất (0.6569) vì pipeline RAG hiện tại sử dụng chunk kích thước nhỏ (256 ký tự) và BM25 truyền thống, khó liên kết các thực thể nằm rải rác ở hai tài liệu khác nhau. Khi thiếu một phần ngữ cảnh, mô hình có xu hướng tự điền thông tin logic thay vì từ chối, làm giảm điểm faithfulness và context_recall.
Đề xuất cải thiện: Cần tăng kích thước parent chunk, áp dụng reranking Cross-Encoder sâu hơn và bổ sung multi-query expansion trước khi retrieve.

## Bẫy adversarial và giới hạn

So sánh với factual và multi_hop, nhóm adversarial đạt điểm trung bình 0.7400. Các câu hỏi adversarial cố tình đưa vào các chi tiết xung đột phiên bản cũ/mới (như chính sách nghỉ phép năm 2023 vs 2024) hoặc câu hỏi phủ định (như việc tự xử lý malware hay dùng VPN cá nhân). Trong câu 47 và 50, do retrieval lấy cả các đoạn tài liệu có từ khóa VPN mà không lọc theo trạng thái cấm, LLM đã bị đánh lừa bởi context nhiễu.
Giới hạn thực nghiệm: Bộ kiểm thử gồm 50 mẫu chạy trên mô hình deepseek-flash. Cần kiểm nghiệm trên tập dữ liệu rộng hơn và bổ sung metadata filter theo phiên bản hiệu lực của chính sách.
