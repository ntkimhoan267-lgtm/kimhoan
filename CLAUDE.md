# Kim Hoàn portfolio — hướng dẫn cho Claude

Website tĩnh (GitHub Pages) tại https://iamkimhoan.vn. Trang chủ `index.html`, blog trong `blog/`, trang dịch vụ visa trong `visa/`. Các thư mục còn lại (ielts, happyflashcard, minigame…) là app riêng, có tên riêng, không dùng logo Kim Hoàn.

## Bộ nhận diện thương hiệu (bắt buộc dùng)

Quy tắc đầy đủ và file logo đóng gói sẵn nằm trong skill `.claude/skills/kimhoan-brand/` (gọi `/kimhoan-brand`). Đọc skill đó trước khi tạo hay sửa bất kỳ ảnh, video nào. Logo Kim Hoàn chỉ dành cho thương hiệu Kim Hoàn, không dùng cho TRIP, TriTravel hay khách hàng khác.

Logo mới nằm trong `images/brand/`. **Luôn dùng các file này, không tự vẽ hay gõ chữ "Kim Hoàn." thay logo.**

| File | Dùng khi |
|---|---|
| `logo-wordmark.png` | Logo chính "Kim Hoàn." màu navy, cho nền sáng (nav, thumbnail nền sáng) |
| `logo-wordmark-cream.png` | Cùng logo, màu kem, cho nền tối (footer navy, thumbnail nền tối, ảnh) |
| `logo-lockup.png` | Logo kèm tagline "AI MARKETING SPECIALIST", cho hero và ảnh chia sẻ OG |
| `logo-mark.png` | Chữ "K." rút gọn, cho chỗ rất nhỏ hoặc watermark |
| `app-icon.png` | Icon vuông bo góc nền navy. Favicon và apple-touch-icon ở thư mục gốc được cắt từ đây |

Màu thương hiệu: Navy `#0B1F45`, Yellow `#F5B82E`, Ivory `#F8F5EC`. Font: Playfair Display (tiêu đề), Be Vietnam Pro (thân), Space Mono (nhãn nhỏ).

## Quy tắc khi tạo hoặc sửa hình ảnh

Mỗi khi tạo ảnh mới cho site (thumbnail blog, ảnh OG, ảnh chia sẻ mạng xã hội, banner, case study, video thumbnail…):

1. **Luôn chèn logo mới** từ `images/brand/`. Chọn bản navy trên nền sáng, bản kem trên nền tối.
2. Thumbnail blog (1200×630): giữ dòng byline "— Kim Hoàn · iamkimhoan.vn" như cũ, chèn thêm wordmark **nhỏ ở góc dưới trái**, cao khoảng 24px, cách mép trái 64px và mép dưới 40px.
3. Ảnh OG (1200×630): dùng `logo-lockup.png` (nền sáng) hoặc `logo-wordmark-cream.png` (nền navy) ở góc trên trái, cao khoảng 120px. Mẫu đã dùng: `og-image.jpg` và `images/blog-og.jpg`.
4. Ảnh ngang không có vùng trống dưới trái (ví dụ video thumbnail): đặt wordmark kem nhỏ ở góc trên phải.
5. Không kéo giãn, không đổi màu logo ngoài hai bản navy/kem, không thêm viền hay bóng.

Cách làm nhanh bằng Pillow: mở ảnh, resize logo theo chiều cao mong muốn với `Image.LANCZOS`, `paste(logo, (x, y), logo)` để giữ nền trong suốt.

## Đăng bài blog

Quy trình đầy đủ nằm trong skill `.claude/skills/kimhoan-blog/` (gọi `/kimhoan-blog`). Đọc skill đó trước khi thêm hay sửa lớn một bài blog: một bài mới phải sửa 6 chỗ (trang bài, thumbnail, `blog/index.html`, dải blog trang chủ, liên kết chéo, `sitemap.xml`).

## Quy tắc chung

- Nội dung song ngữ EN/VI qua `data-en` / `data-vi` trên trang chủ. Thêm văn bản mới thì thêm cả hai.
- Mọi trang HTML đều có bộ favicon trong `<head>`; trang mới phải copy khối đó.
- Sau khi sửa, chụp màn hình bằng Playwright để kiểm tra trước khi push. Site chỉ cập nhật khi merge vào `main`.
