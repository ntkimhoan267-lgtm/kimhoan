---
name: tiktok-edit-style
description: Edit video TikTok/Reels dọc 9:16 theo phong cách "talking-head + chữ keyword serif nghiêng + card nền kem": cắt khoảng lặng và chỗ vấp, phụ đề cụm ngắn, tiêu đề hook mở đầu, chữ keyword theo từng ý, chèn b-roll, card minh hoạ từng bước, CTA cuối. Dùng khi người dùng đưa video gốc (và kịch bản, b-roll, video mẫu) và muốn "edit video", "cắt ghép", "thêm chữ", "làm video TikTok theo style này".
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

## Font
`scripts/fonts.py` tự tải **Playfair Display Italic** (serif nghiêng) và **Be Vietnam Pro** (sans) vào `fonts/`. Không tải được thì dùng font hệ thống (FreeSerif / Georgia, Inter / Arial). Muốn dùng font thương hiệu riêng, đặt file `.ttf` vào `fonts/` với đúng tên trong `fonts.py`.

## Video không có lời (outfit, sản phẩm, du lịch)
Dùng `cut.py --no-silence` để ghép. Bỏ `captions`. Dùng `keyword` cho từng cảnh ("outfit cho" / "ngày ra sân"), `card` cho chi tiết sản phẩm, và `music` (volume ~0.8) làm âm thanh chính.
