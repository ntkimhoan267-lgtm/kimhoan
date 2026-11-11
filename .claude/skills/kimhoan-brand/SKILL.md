---
name: kimhoan-brand
description: Bộ nhận diện thương hiệu cá nhân Kim Hoàn (logo, màu, font) và quy tắc bắt buộc chèn logo khi tạo thumbnail, ảnh OG, banner, ảnh mạng xã hội hoặc edit video cho Kim Hoàn / iamkimhoan.vn. Dùng mỗi khi tạo hay sửa bất kỳ hình ảnh, video nào mang thương hiệu Kim Hoàn. KHÔNG dùng cho TRIP, TriTravel hay thương hiệu khác.
---

# Kim Hoàn brand kit

## Phạm vi

- **Chỉ áp dụng cho thương hiệu cá nhân Kim Hoàn**: website iamkimhoan.vn, blog, thumbnail, video, ảnh mạng xã hội của Kim Hoàn.
- **TRIP là TRIP, Kim Hoàn là Kim Hoàn.** Nội dung của TRIP, TriTravel, Trip Car hay khách hàng khác dùng logo riêng của họ. Không bao giờ chèn logo Kim Hoàn vào đó.

## File logo (trong `assets/` của skill này, bản gốc tại `images/brand/`)

| File | Dùng khi |
|---|---|
| `logo-wordmark.png` | Logo chính "Kim Hoàn." màu navy. Nền sáng. |
| `logo-wordmark-cream.png` | Cùng logo, màu kem. Nền tối hoặc đè lên ảnh/video. |
| `logo-lockup.png` | Logo kèm tagline "AI MARKETING SPECIALIST". Hero, ảnh OG, slide mở đầu video. |
| `logo-mark.png` | Chữ "K." rút gọn. Chỗ rất nhỏ, watermark, avatar. |
| `app-icon.png` | Icon vuông bo góc nền navy. Favicon, avatar kênh. |

Tất cả đều nền trong suốt (PNG RGBA). Không kéo giãn, không đổi màu ngoài hai bản navy/kem, không thêm viền hay bóng.

## Màu và font

- Navy `#0B1F45` · Yellow `#F5B82E` · Ivory `#F8F5EC` · nền kem website `#FDFAF0`
- Tiêu đề: Playfair Display (đậm, nghiêng cho nhấn). Thân: Be Vietnam Pro. Nhãn nhỏ: Space Mono.

## Quy tắc chèn logo

Mỗi ảnh hoặc video mang thương hiệu Kim Hoàn **phải có logo**. Chọn vị trí theo loại:

| Loại | Logo | Vị trí | Kích thước |
|---|---|---|---|
| Thumbnail blog 1200×630 | wordmark navy (nền sáng) / kem (nền tối) | Góc dưới trái, cách trái 64px, cách dưới 40px | Cao 24px |
| Ảnh OG / chia sẻ 1200×630 | lockup (nền sáng) / wordmark kem (nền navy) | Góc trên trái, cách 64–72px | Cao 120px |
| Thumbnail YouTube / video 1280×720 | wordmark kem | Góc trên phải nếu góc dưới trái có chữ, ngược lại góc dưới trái | Cao 3–4% chiều cao ảnh |
| Ảnh vuông / dọc mạng xã hội | wordmark theo nền | Góc dưới trái | Cao 3% chiều cao ảnh |
| Video (watermark) | wordmark kem, mờ 85% | Góc trên phải, cách mép 3% | Rộng 12% chiều rộng video |
| Video (intro / outro) | lockup | Giữa khung, nền kem `#FDFAF0` | Rộng 40% khung |

Giữ nguyên các thành phần sẵn có của ảnh (byline, sticker, chữ). Logo là lớp chèn thêm, không thay thế.

## Cách làm

### Ảnh (Pillow)

```python
from PIL import Image
import numpy as np

def add_logo(img_path, logo_path, h=24, x=64, bottom=40, out=None):
    im = Image.open(img_path).convert("RGB")
    logo = Image.open(logo_path)
    w = int(logo.width * h / logo.height)
    lg = logo.resize((w, h), Image.LANCZOS)
    im.paste(lg, (x, im.height - bottom - h), lg)   # mask = alpha của logo
    im.save(out or img_path, quality=90, optimize=True)

def is_light(img_path, box):
    a = np.array(Image.open(img_path).convert("RGB").crop(box))
    return np.median(a.reshape(-1, 3), axis=0).mean() > 140
```

Lấy mẫu nền ở đúng vùng sẽ đặt logo bằng `is_light`, rồi chọn `logo-wordmark.png` hoặc `logo-wordmark-cream.png`.

### Video (ffmpeg)

Watermark góc trên phải, rộng 12% khung, mờ 85%:

```bash
ffmpeg -i input.mp4 -i .claude/skills/kimhoan-brand/assets/logo-wordmark-cream.png \
  -filter_complex "[1][0]scale2ref=w=iw*0.12:h=ow/mdar[lg][v];[lg]format=rgba,colorchannelmixer=aa=0.85[lg2];[v][lg2]overlay=W-w-W*0.03:H*0.03" \
  -c:a copy output.mp4
```

Intro 2 giây nền kem với lockup ở giữa, ghép trước video:

```bash
ffmpeg -f lavfi -i color=c=0xFDFAF0:s=1920x1080:d=2 -i .claude/skills/kimhoan-brand/assets/logo-lockup.png \
  -filter_complex "[1]scale=768:-1[lg];[0][lg]overlay=(W-w)/2:(H-h)/2" -r 30 -pix_fmt yuv420p intro.mp4
```

### Ảnh OG bằng HTML + Playwright

Viết HTML 1200×630 với font Google ở trên, chèn `<img src="file://.../logo-lockup.png">` cao 120px góc trên trái, chụp bằng Playwright viewport 1200×630. Mẫu đã dùng: `og-image.jpg`, `images/blog-og.jpg`.

## Kiểm tra trước khi lưu

1. Ghép các ảnh vừa tạo thành contact sheet và xem lại bằng mắt.
2. Logo không bị méo, không đè lên chữ hay mặt người, màu đúng với nền.
3. Ảnh dùng trên web thì cập nhật đúng đường dẫn trong HTML, sau đó merge vào `main` để site cập nhật.
