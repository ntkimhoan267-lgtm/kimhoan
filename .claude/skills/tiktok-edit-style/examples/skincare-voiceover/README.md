# Ví dụ: skincare du lịch 90s, footage ngang, có lồng tiếng + hiệu ứng

Thư mục làm việc: `raw/` chứa 10 clip `IMG_73xx.MOV` (iPhone, quay ngang, HDR), file ghi âm `voice.m4a`.

| File | Vai trò |
|---|---|
| `shots.json` | 24 cảnh, `cx` chọn theo vị trí khuôn mặt, nối thành base 90s (`shots.py`) |
| `voice_pieces.json` | 13 đoạn giọng giữ lại + khoảng nghỉ; đã bỏ 1 câu nói thêm và cắt tên hãng cũ cuối câu bước 2 (`voiceover.py layout`) |
| `sfx_events.json` | 48 hiệu ứng: whoosh+ding cho card, sparkle cho "Bước 3 · Đây rồi!" và kết quả, swish khi đổi cảnh, pop khi keyword hiện (`sfx.py`) |
| `plan.json` | Hook + keyword `pos: low`, 4 card bước + card open loop + CTA, `audio: work/mix.wav` (`render.py`) |

Kịch bản: Hook "Đi biển cả ngày… / tối về da khô căng?" → "skincare 4 bước trong vali" → open loop "bước 3 không thể bỏ qua" → Bước 1 tẩy trang → Bước 2 rửa mặt → Bước 3 mặt nạ (sản phẩm gắn link) → Bước 4 kem dưỡng → kết quả "da ẩm mịn / sẵn sàng ra biển" → CTA "MẶT NẠ BƯỚC 3 / link dưới video".
