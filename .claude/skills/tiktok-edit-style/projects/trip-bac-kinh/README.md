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

## Video 2 – "3 sai lầm khi đi Trung Quốc lần đầu" (đã dựng, 44,5s)
- Kịch bản: `video2-kich-ban.md` (hook A). File dựng: `video2/` (shots → plan → sfx; `pieces.json` dùng `combined.wav` = giọng video 2 + 0,3s lặng + câu "Bắc Kinh không xa đâu" cắt từ giọng video 1, gốc 59,27–61,15s).
- Giọng: bỏ lần đọc vấp "Ba, tới Tử Cấm…" (gốc 32,3–35,9s); người dùng đọc nhầm câu cuối thành "Booking không xa đâu" → thay bằng câu của video 1. Người dùng bỏ "Đi cùng TRIP thì" khi đọc → chữ trên màn hình vẫn ghi "Đi cùng TRIP".
- Lỗi 1 và lỗi 2 tạm dùng thẻ đồ hoạ `video2/gfx/phone.png`, `qr.png` (tự vẽ). Có footage điện thoại mất mạng / quét QR thì thay.
- Trang duyệt có cả video 2 (`#video2`, db `edits/video2`).

## Nhạc nền cho video tour Trung Quốc (người dùng chọn, 18/11/2026)
Thư mục Drive riêng "Nhạc tour Trung Quốc (TRIP)" `1Eka2AIaynyG2v2RcHfGJQh9SqmMjw3UQ` (không chia sẻ). File < 10MB → tải bằng `download_file_content` của Drive, không cần bật chia sẻ. **Mọi video tour Trung Quốc lấy nhạc từ đây**, không dùng nền nhịp tự tạo nữa.
| File | ID Drive | Nhịp | Hợp với |
|---|---|---|---|
| 01-rung-xanh-khong-loi-94bpm-15s.mp3 | `1ZuukOrvg8dhP6lYM4EU28-8lYBgg4k1i` | 94 BPM, 15s, nhẹ, không lời | Cảnh thiên nhiên, đoạn ngắn; phải lặp nếu video dài |
| 02-nhac-trung-khong-loi-105bpm-64s.mp3 | `1TvZqn6LAxIjysonGxYqTLK8MaYSyA70U` | 105 BPM, 64s, nhạc Trung êm | Video nhiều lời đọc, thông tin (visa, hỏi đáp, chi phí) |
| 03-Moment-thuan-nhac-129bpm-50s.mp3 | `1N1afXk8GUtbMfSdByX9JVzLUuQ6ck6lq` | 129 BPM, 50s, sôi động | Vlog/montage cắt theo phách (video 4 "Một ngày ở Bắc Kinh") |
- Nguồn: trích từ video TikTok người dùng gửi; bài 02, 03 là nhạc thương mại có bản quyền (03 = "Moment 纯享版"). Đã báo người dùng rủi ro bị tắt tiếng khi đăng tài khoản doanh nghiệp / chạy quảng cáo; người dùng vẫn chọn dùng. Không commit file nhạc vào repo (repo công khai).
- Cách dùng: `"music": {"src": "music/02.mp3", "volume": 0.12}` trong plan (render.py giữ mức cố định, không tự hạ khi có giọng → để 0,10–0,15), bỏ sự kiện `beat` trong sfx; flash/cắt cảnh theo `beats.py` của chính bài nhạc.
