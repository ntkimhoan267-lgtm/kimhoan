# Lên kịch bản (làm TRƯỚC khi dựng, gửi người dùng duyệt)

## 1. Xem footage trước, không viết kịch bản "chay"
- Cắt ảnh lưới từng clip: `ffmpeg -i clip.mov -vf "fps=1/N,scale=200:-2,tile=8x2" -frames:v 1 sheet.jpg` (N = thời lượng / 16).
- Cắt ảnh to (960px) ở những khung cầm sản phẩm để **đọc đúng tên trên bao bì**. Không đọc được thì hỏi người dùng, không đoán.
- Ghi lại: clip nào quay gì, quay ngang hay dọc, khuôn mặt nằm bên nào (để chọn `cx` khi crop), có cảnh nào thiếu (vd thiếu cảnh ngoài trời cho chữ "du lịch").

## 2. Cấu trúc copywriting (video 60–90s)
| Phần | Thời lượng | Việc của nó |
|---|---|---|
| Hook | 0–3s | Đánh vào nỗi đau / tò mò / con số. Vd "Đi biển cả ngày… / tối về da khô căng?" |
| Lời hứa | 3–5s | Nói rõ người xem nhận được gì: "skincare 4 bước trong vali" |
| Open loop | 5–8s | Gài một câu hỏi, trả lời ở giữa video: "bước 3 là bước mình không bỏ" → sau đó card "Bước 3 · Đây rồi!" |
| Các bước | phần thân | Mỗi bước: card nhãn pill → cảnh thao tác + keyword. Biến công dụng thành hình ảnh ("tan thành dầu", "uống nước cho da") |
| Mẹo đáng lưu | 1 chỗ | Một mẹo nhỏ khiến người xem bấm lưu ("vỗ hết tinh chất còn lại lên da") |
| Kết quả | 5–10s | Gắn với cảm xúc / bối cảnh ("sáng mai sẵn sàng ra biển"), không cam kết hiệu quả |
| CTA | 5–8s cuối | Nhắc lại open loop + lý do hành động: "MẶT NẠ BƯỚC 3 / link dưới video / lưu lại trước chuyến đi tới" |

- Video affiliate: sản phẩm gắn link là **nhân vật chính** — đặt open loop vào nó, card riêng, CTA gọi đúng tên nó.
- Luôn đưa 2–3 phương án hook để người dùng chọn.
- Kèm gợi ý mô tả khi đăng + hashtag.

## 3. Thông tin sản phẩm & số liệu — tự tra, không bịa
- Công dụng chỉ lấy từ hãng / nhà bán lẻ (WebSearch), ghi nguồn khi trả lời người dùng.
- Không biết chính xác dòng sản phẩm (vd hãng có nhiều dòng sữa rửa mặt) → chỉ ghi tên hãng, không ghi công dụng.
- Hướng dẫn dùng (vd "đắp 10–20 phút") lấy từ bao bì / trang bán.
- Tên địa điểm: tra tên chính thức (vd "Vinpearl Resort & Golf Nam Hội An").

## 4. Luật quảng cáo mỹ phẩm Việt Nam (áp dụng cả video affiliate)
- Cấm: "trị", "điều trị", "đặc trị", "chữa", "làm lành", "ngăn ngừa", "trị mụn/nám" (Luật Quảng cáo 2012 khoản 9 Điều 8, TT 06/2011/TT-BYT); không gây hiểu nhầm là thuốc.
- Tránh (dự thảo mới đề xuất cấm): "tốt nhất", "số 1", "duy nhất", "100%", "hàng đầu", "tuyệt hảo".
- Không cam kết kết quả có số ("15 phút là mọng nước"). Dùng mô tả cảm giác / công dụng hãng công bố: "cấp ẩm", "làm sạch", "khoá ẩm", "da ẩm mịn".
- Ẩn dụ ("uống nước cho da") được, nhưng báo người dùng để họ quyết.

## 5. Gửi duyệt
Bảng: `Giây | Cảnh (clip) | Chữ trên màn hình | Vai trò`, cộng danh sách câu cần người dùng xác nhận (tên sản phẩm chưa rõ, CTA, nhạc). Chỉ dựng khi người dùng nói "ok dựng".
