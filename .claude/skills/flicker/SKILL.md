---
name: flicker
description: Edit video skincare (kênh affiliate TikTok của Kim Hoàn) theo trend nháy kiểu CapCut — Flicker (chủ thể loé trắng / âm bản / phát sáng), Frame Flick (cảnh sau nháy trong khung chữ nhật trước khi cắt), Mask Frame (cảnh sau hiện từng ô lưới) — cắt theo phách nhạc flicker 145 BPM, chữ hook + stack + CTA giỏ hàng. Dùng khi người dùng nhắn "flicker", "/flicker", "edit skincare kiểu flicker", "video nháy", "làm video skincare như video 4 TRIP".
---

# /flicker — video skincare trend nháy (CapCut Flicker / Frame Flick / Mask Frame)

Người dùng chỉ cần mở phiên và nhắn **"flicker"** (có thể kèm tên sản phẩm). Tự làm hết, chỉ hỏi khi thật sự thiếu thông tin. Người dùng hay dùng điện thoại → trả lời ngắn, tiếng Việt, gửi video bằng SendUserFile.

Công cụ dựng nằm ở skill `tiktok-edit-style` (đường dẫn `../tiktok-edit-style/`). Đọc mục **D3b** trong `../tiktok-edit-style/SKILL.md` (khoá `fx`) và mục 1, 3, 4, C khi cần chi tiết. **Không** dùng `flash` nháy cả khung — người dùng đã xác nhận là sai.

## 0. Đọc trước (không tải lại cả thư mục Drive)
1. `../tiktok-edit-style/projects/skincare/README.md` + `catalog.md`: ID Drive từng video, sản phẩm, mốc cảnh đẹp, đối thủ, video đã làm.
2. Mẫu dựng hoàn chỉnh của hiệu ứng: `../tiktok-edit-style/projects/trip-bac-kinh/video4/ref-fx/` (`shots_ref.json`, `plan_ref.json`, `sfx_ref.json`). Bắt chước cấu trúc `fx`, mật độ và âm thanh.
3. Mẫu dựng skincare cũ (chữ, CTA, nhịp): `../tiktok-edit-style/projects/skincare/ahc-kem-mat/`.

## 1. Chọn sản phẩm
- Người dùng nêu sản phẩm → dùng sản phẩm đó. Không nêu → chọn sản phẩm **chưa làm** có nhiều ⭐ source nhất trong README (bảng "Sản phẩm có trong source"), nói 1 câu đã chọn gì rồi làm luôn.
- Tên sản phẩm đọc từ bao bì (cắt khung 960px lúc cầm sản phẩm). Không đọc được thì hỏi, không đoán.
- Công dụng / thành phần: tra web, theo luật quảng cáo mỹ phẩm (mục A4 của tiktok-edit-style): không hứa chữa trị, không "hết thâm/nâng cơ sau x ngày".

## 2. Tải nguyên liệu (vào scratchpad, thư mục `flicker-<sản phẩm>/`)
- Footage: file < 10MB → `download_file_content` của Drive (không cần chia sẻ). File lớn → `bash ../tiktok-edit-style/scripts/drive_fetch.sh raw <ID>:<tên>.mp4` (cần thư mục Skincare bật chia sẻ link; tải xong nhắc người dùng tắt). Chỉ tải 3–6 file ⭐ cần dùng.
- Nhạc: Drive thư mục **"Nhạc trend Flicker (edit video)"** `1GEybjb1Ffnr7ol8R1pVl92yQUTcldg3U` → `01-flicker-145bpm-60s.mp3` `1_q2nmu8JbYTsO2X3bSUtJyB14rydwuNr` (1,4MB, tải bằng `download_file_content`, lưu `music/flicker.mp3`). Nhạc trích từ video hướng dẫn CapCut người dùng gửi, lặp đoạn intro không lời — **không commit vào repo**. Người dùng gửi bài khác/bài gốc → thêm vào thư mục Drive đó, ghi lại ở bảng dưới.
- Phách: **B = 0,412s** (145,6 BPM), phách mạnh mỗi 0,824s, bắt đầu ~0,07s. Kiểm lại bằng `python ../tiktok-edit-style/scripts/beats.py music/flicker.mp3`.

| Nhạc | ID Drive | BPM / phách | Ghi chú |
|---|---|---|---|
| 01-flicker-145bpm-60s.mp3 | `1_q2nmu8JbYTsO2X3bSUtJyB14rydwuNr` | 145,6 / B=0,412s | Nhạc intro video hướng dẫn, lặp 48 phách, fade cuối |

## 3. Kịch bản + dựng (20–30s, không lời, chỉ chữ + nhạc + SFX)
Source skincare không có lời nói → video montage. Viết nhanh kịch bản chữ (hook theo đối thủ trong README: nỗi đau + câu hỏi tương tác tốt nhất), gửi kèm video luôn (không cần chờ duyệt riêng, trừ khi người dùng yêu cầu).

Nhịp chuẩn (B = 0,412s, mọi mốc cắt là bội số B):
| Đoạn | Thời gian | Hình | `fx` |
|---|---|---|---|
| Hook | 0 – 8B (~3,3s) | Cảnh cầm sản phẩm cạnh mặt / mặt căng bóng | `flicker` `white` lên người hoặc tay+sản phẩm ở phách 2, `flicker` `invert` `blink` ở phách 5 |
| Sản phẩm | 8B – 16B | Cận tuýp/hộp rõ nhãn, chấm kem | `frameflick` ở mốc cắt 8B |
| Các bước | 16B – 48B | Thao tác từng bước, cắt mỗi 4–6B | xen kẽ `maskframe` (grid 3×2 / 2×3 / 3×3) và `frameflick`; `flicker` `glow` mask `sat` lên sản phẩm/kem |
| Kết quả | 48B – 56B | Mặt căng bóng, nháy mắt | 1 `flicker` `glow` |
| CTA | 4–6B cuối | Cầm sản phẩm | chữ CTA "link ở giỏ hàng", 1 `frameflick` trước CTA |
- Mỗi 2–4 phách một hiệu ứng, không chồng 2 hiệu ứng cùng phách; hiệu ứng nhiều nhất ở hook.
- **Không flicker lên mặt người** (mặt trắng xoá/âm bản trông đáng sợ). Flicker lên **sản phẩm**: vật di chuyển theo tay thì thêm `"track": true` (mask theo màu từng khung bằng colorkey, `similarity` 0,07–0,1; lớn hơn sẽ ăn vào vùng da bóng). Máy/chai xanh pastel: `"auto": "pastel_blue"`; da: `"skin"`; vùng sáng: `"bright"`. Mẫu: `projects/skincare/may-xanh-flicker/`.
- Mask: `dark` cho bóng người ngược sáng; footage skincare sáng → thường dùng `sat` (sản phẩm màu đậm, kem, mặt nạ màu) hoặc `box` sát vùng mặt/tay. Luôn đặt `box` chừa nền/sàn, `feather` 3–8.
- Chữ: `hook` hoặc `stack` (small / caps / serif) ở 0–3,3s, `keyword` mỗi bước, `cta` cuối; `caption_style` không cần (không lời). Giữ chữ trong vùng an toàn y 240–1680. Grade `warm`.
- Âm (`sfx.py`, file `sfx.json`): `glitch` sớm 0,05s trước mỗi frameflick, `whoosh`+`click` trước mỗi maskframe, `shutter` ở flicker white, `sparkle` ở cảnh kết quả, `pop` khi keyword hiện. Nhạc `"music": {"src": "music/flicker.mp3", "volume": 0.9}` (không có giọng nên để to; nếu người dùng lồng tiếng thì hạ 0,07–0,12).
- Lệnh:
```bash
S=/home/user/kimhoan/.claude/skills/tiktok-edit-style/scripts
python3 $S/shots.py shots.json -o work/base.mp4   # cắt + chuẩn hoá 1080x1920 → work/base.mp4
python3 $S/sfx.py sfx.json --total <giây> -o work/sfx.wav
python3 $S/render.py plan.json --preview   # kiểm tra nhanh
python3 $S/render.py plan.json             # bản cuối
```

## 4. Kiểm tra trước khi giao
- Tách **từng khung lẻ** đúng mốc mỗi `fx` (`ffmpeg -ss t -frames:v 1`) rồi ghép hstack để xem — ảnh lưới theo fps dễ bỏ sót khung nháy.
- Kiểm: mask không lem ra nền/sàn (đốm trắng), chủ thể nháy rõ, frameflick thấy cảnh sau trong khung, maskframe hiện đủ ô, chữ không đè mặt/sản phẩm, hiệu ứng rơi đúng phách.

## Ảnh bìa (MẶC ĐỊNH — người dùng yêu cầu 18/11/2026)
Không lấy khung hình trong video làm ảnh bìa (người dùng thấy mặt mình trong video xấu). **Luôn dùng ảnh chân dung mặc định**: Drive thư mục "Ảnh bìa mặc định (chân dung Kim Hoàn)" `1M5PlhjmyH3bF-dQ2zQjjMP-jrYGun_Qh` → `portrait-cut-nen-trong.png` `1RbRIaiAHN8-p9jX4JMB3XSONb-OQajTF` (đã tách nền, 1,6MB, tải bằng `download_file_content`), ảnh gốc `portrait-goc.png` `1KfLbnyM7qJQfEPoXL5g03WubN7P-l2iI`. Không commit ảnh này vào repo (repo công khai).
- Dựng bằng `tiktok-edit-style/projects/skincare/thumb/thumb_portrait.py cfg.json` (mẫu: `projects/skincare/may-xanh-flicker/thumb.json`): nền gradient theo màu sản phẩm (`bg`), quầng sáng sau đầu, chữ hook 3 dòng (small / CAPS cam viền trắng / serif nghiêng), bong bóng tròn cắt cảnh sản phẩm từ footage + nhãn tên sản phẩm. Chữ trong vùng y 240–1680.
- Đổi màu nền theo sản phẩm (xanh pastel cho máy xanh, hồng cho máy LED hồng, vàng kem cho mặt nạ vàng…). Không cần logo Kim Hoàn trừ khi người dùng yêu cầu.

## 5. Giao + lưu
- SendUserFile video 1080x1920 + 1 ảnh bìa theo mục "Ảnh bìa" ở trên (ảnh chân dung mặc định, KHÔNG lấy khung video). Kèm timeline ngắn và caption đăng bài (dòng đầu chứa từ khoá tìm kiếm, 1 câu hỏi, "link ở giỏ hàng", 4–5 hashtag).
- Thương hiệu: kênh skincare là kênh affiliate cá nhân — chỉ chèn logo Kim Hoàn nếu người dùng yêu cầu (khi đó theo skill `kimhoan-brand`).
- Commit `shots.json`, `plan.json`, `sfx.json`, kịch bản vào `../tiktok-edit-style/projects/skincare/<sản-phẩm>-flicker/` (không commit video, nhạc, footage); cập nhật bảng "Đã làm" và mốc cảnh mới trong `projects/skincare/README.md`. Tạo nhánh `claude/...`, commit + push; không tạo PR trừ khi người dùng yêu cầu.
