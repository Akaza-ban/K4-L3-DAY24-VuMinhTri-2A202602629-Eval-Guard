# Đánh giá LLM Judge Phase B

Nhóm: K4-L3-DAY24-VuMinhTri-Eval-Guard

Người phụ trách: Vũ Minh Trí - MSSV 2A202602629

Nguồn: `artifacts/judge_results.json`; run timestamp: 2026-10-12T04:19:27.161522+00:00.
Models generation/judge: Generation sử dụng deepseek-flash; Judge sử dụng deepseek-flash.

## Năm cặp A/B và hai lượt

Nguồn cố định: A từ artifacts/answers_50q.json:answer; B từ
fixtures/human_labels_10q.json:model_answer; reference từ fixtures/test_set_50q.json:ground_truth.
Ids: 1, 5, 12, 21, 41. Không đổi nguồn sau khi xem kết quả judge.

| ID | Candidate A | Candidate B | Winner P1 | Winner P2 | Final Winner | Consistent | Scores P1 (A/B) | Scores P2 (A/B) | Reasoning tóm tắt |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Không tìm thấy. | Nhân viên được nghỉ 3 ngày làm việc có lương khi kết hôn. | B | B | B | True | 0.0 / 0.85 | 0.0 / 0.80 | B nêu đúng số ngày nghỉ và có lương theo reference; A không tìm thấy thông tin. |
| 5 | Không tìm thấy. | Cần Giám đốc phòng ban phê duyệt. | A | tie | tie | False | 0.20 / 0.0 | 0.0 / 0.0 | CEO mới là người duyệt đơn trên 50 triệu; lượt 1 ưu tiên câu từ chối hơn thông tin sai, lượt 2 hòa. |
| 12 | Thưởng Tết tối thiểu cho nhân viên chính thức có từ 6 tháng trở lên là **1 tháng lương**. | Nhân viên được thưởng Tết tối thiểu 1 tháng lương. | A | A | A | True | 1.0 / 0.60 | 1.0 / 0.90 | Cả hai đều đúng nhưng A nêu đầy đủ điều kiện đối tượng (chính thức từ 6 tháng trở lên). |
| 21 | Dựa trên context: 18 ngày phép (15+3). Về lương: Không tìm thấy. | Được nghỉ 18 ngày phép (15 cơ bản + 3 thâm niên). Lương Senior từ 20 đến 35 triệu. | B | B | B | True | 0.50 / 1.0 | 0.50 / 1.0 | B trả lời trọn vẹn cả 2 vế (phép năm và lương); A thiếu thông tin mức lương Senior. |
| 41 | Nhân viên chính thức được hưởng **12 ngày phép năm** có lương. | Nhân viên được nghỉ 12 ngày phép năm. | tie | B | tie | False | 0.20 / 0.15 | 0.05 / 0.10 | Cả hai đều sai do dùng mốc 12 ngày (v2023 cũ thay vì 15 ngày v2024); đổi vị trí làm phán quyết dao động. |

Position bias count/rate: 2 trường hợp (40.0%).
Verbosity win rate: 0.667; decisive cases: 3 (trong 3 cặp có phân định thắng thua, 2 cặp câu trả lời dài hơn giành chiến thắng).

Giải thích các case không nhất quán và các winner dài hơn:
Trong 5 cặp được đánh giá hai lượt với việc đảo vị trí (swap-and-average), có 2 trường hợp xuất hiện position bias (ID 5 và ID 41). Ở câu ID 5, cả hai ứng viên đều không đạt yêu cầu theo tài liệu tham chiếu (CEO phê duyệt đơn hàng trên 50 triệu), lượt 1 judge thiên về A (vì từ chối trung thực hơn là cung cấp sai chức danh), nhưng khi đảo vị trí ở lượt 2 judge chấm hòa. Ở câu ID 41, cả hai ứng viên đều trích xuất sai quy định cũ (12 ngày thay vì 15 ngày), ở lượt 1 judge đánh giá hòa nhưng ở lượt 2 lại chấm B thắng do B ngắn gọn hơn.
Về verbosity bias, tỷ lệ thắng của câu dài hơn là 66.7% (2/3 decisive cases). Tuy nhiên, phân tích nội dung thực tế cho thấy các câu dài hơn thắng (ID 12 và ID 21) là do chúng cung cấp đầy đủ thông tin điều kiện tiên quyết và đầy đủ các vế câu hỏi phức hợp, chứ không đơn thuần vì số lượng từ ngữ. Kỹ thuật swap position và lấy trung bình điểm là bắt buộc để triệt tiêu thiên lệch vị trí của LLM.

## Calibration đúng model_answer

Helper đánh giá đúng question/model_answer đang có trong fixtures/human_labels_10q.json;
không lấy answer mới của pipeline. Prompt chỉ nhận question, answer, reference.
Không gửi human_label, human_note hoặc phân bố nhãn human vào prompt.

| Question ID | Model Answer Gốc | Nhãn Judge (0/1) | Human Label (0/1) | Đồng Thuận (Agree) | Phân Tích Reasoning Của Judge |
|---|---|---|---|---|---|
| 1 | Nhân viên được nghỉ 3 ngày làm việc có lương khi kết hôn. | 1 | 1 | True | Đúng số ngày theo reference (3 ngày làm việc có lương), không mâu thuẫn chính sách. |
| 5 | Cần Giám đốc phòng ban phê duyệt. | 0 | 0 | True | Sai cấp phê duyệt, theo reference đơn hàng trên 50 triệu VNĐ phải do Tổng Giám đốc (CEO) duyệt. |
| 12 | Nhân viên được thưởng Tết tối thiểu 1 tháng lương. | 1 | 1 | True | Trả lời chính xác mức tối thiểu 1 tháng lương cho nhân viên đủ điều kiện. |
| 21 | Được nghỉ 18 ngày phép (15 cơ bản + 3 thâm niên). Lương Senior từ 20 đến 35 triệu. | 1 | 1 | True | Đầy đủ và chính xác cả 2 yếu tố: 18 ngày phép và mức lương Senior 20-35 triệu VNĐ. |
| 23 | Hoàn trả 25 triệu vì chưa đủ 1 năm cam kết. | 1 | 1 | True | Đúng tỷ lệ hoàn trả 100% (25 triệu) do nhân viên nghỉ việc sau 8 tháng (dưới 1 năm cam kết). |
| 29 | Trưởng phòng phê duyệt. Phạt 2% tháng trên 8 triệu. | 0 | 0 | True | Thiếu thẩm quyền Kế toán trưởng cùng phê duyệt và không tính ra số tiền phạt cụ thể 80.000 VNĐ. |
| 33 | Phép: 19 ngày. Phụ cấp: 1.500.000 VNĐ/tháng. | 1 | 1 | True | Khớp chính xác cả hai chế độ: phụ cấp vị trí Manager và tổng số ngày phép theo thâm niên. |
| 41 | Nhân viên được nghỉ 12 ngày phép năm. | 0 | 0 | True | Sai do dùng số liệu v2023 đã hết hiệu lực, chính sách hiện hành v2024 quy định 15 ngày cơ bản. |
| 46 | Nhân viên thử việc không được nghỉ phép năm và phải xin nghỉ không lương nếu cần. | 1 | 1 | True | Nêu đúng quy định nhân viên thử việc không hưởng phép năm và quy trình xin nghỉ không lương. |
| 50 | Được, miễn là đảm bảo kết nối an toàn. | 0 | 0 | True | Vi phạm chính sách an ninh mạng: nghiêm cấm VPN thương mại cá nhân và bắt buộc WireGuard công ty. |

Cohen’s κ: 1.0000.
Observed/chance agreement và diễn giải:
Tỷ lệ đồng thuận quan sát được P_o = 10/10 = 1.0 (100%). Xác suất ngẫu nhiên P_e = (6/10 * 6/10) + (4/10 * 4/10) = 0.36 + 0.16 = 0.52. Hệ số Cohen’s kappa κ = (P_o - P_e) / (1 - P_e) = (1.0 - 0.52) / (1.0 - 0.52) = 1.0000. Kết quả đạt mức gần như tuyệt đối (Almost Perfect Agreement), chứng minh prompt phán quyết nhị phân có hướng dẫn tiêu chí rõ ràng giúp mô hình deepseek-flash đồng thuận hoàn toàn với chuyên gia con người trên tập mẫu thử nghiệm.

## Giới hạn và cách dùng judge

Thực nghiệm calibration trên bộ dữ liệu 10 câu cho hệ số tương quan rất cao (κ = 1.0), tuy nhiên kích thước mẫu n=10 câu và 5 cặp A/B là tương đối nhỏ để khái quát hóa toàn diện cho toàn bộ hệ thống tri thức doanh nghiệp. Mô hình LLM Judge sử dụng là deepseek-flash với prompt tiếng Việt được tinh chỉnh chặt chẽ theo các quy tắc đối chiếu reference.
Trong thực tế production, không bao giờ được coi phán quyết của LLM Judge là sự thật tuyệt đối (ground truth không thể sai). Cần lưu ý các ranh giới quan trọng:
1. LLM Judge vẫn có nguy cơ bị position bias (như đã thấy ở tỷ lệ 40% trong 5 cặp) khi các câu trả lời có chất lượng tương đồng hoặc cùng sai. Biện pháp bắt buộc là luôn dùng hoán đổi vị trí (swap-and-average) trong chế độ pairwise.
2. Đối với các tình huống biên (edge cases) như xung đột phiên bản chính sách hoặc văn bản quy phạm mập mờ, phán quyết của LLM Judge cần được lưu log kèm trích dẫn văn bản và gửi đến con người (Human-in-the-loop) để thẩm định định kỳ.
3. Cần duy trì một tập kiểm thử vàng (Golden Dataset) có nhãn con người để liên tục tái hiệu chuẩn (re-calibrate) khi nâng cấp phiên bản mô hình thẩm định.
