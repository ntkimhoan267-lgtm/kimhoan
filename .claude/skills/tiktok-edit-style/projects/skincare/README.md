# Dự án Skincare (kênh affiliate TikTok của Kim Hoàn)

Đọc file này TRƯỚC khi xem video: nó thay cho việc tải và xem lại cả thư mục Drive (rất tốn token).

## Source
- Drive: thư mục **Skincare** (`1ENS0hHZ_2rFR0JWNMMoiS_iNpY0rkoWP`), 83 video gốc (đã xoá bản trùng ngày 31/10/2026).
- Danh mục từng video (ID Drive, độ dài, nội dung): [`catalog.md`](catalog.md). ⭐ = source đẹp cho sản phẩm đó.
- Tất cả: cùng một bạn nữ, skincare buổi tối, quay dọc 720x1280 (trừ vài file `own_*`), **không có lời nói** (chỉ tiếng nền) → video dựng bằng chữ + SFX, lồng tiếng nếu người dùng ghi âm.
- File "bản đã đăng" có sẵn chữ POV cháy vào hình → không dùng làm source, chỉ tham khảo giọng văn kênh (POV nhẹ nhàng, "yêu bản thân", "phần thưởng cho làn da").
- Tải: `bash scripts/drive_fetch.sh work/raw <ID>:<tên>.mp4 ...` (cần thư mục đang bật chia sẻ bằng link; tải xong nhắc người dùng tắt). File < 10MB có thể tải bằng `download_file_content` của Drive mà không cần bật chia sẻ.

## Sản phẩm có trong source (số video ≈)
| Sản phẩm | Video | Đã làm |
|---|---|---|
| Kem mắt AHC Pro Shot Colla-Juvenation Lift 4 (tuýp đỏ, đầu massage kim loại chữ T) | ~25 | ✅ `ahc-kem-mat/` (bản A + B) |
| Máy rửa mặt / LED cầm tay màu xanh (ánh đỏ + xanh dương) | ~17 | |
| Đá Gua Sha Lixibox (hồng, hình trái tim) + cảnh lấy từ tủ lạnh | ~8 | |
| Máy LED hồng | ~5 | |
| Mặt nạ: dẻo vàng / xanh ngọc, thạch tím, giấy, xanh dương | ~12 | |
| Kem tay L'Occitane, serum que cho mắt, serum Innisfree | rải rác | |
Tên chính xác trên bao bì: cắt ảnh to (960px) ở khung cầm sản phẩm rồi đọc — chưa đọc được thì hỏi, không đoán.

## Video đã làm: kem mắt AHC (`ahc-kem-mat/`)
- `shots.json` → `scripts/shots.py` (source tải vào `raw/`), `plan.json` (hook A) / `plan_B.json` (hook B) → `scripts/render.py`, `sfx_events.json` → `scripts/sfx.py --total 32`, `thumb.py` → 3 thumbnail.
- 32s, 120 BPM: hook 0–4s cắt + nháy flash mỗi phách → sản phẩm → chấm kem → Bước 1 vùng mắt (trong ra ngoài) → Bước 2 rãnh cười (đi lên) → Bước 3 viền hàm (ra mang tai) → mẹo ấn nhẹ đuôi mắt → da ẩm mướt → CTA "link ở giỏ hàng".
- Hook A "Kem mắt mà mình lăn cả mặt"; hook B "Cú đêm mà mắt vẫn trông tươi? / 3 đường lăn mỗi tối của mình". Đăng cách 2–3 ngày, so tỷ lệ xem 3s đầu + lượt lưu/lượt xem. **Chưa có kết quả — hỏi người dùng bản nào thắng rồi ghi vào đây.**
- Mốc cảnh đẹp (giây trong file source):
  - `…895296` (281s): 70,4 cầm tuýp rõ nhãn · 85,5 chấm kem · 118–145 lăn dưới mắt / đuôi mắt · 150–165 má · 175–195 thái dương
  - `…895303` (30s): 2–4 cạnh mũi/rãnh cười · 14–21 má → viền hàm · 22–28 mặt căng bóng
  - `…895266` (61s): 4 và 15,2 cầm tuýp · 20–46 lăn mắt, má (6–14 là serum que khác, 48+ là máy LED — tránh)
  - `…895310` (14s): mặt căng bóng xoay nhẹ (cảnh kết quả)
  - `…895252` (41s): 0–2 cầm tuýp cạnh mặt

## Đối thủ kem mắt AHC Lift 4 (phụ đề ASR thật trong `ahc-kem-mat/competitors/`)
| Video | Xem / thích / lưu | 3 giây đầu | Bìa |
|---|---|---|---|
| @rinabeauty859 `7506849479174229255` | 552K / 1,9% / 0,45% | "Mắt thâm như này thì bây giờ phải làm như nào?" | "Mắt thâm thì phải làm thế nào?" + sơ đồ vùng mắt |
| @tran_lam18 `7481625312661392648` | 572K / 0,4% / 0,1% | "Mọi người nhất định phải thử em kem mắt này" | "Kem mắt xịn dưới 1M" |
| @trankimdung249 `7516022212361538824` | 111K / 0,7% / 0,07% | "Một ngày lướt điện thoại 10 tiếng…" | "Kem dưỡng mắt dành cho mặt" |
| @diep.lez `7313866645510950162` | 406K / 0,9% / 0,12% | "…có vàng thật hay không?" (kem mắt vàng) | "Kem mắt vàng AHC" |
| @costcosisters `7551805737983380767` | 21,9M (quảng cáo) | partnership + "limited time" | hộp ở Costco |
- Tất cả nói trước camera 60–100s, đọc thành phần (4 collagen, 4 peptide, retinol thực vật). Ý "dùng cho cả mặt" chỉ nhắc ở giây 12–58 → mình đưa lên hook.
- Kiểu nỗi đau + câu hỏi (rinabeauty) tương tác tốt nhất; tránh hứa "hết thâm / nâng cơ 7 ngày" (hãng ghi 4 tuần).
- Lấy số liệu + phụ đề một video TikTok: `curl` trang video, đọc JSON `__UNIVERSAL_DATA_FOR_REHYDRATION__` → `itemStruct.stats`, `desc`, `video.subtitleInfos[].Url` (WebVTT, Source ASR). Không tải được video (chặn bot) — đừng cố vượt.

## Kiểu "flicker" (nhắn `flicker` để làm)
Skill `.claude/skills/flicker/`: video skincare nháy theo vùng kiểu CapCut (Flicker / Frame Flick / Mask Frame), nhạc flicker 145 BPM trong Drive "Nhạc trend Flicker (edit video)" `1GEybjb1Ffnr7ol8R1pVl92yQUTcldg3U`. Video đã làm theo kiểu này:
- `may-xanh-flicker/` — **máy rửa mặt & massage Halio 5 in 1 Ice Blue** (18/11/2026), 33s, hook A "Skincare cả chục bước mà da vẫn xỉn?", có lồng tiếng người dùng (`pieces.json`: giữ giây 19,7–53,5 của file ghi âm, bỏ 2 lần đọc hỏng hook). Source: `518` (`1nr-3GiKvOop4aOGAOiQ7SlHQ04e8bKj_`: 3–10 rửa mặt máy, 12–16 toner/serum, 20–34 đèn đỏ, 36–48 đèn xanh, 49–52 da căng bóng), `550` (`1abQagGkOLXqyiA_b_f16S-LvVM1SLI16`: 2, 10, 12, 32 cầm máy trước mặt), `507` (`1B0RDLWNBwNJg1aEz02tzKbMduJpy984x`: 4–16 rửa có bọt, 41 mặt sau dưỡng), `515` (`1YXLuICcpTGZ4xdsdTqOmhOOzISRa24HK`: 0 mặt).
- Bài học: **không flicker lên mặt** (mặt trắng xoá / âm bản xấu) → flicker lên máy bằng mask `{"auto":"pastel_blue","track":true,"similarity":0.075}` (mask chạy theo từng khung, bám tay di chuyển). Đèn đỏ/xanh dùng `glow` + mask `sat` có `box` vùng mặt (áo ngủ đỏ xanh cũng bão hoà → bắt buộc box). Ảnh bìa lấy khung không có hiệu ứng.

## Ảnh bìa mặc định (mọi video skincare)
Ảnh chân dung người dùng đã tách nền, lưu Drive `1RbRIaiAHN8-p9jX4JMB3XSONb-OQajTF` (thư mục `1M5PlhjmyH3bF-dQ2zQjjMP-jrYGun_Qh`); dựng bằng `thumb/thumb_portrait.py`. Không dùng khung hình trong video làm ảnh bìa.
