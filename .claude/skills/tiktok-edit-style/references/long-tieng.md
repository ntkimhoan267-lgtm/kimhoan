# Lồng tiếng

## 1. Viết lời đọc
- Bám bảng kịch bản đã duyệt: mỗi phần một đoạn lời, câu ngắn, giọng nói chuyện ("…nha", "…nè").
- Tiếng Việt đọc tự nhiên ~2,5–3 chữ/giây → video 90s chỉ cần ~150–180 chữ, chừa chỗ thở và chỗ cho hiệu ứng.
- Lời đọc theo cùng luật ở `kich-ban.md` (không "trị", không "tốt nhất", không cam kết kết quả).
- Keyword trên màn hình là cụm đắt nhất của câu đang đọc.

## 2. Chọn giọng — khuyên người dùng tự ghi âm
Video affiliate: giọng thật của người dùng sản phẩm đáng tin hơn giọng AI. Phương án khác:
1. Giọng đọc có sẵn của TikTok (Text-to-speech khi đăng) — miễn phí, có giọng nữ tiếng Việt, an toàn điều khoản.
2. ElevenLabs — chất lượng tốt, gói trả phí cho phép thương mại, cần API key của người dùng.
3. Endpoint giọng Microsoft không chính thức (vd vi-VN-HoaiMy) — chưa rõ có được dùng thương mại không; phải nói rõ rủi ro trước khi dùng.

Hướng dẫn ghi âm gửi người dùng: app Ghi âm iPhone, cách miệng ~20 cm, phòng kín, tắt quạt/điều hoà; đọc từng đoạn, nghỉ 2 giây giữa các đoạn; vấp thì đọc lại cả câu.

## 3. Xử lý (scripts/voiceover.py)
```bash
python scripts/voiceover.py clean  voice.m4a -o work/voice_clean.wav        # lọc ồn, rõ giọng, nén, -15 LUFS
python scripts/voiceover.py words  voice.m4a -o work/words.json --prompt "tên riêng, thương hiệu"
python scripts/voiceover.py pauses work/voice_clean.wav                     # khoảng lặng = điểm cắt
python scripts/voiceover.py layout voice_pieces.json -o work/voice_track.wav --words work/words.json
```
- `words`: faster-whisper large-v3, mốc từng chữ. Whisper hay đặt đầu chữ **sớm** hơn thực tế và nghe nhầm chữ (vd "khoá lại độ ẩm" → "khói lại đồ ẩm") — chỉ dùng để lấy mốc, chữ hiển thị lấy từ kịch bản.
- Đọc transcript để: bỏ câu nói thêm / câu vấp (không đưa vào pieces), bỏ cụm chữ cần đổi (vd người dùng đổi hãng sau khi ghi âm: cho `out` dừng ngay trước tên hãng cũ, card trên hình ghi tên mới).
- Điểm cắt: lấy giữa khoảng lặng trong `pauses`, không lấy thẳng mốc whisper.
- `voice_pieces.json` (mẫu: `examples/skincare-voiceover/voice_pieces.json`): mỗi đoạn `in`/`out` theo file gốc + `gap` = khoảng nghỉ chèn sau. Dùng `gap` để kéo video tới thời lượng người dùng yêu cầu (đoạn nghỉ có hình + hiệu ứng, 1–4s mỗi chỗ).
- **Dựng hình theo giọng**: mọi mốc cảnh / keyword / card lấy từ `voice_track.wav.json` (mốc từng đoạn) và `.words.json` (mốc từng chữ, khoá `t`). Keyword hiện đúng lúc nói chữ đó; card "Bước n" bắt đầu đúng chữ "Bước".
- Có giọng thì không cần phụ đề chạy theo lời khi keyword đã nhắc lại ý; nhắc người dùng có thể bật phụ đề tự động của TikTok.

## 4. Cài đặt
`pip install faster-whisper`. Trong môi trường cloud nếu pip báo không phân giải được pypi.org, chạy pip qua proxy: `NO_PROXY=localhost,127.0.0.1 pip install faster-whisper`. Model tải từ huggingface.co lần đầu.
