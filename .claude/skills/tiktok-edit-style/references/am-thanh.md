# Âm thanh: hiệu ứng chuyển cảnh + nhạc

## Hiệu ứng chuyển cảnh (scripts/sfx.py)
Tự tổng hợp bằng numpy → không dính bản quyền. Nghe thử: `python scripts/sfx.py --export work/sfx/`.

| Âm | Đặt ở đâu |
|---|---|
| `whoosh` (vút dài) | Card mới hiện lên, CTA — đặt sớm 0,12s trước mốc |
| `ding` | Ngay sau whoosh của card "Bước n", card CTA (+0,12s) |
| `sparkle` (lấp lánh) | Khoảnh khắc "đây rồi" (card sản phẩm chính), cảnh kết quả |
| `swish` (vút ngắn) | Mỗi lần đổi cảnh thường |
| `pop` | Mỗi keyword mới hiện ra; chữ "link" trong CTA; hook ở 0,3s |

```bash
python scripts/sfx.py sfx_events.json -o work/mix.wav --voice work/voice_track.wav --total 90 [--level 0.8]
```
- `sfx_events.json`: `[["whoosh", 12.9], ["ding", 13.3], {"sfx": "pop", "t": 20.2, "gain": 0.8}]` (mẫu: `examples/skincare-voiceover/sfx_events.json`).
- Đang có giọng thì hiệu ứng tự nhỏ lại x0.6. Người dùng chê to/nhỏ → chỉ chạy lại với `--level`, không cần dựng lại hình.
- Ghép vào video: thêm `"audio": "work/mix.wav"` vào plan.json (render.py dùng track này thay tiếng gốc).
- Video không lời vẫn nên có hiệu ứng ở mỗi chuyển cảnh (người dùng hỏi "âm thanh chuyển cảnh đâu" = thiếu phần này).

## Nhạc nền
- Video có gắn link sản phẩm (affiliate / TikTok Shop) bị tính là **nội dung thương mại** → chỉ dùng nhạc trong **Commercial Music Library** của TikTok hoặc nhạc có license thương mại; sound trend thường có thể bị tắt tiếng / gỡ.
- Khi người dùng nhờ đề xuất "sound trend": tra WebSearch cho tháng hiện tại, nói rõ nguồn là blog tổng hợp, và hướng dẫn chọn trong app: Thêm âm thanh → mục Commercial → lọc "chill / lofi / acoustic".
- Mặc định xuất video **không nhạc** để người dùng ghép nhạc trên TikTok; nếu có giọng, dặn để nhạc ~10–15%.
