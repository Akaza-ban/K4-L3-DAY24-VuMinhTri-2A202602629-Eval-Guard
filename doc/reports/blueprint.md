# Blueprint CI/CD cho RAG và guardrails

Nhóm: K4-L3-DAY24-VuMinhTri-Eval-Guard

Người phụ trách: Vũ Minh Trí - MSSV 2A202602629

Đây là **đề xuất CI/CD**, không phải workflow đã được triển khai/chạy.
Nguồn kết quả: artifacts/ragas_50q.json, judge_results.json, guard_results.json.
Run timestamp: 2026-10-12T04:30:11.758988+00:00; guard models: deepseek-flash.
Models generation/evaluator/judge từ A/B: Generation dùng deepseek-flash (Phase A); Evaluator dùng deepseek-flash (Phase A); Judge dùng deepseek-flash (Phase B); Guardrail dùng deepseek-flash (Phase C).

## Kiến trúc và failure action

Input → Presidio → NeMo input → RAG → NeMo output → response.
Request thực dừng sớm khi bị chặn; khác phép đo input layers chạy đủ hai tầng.

Mô tả luồng dữ liệu (Data Flow):
Mỗi yêu cầu từ người dùng trước hết đi qua tầng Presidio PII để phát hiện và ẩn danh các thực thể nhạy cảm (CCCD, SĐT, Email). Nếu phát hiện cố tình tiêm mã PII không hợp lệ, hệ thống từ chối ngay lập tức và trả thông báo mẫu an toàn. Tiếp đó, input được chuyển qua NeMo input guardrails (Colang self-check) để sàng lọc prompt injection, jailbreak và yêu cầu trái phạm vi hỗ trợ nội bộ. Nếu vi phạm, request bị short-circuit và ngắt luồng. Khi input an toàn, pipeline RAG thực hiện Hybrid Retrieval (BM25 + Semantic Search), Rerank và sinh câu trả lời với LLM. Trước khi gửi câu trả lời về cho người dùng, NeMo output rails kiểm tra rò rỉ dữ liệu cá nhân và thông tin mật.

Chính sách xử lý lỗi (Failure Action) và Quản lý Secrets:
1. Log & Redact: Mọi payload đi vào hệ thống đều được redact PII trước khi ghi vào audit logs (sử dụng Presidio Anonymizer thay thế bằng token `<VN_CCCD>`, `<VN_PHONE>`). Không ghi log văn bản thuần chứa dữ liệu nhạy cảm.
2. Secrets Management: Toàn bộ API keys (DeepSeek, OpenAI) được quản lý qua dịch vụ bảo mật (như HashiCorp Vault hoặc AWS Secrets Manager), tuyệt đối không commit vào repository hoặc lưu trữ trong các file cấu hình tĩnh.
3. Fallback conditions: Nếu NeMo Guardrails hoặc dịch vụ LLM từ xa gặp sự cố timeout (>2000ms) hoặc mã lỗi 5xx, hệ thống tự động fallback về Circuit Breaker: từ chối an toàn với thông báo 'Hệ thống đang bảo trì, vui lòng liên hệ helpdesk@cty.vn' thay vì bỏ qua hàng rào kiểm soát an ninh.

## Phạm vi và số đo latency

Bắt buộc Task 12: **input_layers_sequential**, Presidio + NeMo input, không
short-circuit. Engines tạo trước đo; có hai warm-up thật không tính vào mẫu.
Percentile nội suy tuyến tính từ raw samples; tổng từ tổng từng sample.

Số mẫu timed: 20; warm-up: 2; phương pháp: linear.

| Layer / scope | P50 ms | P95 ms | P99 ms | Tình trạng |
|---|---|---|---|---|
| Presidio | 5.71 ms | 6.80 ms | 7.47 ms | Đạt ngân sách (<10ms), regex và local analyzer thực thi rất nhanh |
| NeMo input | 962.53 ms | 1528.52 ms | 1745.53 ms | Vượt mục tiêu do độ trễ mạng Internet và round-trip của mô hình API từ xa |
| Input guard sequential | 968.42 ms | 1534.18 ms | 1750.88 ms | Tổng hai tầng tuần tự đạt 1534.18 ms tại P95 |
| RAG | chưa đo | chưa đo | chưa đo | Ngoài phạm vi bắt buộc |
| NeMo output | chưa đo | chưa đo | chưa đo | Ngoài phạm vi bắt buộc |
| Full guard / short-circuit request | chưa đo | chưa đo | chưa đo | Không suy từ input_guard_ms |

Input-layer budget target: 500ms; kết quả thực tế: 1534.18 ms; budget_ok: False.

Phân tích điểm nghẽn (Bottleneck):
Điểm nghẽn lớn nhất của hệ thống nằm ở NeMo input guardrails (P95 đạt 1528.52 ms), trong khi tầng Presidio PII hoạt động hoàn toàn cục bộ bằng CPU với thời gian chỉ 6.80 ms ở P95. Lý do NeMo input vượt quá ngưỡng 500ms là vì mỗi lượt kiểm tra self-check input phải gửi HTTP request qua Internet tới API deepseek-flash kèm theo thời gian xử lý tokens.
Kế hoạch đo lường các phần ngoài phạm vi:
Các thành phần RAG, NeMo output và full guard short-circuit hiện ghi nhận 'chưa đo' vì không thuộc phạm vi tuần tự bắt buộc của Task 12. Khi triển khai giai đoạn tới trên môi trường Staging, nhóm sẽ tích hợp OpenTelemetry span tracer, thu thập 100 mẫu với 5 lượt warm-up thật và gắn timestamp chi tiết từ client request đến response hoàn tất.

## CI gates đề xuất

- RAGAS faithfulness ≥0.75, avg_score ≥0.65 trên 50 câu.
- Attacks ≥18/20 cho CI đề xuất; clean 8/8 allowed; output cases đúng.
- Full guard P95 <500ms chỉ áp dụng sau khi thực sự đo full guard.

Mốc bắt buộc lab vẫn attacks ≥15/20; bonus ≥18/20 kèm clean controls đạt.
Đề xuất kịch bản kiểm định tự động (CI Gate Script):
Khi có Pull Request mới, GitHub Actions runner sẽ thực thi lệnh kiểm thử sau:
`python scripts/run_experiments.py --phase all --live && python scripts/check_lab.py --with-tests`
Kịch bản tự động kiểm tra exit code: Nếu bất kỳ chỉ số nào vi phạm ngưỡng (ví dụ RAGAS faithfulness < 0.75, số ca tấn công vượt rào > 2, hoặc false positive rate > 0 trên clean set), script sẽ gọi `sys.exit(1)`, ngăn chặn việc merge vào nhánh chính (main branch). Lưu ý rằng đây là đề xuất workflow cho hệ thống production, hiện tại môi trường repository học tập chưa kích hoạt job runner tự động trên đám mây.

## Monitoring và cải tiến

Chiến lược giám sát vận hành (Production Monitoring):
1. Metrics & Alert Thresholds: Theo dõi tỷ lệ chặn (Block Rate), độ trễ P95/P99 tại từng chặng, tỷ lệ người dùng bấm dislike phản hồi, và tỷ lệ false positive trên traffic thực tế. Nếu tỷ lệ chặn vượt quá 15% trong 1 giờ hoặc P95 vượt 2500ms, hệ thống gửi cảnh báo PagerDuty/Slack tới đội trực On-call.
2. Xử lý False Positives: Định kỳ lấy ngẫu nhiên 5% các câu hỏi bị chặn để đội ngũ chuyên môn (HR, Security) đánh giá lại; nếu xác định là nhầm lẫn, cập nhật bộ whitelist quy tắc Colang và thêm mẫu vào bộ regression test.
3. Chống Data Drift: Hàng tháng lấy mẫu 200 câu hỏi thực tế (đã anonymize PII) để đánh giá lại bằng bộ chỉ số RAGAS và đối chiếu nhãn chuyên gia con người.

RAGAS mean/worst distribution: Mean toàn bộ là 0.7275; nhóm yếu nhất là multi_hop với mean 0.6569.
Cohen’s κ: 1.0000.
Attacks passed: 20/20; clean false_positive_rate: 0.0000 (8/8 câu thông thường được phép đi qua).

Đề xuất các bước cải tiến cụ thể:
1. Triển khai mô hình Guardrail chuyên dụng kích thước nhỏ chạy cục bộ (on-premise Small Language Model như Llama-Guard-3-1B hoặc mô hình classifier phân loại tiếng Việt) thay cho API LLM từ xa để đưa độ trễ P95 của input rail từ 1528ms xuống dưới 80ms.
2. Nâng cấp bộ tìm kiếm RAG từ chunking kích thước cố định lên Parent-Document Retriever và Semantic Chunking nhằm nâng cao điểm context_recall và faithfulness cho các câu hỏi đa bước (multi_hop) vốn đang là điểm yếu nhất (0.6569).
3. Bổ sung bộ lọc Metadata Filter theo phiên bản hiệu lực của chính sách (v2023 vs v2024) ở bước truy vấn để loại bỏ triệt để các context tài liệu lỗi thời gây hallucination ở các câu hỏi bẫy adversarial.
4. Mở rộng bộ dữ liệu kiểm định vàng (Golden Benchmark) từ 50 câu lên 250 câu có gán nhãn đa dạng để đảm bảo độ tin cậy thống kê cao hơn trong quá trình CI/CD liên tục.
