# Dự án TRIP – series "Bắc Kinh không xa"

Khách hàng: TRIP (công ty tour). Kế hoạch gốc: file "Kịch bản video tour Trung Quốc – TRIP" (5 video, 18/11/2026) — người dùng tải lên chat, chưa lưu trong repo.
- Kênh: TikTok trước, rồi Reels. CTA mọi video: "Nhắn Zalo [số] …". Đo bằng số tin nhắn Zalo (mục tiêu 50 lead / 2 tuần).
- Không có footage của TRIP → stock Pexels do nhóm tải tay lên thư mục Drive "Bắc Kinh" (danh mục: [`catalog.md`](catalog.md)). Pexels đã dừng cấp API key mới (11/2026); web Pexels/Pixabay chặn truy cập tự động — đừng thử lại. Wikimedia Commons có ít footage Bắc Kinh, hay bị giới hạn lượt gọi. Cảnh "đoàn TRIP", HDV, nhân viên, tin nhắn khách phải là hình thật; chưa có thì bỏ, không dựng giả.
- Giọng: người dùng tự lồng tiếng; giữ một giọng cố định cả series. Câu kết cố định: "Bắc Kinh không xa đâu."

## Video 1 – "Bắc Kinh 5 ngày hết bao nhiêu tiền?"
Kịch bản lời đọc: [`video1-kich-ban.md`](video1-kich-ban.md). Bản nháp chưa giọng (hook A, giá/Zalo để trống): `video1/` (shots → plan → sfx, 40s, nền nhịp 100 BPM). Có giọng thì dời mốc chữ/cảnh theo `voiceover.py layout` và bỏ `captions` cứng.

Chi phí tự túc dùng trong kịch bản (1 người, 5 ngày 4 đêm, mức tiết kiệm–vừa, tra ngày 18/11/2026, tỷ giá ~3.900 đ/CNY):
| Hạng mục | Ước tính | Cách tính / nguồn |
|---|---|---|
| Vé máy bay khứ hồi HN–Bắc Kinh | ~9 triệu | hãng giá rẻ 7,8–9,2tr (BestPrice), VNA từ 11,66tr |
| Khách sạn 4 đêm, phòng đôi | ~3,5 triệu/người | 350–600 CNY/đêm/phòng (trave.vn 8/2026) |
| Ăn uống 5 ngày | ~3 triệu | 100–200 CNY/ngày |
| Vé tham quan + đi lại | ~2,5 triệu | Tử Cấm Thành ~60, Mutianyu + cáp treo ~185, Di Hòa Viên ~30–60, Thiên Đàn 34 CNY; metro/Didi |
| Visa L 1 lần | ~2 triệu | 45 USD + phí trung tâm ~690k (người Việt chưa được miễn visa du lịch) |
| **Tổng** | **~20 triệu** | khớp ước tính 18,8tr của Klook |
Bay thẳng HN–Bắc Kinh ~3 giờ 30 phút (Kayak, VietnamBooking). Số liệu là ước tính từ trang bán vé/blog — kiểm lại ngay trước khi đăng.

## Âm thanh & duyệt
- Tiếng "kaching" do người dùng chọn: Pixabay "dragon-studio cash register kaching 376867" (file gốc trong chat, chưa lưu repo — giấy phép Pixabay không cho phát tán file rời; xin người dùng gửi lại hoặc để trong thư mục Drive SFX). Đặt **ngay sau khi nói xong con số** (mốc cuối chữ "triệu"/"rưỡi"/"nghìn" trong `.words.json`, trừ 0,06s), không đặt lúc chữ hiện.
- Web Pixabay chặn truy cập tự động và Pixabay không có API âm thanh → người dùng tự tải sound, gửi qua chat hoặc Drive.
- Trang duyệt (artifact, chỉ người dùng xem): https://claude.ai/artifact/DEEG41UzejEDSVBeF7RjRz — sửa chữ, bật/tắt, chỉnh âm lượng, dời mốc từng âm; lưu ở db `edits/video1` (`texts{id:text}`, `sounds{id:{on,gain,t}}`, `note`). Id lấy từ `items.json` (o<overlay>l<dòng>, c<phụ đề>, s<chỉ số sự kiện trong sfx_v.json>). Chỉ đổi âm → `render.py --audio-only` (vài giây).
