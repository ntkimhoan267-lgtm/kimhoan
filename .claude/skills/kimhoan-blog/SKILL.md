---
name: kimhoan-blog
description: Quy trình đăng một bài blog mới lên iamkimhoan.vn từ A đến Z — tạo trang bài viết song ngữ VI/EN, thumbnail, SEO (meta, OG, schema), cập nhật trang /blog/, dải blog trang chủ, liên kết chéo, sitemap, kiểm tra bằng Playwright rồi đưa lên main. Dùng mỗi khi được nhờ đăng, thêm, chuyển hay sửa lớn một bài blog trên website Kim Hoàn.
---

# Đăng bài blog trên iamkimhoan.vn

Site là HTML tĩnh trên GitHub Pages, **không có CMS hay bước build**. Mỗi bài là một file HTML viết tay, và danh sách bài được chép tay ở nhiều nơi. Đăng một bài = sửa đúng **6 chỗ** dưới đây. Bỏ sót chỗ nào thì bài vẫn lên nhưng không ai thấy, hoặc chia sẻ lên Facebook bị lỗi ảnh.

Mẫu tham khảo tốt nhất: commit `1c6e23c` (bài "Đi Trung Quốc có cần visa không?"). Chạy `git show 1c6e23c --stat` để xem đủ các file một lần đăng bài phải chạm vào.

## Checklist tổng

| # | Việc | File |
|---|---|---|
| 1 | Tạo trang bài viết | `blog/<slug>/index.html` (mới) |
| 2 | Thumbnail 1200×630 (+ ảnh bìa trong bài nếu có) | `images/thumb-<slug>.jpg` |
| 3 | Thẻ bài ở đầu trang danh sách, tăng số đếm, chuyển nhãn MỚI | `blog/index.html` |
| 4 | Card đầu tiên trong dải blog trang chủ | `index.html` (`#blogCarousel`) |
| 5 | Liên kết chéo: thêm bài mới vào "Bài viết khác" của các bài cũ | `blog/*/index.html` |
| 6 | Thêm URL vào sitemap, cập nhật `lastmod` của `/blog/` | `sitemap.xml` |

Sau đó: kiểm tra → commit → push → PR → merge vào `main` (site chỉ cập nhật khi vào `main`).

---

## 0. Chuẩn bị nội dung

Trước khi viết HTML, chốt các thông tin sau (hỏi Kim Hoàn nếu thiếu):

- **Slug**: chữ thường, không dấu, nối bằng gạch ngang, chứa từ khoá chính. Ví dụ `di-trung-quoc-co-can-visa-khong`. URL cuối: `https://iamkimhoan.vn/blog/<slug>/`.
- **Tiêu đề VI + EN**, **mô tả ngắn VI + EN** (1–2 câu), **chuyên mục** (VD: Hướng dẫn Visa / Visa Guide, Câu chuyện / Personal Story, AI).
- **Ngày đăng** (định dạng hiển thị `dd.mm.yyyy`, trong meta/schema `yyyy-mm-dd`) và **số phút đọc** (~200 từ tiếng Việt/phút).
- **Từ khoá SEO** chính và phụ.
- Tác giả luôn là **Nguyễn Thị Kim Hoàn**.

**Nếu bài gốc viết cho TRIP / TriTravel / khách hàng khác**: bỏ hết phần thuộc thương hiệu đó — tên tác giả khác, mục giới thiệu dịch vụ, giá tour, địa chỉ văn phòng, link nội bộ sang site của họ (sẽ thành link chết). Thay CTA bằng link về trang của site này (bài visa → `/visa/`). Giữ lại phần có giá trị thật cho người đọc.

## 1. Tạo trang bài viết `blog/<slug>/index.html`

**Copy nguyên file của bài mới nhất** (`blog/di-trung-quoc-co-can-visa-khong/index.html`) rồi thay nội dung. Không viết lại từ đầu, không đổi CSS chung — giữ giao diện đồng bộ giữa các bài.

### `<head>` — phải thay hết

- `<title>`, `meta description` (~150–160 ký tự, có từ khoá), `meta keywords`, `meta author`.
- `<link rel="canonical" href="https://iamkimhoan.vn/blog/<slug>/">`
- Open Graph: `og:title`, `og:description`, `og:image` = `https://iamkimhoan.vn/images/thumb-<slug>.jpg` (**URL tuyệt đối**), `og:url`, `og:type=article`, `og:locale=vi_VN`, `article:published_time`, `article:author`, `article:section`.
- Twitter: `twitter:card=summary_large_image`, title, description, image.
- **Schema JSON-LD `BlogPosting`**: headline, description, image, datePublished, dateModified, inLanguage `vi-VN`, articleSection, author/publisher (Person, Nguyễn Thị Kim Hoàn, `https://iamkimhoan.vn/`), mainEntityOfPage = URL bài.
- **Schema `FAQPage`** nếu bài có mục FAQ — câu hỏi/đáp án phải khớp đúng nội dung FAQ hiển thị trong bài.
- **Bộ favicon** (bắt buộc, copy nguyên khối):
  ```html
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  ```

### Song ngữ trong bài viết

Trong các trang blog, song ngữ dùng **cặp span**, không dùng `data-en/data-vi` như trang chủ:

```html
<span class="vi">Câu tiếng Việt</span>
<span class="en">English sentence</span>
```

- Mọi đoạn văn bản người đọc thấy đều phải có đủ cặp `vi` + `en` — số lượng `class="vi"` và `class="en"` trong file phải **bằng nhau**.
- Trong `<script>` cuối file, cập nhật hai chuỗi `document.title` trong hàm `toggleLang()` (bản EN và bản VI).
- Mặc định trang mở bằng tiếng Việt (`<html lang="vi">`, nút VI active).

### Cấu trúc trang (giữ thứ tự)

1. `#progress-bar` + `nav` — logo `images/brand/logo-wordmark.png` (không gõ chữ thay logo), link "← Tất cả bài viết", nút đổi ngôn ngữ.
2. `header.article-hero` — `kicker` (chuyên mục), `h1.article-title`, `p.article-subtitle`, `article-meta` (avatar `/hero.jpg`, tên tác giả, phút đọc, ngày `dd.mm.yyyy`, chuyên mục).
3. `article.article-body`:
   - `figure.cover` — ảnh bìa 1200×630, có `alt` chứa từ khoá, `figcaption` song ngữ.
   - `div.toc` — mục lục, mỗi mục trỏ `#id` của một `h2`.
   - Nội dung với `h2 id="..."` (id không dấu). Các khối có sẵn để dùng: `answer-box` (câu trả lời ngắn ngay đầu bài — tốt cho SEO), `highlight-box`, `table-wrap > table` (**bảng luôn bọc trong `.table-wrap`** để không tràn ngang trên điện thoại), `figure`, `inline-photo`, `inline-cta`, `divider`, `tag-row`.
   - Sơ đồ đơn giản: vẽ SVG nội tuyến, nhãn dùng font Be Vietnam Pro để dấu tiếng Việt hiện đúng.
   - FAQ dùng `<details class="faq"><summary>…</summary><div class="faq-answer">…</div></details>` (đáp án nằm sẵn trong HTML cho Google đọc).
4. `div.sources` — nguồn tham khảo (bài có số liệu/chính sách), link ngoài có `target="_blank" rel="noopener"`.
5. `div.disclaimer` — với bài chính sách/visa: "Cập nhật ngày …" + khuyến nghị kiểm tra nguồn chính thức.
6. `div.article-cta` — hộp CTA cuối bài (bài visa → `/visa/`).
7. `div.related` — "Bài viết khác": 2 thẻ `related-card` trỏ tới bài liên quan.
8. `footer` + `<script>` (đổi ngôn ngữ, thanh tiến độ, hiện dần khi cuộn) — giữ nguyên, chỉ sửa `document.title`.

Link nội bộ dùng đường dẫn tuyệt đối từ gốc và có `/` cuối: `/blog/<slug>/`, `/visa/`.

## 2. Thumbnail và ảnh trong bài

**Đọc skill `kimhoan-brand` trước khi làm ảnh.** Tóm tắt quy cách thumbnail hiện tại (xem các file `images/thumb-*.jpg` làm mẫu):

- Kích thước **1200×630**, JPG, lưu tại `images/thumb-<slug>.jpg`. Ảnh này dùng cho cả og:image, thẻ ở `/blog/` và card trang chủ.
- Bố cục: ảnh chân dung Kim Hoàn tách nền bên phải; bên trái là nhãn chuyên mục (pill vàng, Space Mono), tiêu đề ngắn bằng Playfair Display (chữ nhấn in nghiêng vàng), byline **"— Kim Hoàn · iamkimhoan.vn"**. Mỗi bài một màu nền/ảnh nền theo chủ đề.
- **Bắt buộc chèn wordmark nhỏ góc dưới trái**: cao ~24px, cách trái 64px, cách dưới 40px; bản navy trên nền sáng, bản kem (`logo-wordmark-cream.png`) trên nền tối.
- Ảnh bìa trong bài (nếu khác thumbnail): 1200×630, đặt tên mô tả có từ khoá (VD `images/tu-cam-thanh-mua-dong.jpg`), nén gọn (< ~150KB).
- Ảnh của TRIP / khách hàng khác: không chèn logo Kim Hoàn.

## 3. Trang danh sách `blog/index.html`

- Thêm một thẻ `<a href="/blog/<slug>/" class="post fade-up">` **lên đầu** `<main class="list">`, copy cấu trúc thẻ đang ở đầu: `img.post-thumb` (thumb-<slug>.jpg, width 240 height 126, `loading="lazy"`), `post-chip`, `post-date` (`dd.mm.yyyy · X phút đọc`), `h2.post-title`, `p.post-desc`, `post-more` — tất cả song ngữ bằng cặp span.
- Thẻ mới mang class `post-chip new` (nhãn màu mint). **Bỏ `new`** khỏi thẻ trước đó — chỉ một bài được đánh dấu mới.
- Tăng số đếm trong `div.count` (cả "N bài viết" và "N posts").

## 4. Dải blog trang chủ `index.html`

Trong `section#blog` → `div#blogCarousel`, thêm card mới **ở đầu**, copy cấu trúc card hiện có:

```html
<a href="/blog/<slug>/" class="post">
  <div class="post-thumb"><img src="/images/thumb-<slug>.jpg" alt="" loading="lazy" draggable="false"></div>
  <div class="post-body">
    <div class="post-meta" data-en="8 min read · Visa guide" data-vi="8 phút đọc · Hướng dẫn visa">8 min read · Visa guide</div>
    <h3 data-en="English title" data-vi="Tiêu đề tiếng Việt">English title</h3>
    <p data-en="English teaser" data-vi="Mô tả tiếng Việt">English teaser</p>
    <div class="post-more" data-en="Read article →" data-vi="Đọc bài viết →">Read article →</div>
  </div>
</a>
```

Trang chủ dùng `data-en` / `data-vi` (text mặc định bên trong thẻ là bản EN). Ký tự `&` viết thành `&amp;`. Dải hiện giữ khoảng 4 bài mới nhất; nếu dài quá thì bỏ card cũ nhất (bài vẫn còn ở `/blog/`).

## 5. Liên kết chéo

- Thêm một `related-card` trỏ tới bài mới vào mục "Bài viết khác" của các bài cũ (ít nhất các bài cùng chủ đề; lần đăng gần nhất đã thêm vào cả 4 bài cũ), đặt lên đầu `related-grid`.
- Trong thân bài mới, nếu hợp ngữ cảnh, chèn 1 link tự nhiên sang bài liên quan cũ.

## 6. `sitemap.xml`

```xml
<url>
  <loc>https://iamkimhoan.vn/blog/<slug>/</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.9</priority>
</url>
```

Đặt cạnh các bài khác (bài mới nhất phía trên). Cập nhật `lastmod` của `https://iamkimhoan.vn/blog/` thành ngày đăng; nếu sửa trang chủ thì cập nhật `lastmod` của `/` luôn. Bài hướng dẫn/SEO dùng priority 0.9, bài cá nhân 0.7–0.8.

---

## 7. Kiểm tra trước khi push

Chạy server tĩnh từ gốc repo (`python3 -m http.server 8000`) rồi kiểm tra bằng Playwright:

1. **Chụp màn hình** bài mới ở 375px, 768px, 1280px; chụp `/blog/` và dải blog trang chủ. Xem bằng mắt: thumbnail hiện đúng, logo không méo.
2. **Không tràn ngang**: `document.documentElement.scrollWidth <= innerWidth` ở cả 3 kích thước.
3. **Không lỗi JS** trên bài mới, `/blog/`, trang chủ và các bài cũ vừa sửa (bắt `pageerror` / `console.error`).
4. **Nút đổi ngôn ngữ** chạy: bấm sang EN thì không còn chữ tiếng Việt lộ ra, title đổi theo.
5. **Song ngữ cân**: đếm `class="vi"` = `class="en"` trong file bài mới.
6. **Link nội bộ** (`href="/..."`) đều trỏ tới file có thật; mọi `href="#id"` trong mục lục có `id` tương ứng.
7. **JSON-LD hợp lệ**: `JSON.parse` từng khối `application/ld+json`.
8. Ảnh og:image tồn tại đúng đường dẫn, đúng 1200×630.

## 8. Đưa lên site

1. Làm trên nhánh riêng (không commit thẳng `main`).
2. Commit message tiếng Việt, dòng đầu dạng: `Thêm bài "<tiêu đề>" tại /blog/<slug>/`. Thân commit ghi: đã bỏ/sửa gì so với bản gốc, các chỗ đã tích hợp (danh sách, trang chủ, liên kết chéo, sitemap), và kết quả kiểm tra ở bước 7.
3. Push nhánh, tạo PR vào `main`. **Bài chỉ lên iamkimhoan.vn sau khi PR được merge** (GitHub Pages tự cập nhật sau 1–2 phút).
4. Sau khi lên: mở `https://iamkimhoan.vn/blog/<slug>/`, dán link vào Facebook Sharing Debugger để làm mới ảnh chia sẻ nếu cần.

## Lỗi hay gặp

- Quên đổi `og:image` / `canonical` / `og:url` → chia sẻ ra link hoặc ảnh của bài cũ.
- og:image dùng đường dẫn tương đối → Facebook/Zalo không hiện ảnh.
- Thêm đoạn văn chỉ có tiếng Việt → bấm EN bị trống hoặc lộ tiếng Việt.
- Bảng không bọc `.table-wrap` → tràn ngang trên điện thoại.
- Để hai bài cùng nhãn MỚI, hoặc quên tăng số đếm "N bài viết".
- Gõ chữ "Kim Hoàn." thay cho file logo, hoặc chèn logo Kim Hoàn vào nội dung của TRIP.
