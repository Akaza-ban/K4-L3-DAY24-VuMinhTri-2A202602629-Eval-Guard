# Nhóm thực hiện K4 Track 3A

Tên nhóm: K4-L3-DAY24-VuMinhTri-Eval-Guard

Repo chung: https://github.com/VinUni-AI20k/K4-Track-3A-Day24-Eval-Guard

Trưởng nhóm/người nộp: Vũ Minh Trí - MSSV 2A202602629

Ngày lab/deadline áp dụng: 23:59 ngày diễn ra lab — Asia/Ho_Chi_Minh (UTC+07:00)

Commit dùng để chấm: b9f8d5b53bc4f94899aa30fdc52c30be0e96eb6d

Mỗi nhóm nộp một repo. Điền đủ thành viên và một mục INDIVIDUAL cho từng người.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Vũ Minh Trí | 2A202602629 | Toàn bộ Phase A, B, C, m1-m5, Guardrails và báo cáo | Commits git, artifacts và reports |

Người tích hợp/chạy batch/nộp link: Vũ Minh Trí, tích hợp toàn bộ pipeline, chạy runner thực nghiệm và kiểm tra checker.

## Môi trường và chuẩn bị trước lớp

OS/Python/compiler: Windows 11, Python 3.11, MSVC C++ runtime.
Virtualenv/dependencies/imports: Đã cài đặt .venv từ requirements.txt, pip check và import kiểm tra đạt 100%.
Models/Qdrant/50 answers đã chuẩn bị: Đã sinh thành công 50 câu trả lời RAG trong artifacts/answers_50q.json bằng DeepSeek LLM.
Runtime đầy đủ với Presidio PII và NeMo Guardrails đã khởi tạo và chạy kiểm thử thành công.

## INDIVIDUAL

### VuMinhTri-2A202602629

- Phần được giao và phần thực tế đã làm: Tự thực hiện toàn bộ bài lab (làm 1 mình): cài đặt pipeline RAG m1-m5, hoàn thiện Phase A RAGAS evaluation, Phase B LLM Judge (pairwise swap-and-average, Cohen kappa, bias analysis), Phase C Presidio PII + NeMo Guardrails, đo latency và viết blueprint.
- Bằng chứng: Các commits trên repo, 4 file dữ liệu chạy thật trong artifacts/ và 3 báo cáo trong doc/reports/.
- Cách kiểm tra: Đạt 86/86 offline unit tests trên pytest; chạy thành công runner live scripts/run_experiments.py; vượt qua toàn bộ checks của scripts/check_lab.py --with-tests.
- Điều đã học: Nắm vững các khía cạnh đánh giá độ tin cậy của RAG qua RAGAS; kỹ thuật phát hiện và khử thiên lệch (position/verbosity bias) của LLM Judge bằng swap-and-average; phương pháp xây dựng guardrail phòng vệ đa tầng kết hợp regex/Presidio cho PII và Colang/NeMo cho prompt injection.
- Giới hạn/cách xử lý: Khắc phục lỗi build C++ của thư viện annoy trên Windows bằng pre-compiled wheel; cấu hình proxy OpenAI-compatible cho DeepSeek API; xử lý encoding UTF-8 trên Windows PowerShell.
- Nguồn/AI hỗ trợ nếu có: Sử dụng Antigravity AI Assistant hỗ trợ rà soát hợp đồng dữ liệu và cấu hình môi trường, tự chạy kiểm chứng 100% bằng test suite của repo.

## Cập nhật sau khi nộp

Phiên bản nộp đúng hạn đầu tiên theo commit đã ghi nhận; không có cập nhật sau deadline.
