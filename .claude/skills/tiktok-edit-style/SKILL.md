---
name: tiktok-edit-style
description: Lên kịch bản, lồng tiếng, thêm hiệu ứng âm thanh và edit video TikTok/Reels dọc 9:16 theo phong cách "talking-head + chữ keyword serif nghiêng + card nền kem": cắt khoảng lặng và chỗ vấp, phụ đề cụm ngắn, tiêu đề hook mở đầu, chữ keyword theo từng ý, chèn b-roll, card minh hoạ từng bước, CTA cuối. Dùng khi người dùng đưa video gốc (và kịch bản, b-roll, video mẫu) và muốn "edit video", "cắt ghép", "thêm chữ", "viết kịch bản", "lồng tiếng", "âm thanh chuyển cảnh", "video affiliate", "làm video TikTok theo style này".
---

# TikTok edit style — talking-head + keyword serif + card kem

Skill dựng video hoàn chỉnh bằng ffmpeg + Pillow qua 3 script trong `scripts/`.
Mọi đường dẫn script dưới đây tính từ thư mục skill này.

## Phong cách (bám sát khi lên plan)

| Thành phần | Trông như thế nào | Dùng khi |
|---|---|---|
| **Hook** (`hook`) | 2 dòng sans đậm có viền: dòng 1 trắng, dòng 2 cam; dòng accent vàng nhỏ có lấp lánh. Khoảng 18–33% chiều cao màn hình | 0–3s đầu, nêu lợi ích + con số ("Cách edit video / bằng Claude Code / chỉ trong 30'") |
| **Keyword** (`keyword`) | Dòng nhỏ sans trắng ("dành cho") + chữ **serif nghiêng to** hồng nhạt hoặc trắng ("newbie"). Hiện mờ dần + trượt lên | Mỗi ý chính, 2–4s một lần. Chữ to là **từ khoá đắt nhất** của câu đang nói (1–3 từ) |
| **Phụ đề** (`captions`) | Cụm 3–6 chữ, sans semibold trắng có bóng, ở ~71% chiều cao. Trên card tự đổi sang chữ tối | Suốt video có lời nói, cụm nối liền nhau, không nhấp nháy |
| **B-roll** (`broll`) | Video/ảnh phủ kín màn hình, tiếng nói vẫn chạy bên dưới; ảnh tĩnh tự zoom chậm | Mỗi 5–8s lời nói, minh hoạ đúng câu đang nói. Thường đi kèm 1 keyword |
| **Card** (`card`) | Nền kem `#F6F4F1`, nhãn pill màu pastel (blue/pink/yellow/green) ("Bước 1 · Mở Claude Code"), ảnh hoặc video có bóng đổ ở giữa, có thể có chữ serif to ("3–4 tiếng") | Giải thích từng bước, so sánh trước/sau, con số, chụp màn hình |
| **CTA** (`cta`) | Đặt trên card trống: chữ HOA đậm có viền + serif nghiêng to gạch chân hồng + dòng phụ xám | 3–5s cuối: "Comment ...", "link ở bio" |

**Nhịp dựng:**
- Không để khoảng lặng nào quá 0,35s; cắt cả câu nói vấp, nói lặp.
- Màn hình phải đổi (chữ mới, b-roll, card, zoom) ít nhất mỗi 2–3s.
- Các jump cut tự xen kẽ zoom 1.0 ↔ 1.08 để che vết cắt.
- Thứ tự quen thuộc: hook → vấn đề → giải pháp theo từng bước (card) → kết quả → CTA.

## Quy trình

**Luôn theo thứ tự:** xem footage → viết kịch bản (mục **A**) → người dùng duyệt → lồng tiếng nếu có (mục **B**) → dựng → hiệu ứng âm thanh (mục **C**) → kiểm tra → giao.

### 0. Thu thập đầu vào
Hỏi người dùng nếu còn thiếu: video gốc, kịch bản (nếu có), b-roll / ảnh chụp màn hình, nhạc nền (tuỳ chọn), thông điệp CTA. Xem video gốc bằng cách cắt khung hình (`ffmpeg -vf fps=1,scale=240:-1,tile=8x4`) để biết nội dung từng đoạn.

### 1. Cắt + chuẩn hoá
```bash
python scripts/cut.py raw.mp4 -o work/cut.mp4                     # cắt khoảng lặng
python scripts/cut.py raw.mp4 -o work/cut.mp4 --remove 12.4-13.1   # cắt thêm chỗ vấp (giây theo video gốc)
python scripts/cut.py a.mov b.mov c.mov -o work/base.mp4 --no-silence   # video không lời: chỉ ghép
```
- Script tự xoay video iPhone, chuyển HDR về màu thường, đưa về 1080x1920 30fps.
- Có tiếng ồn nền hay nhạc khiến cắt không ăn: chỉnh `--noise -30` (ồn) hoặc `-40` (yên tĩnh). Muốn giữ nhịp thở tự nhiên hơn: `--min-silence 0.5`.
- Ghi kèm `cut.mp4.json` là bảng ánh xạ thời gian gốc sang thời gian mới.

### 2. Phụ đề
```bash
python scripts/transcribe.py work/cut.mp4 -o work/captions.json --lang vi
```
- Cần `pip install faster-whisper`. Nếu thoát với mã 2 (chưa cài), hãy đề nghị người dùng cài, hoặc tự viết `captions.json` từ kịch bản.
- Đọc transcript để: (a) tìm chỗ nói vấp hoặc lặp, rồi quay lại bước 1 với `--remove`, tính lại thời gian theo video gốc; (b) sửa chính tả tiếng Việt và tên riêng; (c) chọn keyword.

### 3. Viết plan.json
Mẫu đầy đủ: `examples/plan.example.json`. Thời gian (`start`/`end`) tính theo video **đã cắt** (`base`).
```json
{
  "base": "work/cut.mp4", "output": "final.mp4",
  "grade": "clean",
  "music": {"src": "music.mp3", "volume": 0.12},
  "captions": "work/captions.json",
  "overlays": [
    {"type": "hook", "start": 0, "end": 2.6, "lines": ["Dòng trắng", "Dòng cam"], "accent": "dòng vàng"},
    {"type": "keyword", "start": 3, "end": 5.5, "small": "dành cho", "big": "newbie", "color": "pink"},
    {"type": "broll", "start": 5.5, "end": 7.5, "src": "broll/office.mov", "src_in": 2.0},
    {"type": "card", "start": 8, "end": 11, "label": "Bước 1 · ...", "color": "blue", "media": "shot.png", "big": "3–4 tiếng"},
    {"type": "card", "start": 25, "end": 29},
    {"type": "cta", "start": 25, "end": 29, "top": "AGENT EDIT VIDEO", "big": "update miễn phí", "sub": "link ở bio"},
    {"type": "text", "start": 12, "end": 14, "text": "chữ tự do", "y": 0.5, "size": 60, "color": "white"}
  ]
}
```
Các tuỳ chọn:
- `grade`: `none` | `clean` | `warm` | `film`.
- Keyword `color`: `pink` | `white` | mã hex.
- Card `media` nhận ảnh hoặc video (video có `src_in`). `media_box: [x, y, w, h]` đổi vùng đặt media. `big_y` (0–1) đổi vị trí chữ to.

Quy tắc chồng lớp: b-roll và card nằm dưới chữ; chữ nằm theo thứ tự trong `overlays`; phụ đề nằm trên cùng.

### 4. Render, kiểm tra, giao
```bash
python scripts/render.py plan.json --preview   # bản 540x960 nhanh
python scripts/render.py plan.json             # bản 1080x1920
```
- Luôn kiểm tra trước khi giao: cắt khoảng 1 khung hình mỗi giây thành ảnh lưới rồi xem. Kiểm tra chữ có đè mặt, đè nhau hay bị tràn không; b-roll có đúng câu đang nói không; có còn khoảng lặng không.
- Khi giao, kèm bảng timeline ngắn (giây, nội dung) và nói rõ những gì chưa làm được, ví dụ chưa có phụ đề tự động hay chưa có nhạc.

## Footage quay ngang / chọn khung từng cảnh
`cut.py` crop giữa khung, dễ cắt mất mặt khi footage quay ngang. Dùng `scripts/shots.py`: mỗi cảnh tự chọn đoạn, `cx` (tâm crop ngang, theo vị trí khuôn mặt), tốc độ; tự xử lý HDR và video xoay; cache từng cảnh nên sửa 1 cảnh chỉ render lại cảnh đó.
```bash
python scripts/shots.py shots.json -o work/base.mp4
```
- Sau khi dựng base, cắt ảnh lưới 1 khung/giây để kiểm tra khung crop; cảnh nào mất mặt thì chỉnh `cx` rồi chạy lại.
- Khi mặt nằm nửa trên khung, đặt chữ ở nửa dưới: `"pos": "low"` cho `keyword` và `hook`.
- Card có thể dùng thẳng video ngang làm `media` (render.py tự chuyển HDR) — hợp cho cảnh giới thiệu sản phẩm cần thấy đủ khung.

## Lồng tiếng + hiệu ứng âm thanh
```bash
python scripts/voiceover.py clean voice.m4a -o work/voice_clean.wav
python scripts/voiceover.py words voice.m4a -o work/words.json
python scripts/voiceover.py layout voice_pieces.json -o work/voice_track.wav --words work/words.json
python scripts/sfx.py sfx_events.json -o work/mix.wav --voice work/voice_track.wav --total 90
```
Rồi thêm `"audio": "work/mix.wav"` vào plan.json. Chi tiết: mục **B** và **C** bên dưới.
Ví dụ hoàn chỉnh (video skincare du lịch 90s, footage ngang, có lồng tiếng + hiệu ứng): `examples/skincare-voiceover/`.

## Font
Font **Playfair Display Italic** (serif nghiêng) và **Be Vietnam Pro** (sans) đã có sẵn trong `fonts/` (giấy phép OFL, file kèm theo). Nếu thiếu, `scripts/fonts.py` tự tải lại từ raw.githubusercontent.com hoặc jsdelivr. Không tải được thì dùng font hệ thống (FreeSerif / Georgia, Inter / Arial). Muốn dùng font thương hiệu riêng, đặt file `.ttf` vào `fonts/` với đúng tên trong `fonts.py`.

## Video không có lời (outfit, sản phẩm, du lịch)
Dùng `cut.py --no-silence` (hoặc `shots.py` nếu quay ngang) để ghép. Bỏ `captions`. Dùng `keyword` cho từng cảnh ("outfit cho" / "ngày ra sân"), `card` cho chi tiết sản phẩm. Vẫn thêm hiệu ứng chuyển cảnh bằng `sfx.py` (không có `--voice`). Video gắn link affiliate: không tự ghép nhạc trend, xem mục **C**.

## A. Lên kịch bản (làm TRƯỚC khi dựng, gửi người dùng duyệt)

### A1. Xem footage trước, không viết kịch bản "chay"
- Cắt ảnh lưới từng clip: `ffmpeg -i clip.mov -vf "fps=1/N,scale=200:-2,tile=8x2" -frames:v 1 sheet.jpg` (N = thời lượng / 16).
- Cắt ảnh to (960px) ở những khung cầm sản phẩm để **đọc đúng tên trên bao bì**. Không đọc được thì hỏi người dùng, không đoán.
- Ghi lại: clip nào quay gì, quay ngang hay dọc, khuôn mặt nằm bên nào (để chọn `cx` khi crop), có cảnh nào thiếu (vd thiếu cảnh ngoài trời cho chữ "du lịch").

### A2. Cấu trúc copywriting (video 60–90s)
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

### A3. Thông tin sản phẩm & số liệu — tự tra, không bịa
- Công dụng chỉ lấy từ hãng / nhà bán lẻ (WebSearch), ghi nguồn khi trả lời người dùng.
- Không biết chính xác dòng sản phẩm (vd hãng có nhiều dòng sữa rửa mặt) → chỉ ghi tên hãng, không ghi công dụng.
- Hướng dẫn dùng (vd "đắp 10–20 phút") lấy từ bao bì / trang bán.
- Tên địa điểm: tra tên chính thức (vd "Vinpearl Resort & Golf Nam Hội An").

### A4. Luật quảng cáo mỹ phẩm Việt Nam (áp dụng cả video affiliate)
- Cấm: "trị", "điều trị", "đặc trị", "chữa", "làm lành", "ngăn ngừa", "trị mụn/nám" (Luật Quảng cáo 2012 khoản 9 Điều 8, TT 06/2011/TT-BYT); không gây hiểu nhầm là thuốc.
- Tránh (dự thảo mới đề xuất cấm): "tốt nhất", "số 1", "duy nhất", "100%", "hàng đầu", "tuyệt hảo".
- Không cam kết kết quả có số ("15 phút là mọng nước"). Dùng mô tả cảm giác / công dụng hãng công bố: "cấp ẩm", "làm sạch", "khoá ẩm", "da ẩm mịn".
- Ẩn dụ ("uống nước cho da") được, nhưng báo người dùng để họ quyết.

### A5. Gửi duyệt
Bảng: `Giây | Cảnh (clip) | Chữ trên màn hình | Vai trò`, cộng danh sách câu cần người dùng xác nhận (tên sản phẩm chưa rõ, CTA, nhạc). Chỉ dựng khi người dùng nói "ok dựng".

## B. Lồng tiếng

### B1. Viết lời đọc
- Bám bảng kịch bản đã duyệt: mỗi phần một đoạn lời, câu ngắn, giọng nói chuyện ("…nha", "…nè").
- Tiếng Việt đọc tự nhiên ~2,5–3 chữ/giây → video 90s chỉ cần ~150–180 chữ, chừa chỗ thở và chỗ cho hiệu ứng.
- Lời đọc theo cùng luật ở mục **A** (không "trị", không "tốt nhất", không cam kết kết quả).
- Keyword trên màn hình là cụm đắt nhất của câu đang đọc.

### B2. Chọn giọng — khuyên người dùng tự ghi âm
Video affiliate: giọng thật của người dùng sản phẩm đáng tin hơn giọng AI. Phương án khác:
1. Giọng đọc có sẵn của TikTok (Text-to-speech khi đăng) — miễn phí, có giọng nữ tiếng Việt, an toàn điều khoản.
2. ElevenLabs — chất lượng tốt, gói trả phí cho phép thương mại, cần API key của người dùng.
3. Endpoint giọng Microsoft không chính thức (vd vi-VN-HoaiMy) — chưa rõ có được dùng thương mại không; phải nói rõ rủi ro trước khi dùng.

Hướng dẫn ghi âm gửi người dùng: app Ghi âm iPhone, cách miệng ~20 cm, phòng kín, tắt quạt/điều hoà; đọc từng đoạn, nghỉ 2 giây giữa các đoạn; vấp thì đọc lại cả câu.

### B3. Xử lý (scripts/voiceover.py)
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

### B4. Cài đặt
`pip install faster-whisper`. Trong môi trường cloud nếu pip báo không phân giải được pypi.org, chạy pip qua proxy: `NO_PROXY=localhost,127.0.0.1 pip install faster-whisper`. Model tải từ huggingface.co lần đầu.

## C. Âm thanh: hiệu ứng chuyển cảnh + nhạc

### Hiệu ứng chuyển cảnh (scripts/sfx.py)
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

### Nhạc nền
- Video có gắn link sản phẩm (affiliate / TikTok Shop) bị tính là **nội dung thương mại** → chỉ dùng nhạc trong **Commercial Music Library** của TikTok hoặc nhạc có license thương mại; sound trend thường có thể bị tắt tiếng / gỡ.
- Khi người dùng nhờ đề xuất "sound trend": tra WebSearch cho tháng hiện tại, nói rõ nguồn là blog tổng hợp, và hướng dẫn chọn trong app: Thêm âm thanh → mục Commercial → lọc "chill / lofi / acoustic".
- Mặc định xuất video **không nhạc** để người dùng ghép nhạc trên TikTok; nếu có giọng, dặn để nhạc ~10–15%.
