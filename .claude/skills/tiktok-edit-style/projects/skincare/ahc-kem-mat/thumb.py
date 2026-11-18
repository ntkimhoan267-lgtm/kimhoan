"""Thumbnail 1080x1920 cho video kem mắt AHC: 3 bản (A gọn, B sơ đồ 3 đường lăn, hookB).

Chạy trong thư mục làm việc có c/266_28.jpg (nền) và c/296_71.1.jpg (ô sản phẩm):
  ffmpeg -ss 28 -i raw/1793381895266.mp4 -frames:v 1 -q:v 2 c/266_28.jpg
  ffmpeg -ss 71.1 -i raw/1793381895296.mp4 -frames:v 1 -q:v 2 c/296_71.1.jpg
  python thumb.py
Toạ độ mũi tên (map_lines) tính theo khung 720x1280 của source; đổi ảnh nền thì đo lại.
Chữ và ô sản phẩm nằm trong y 240–1680 để lưới trang cá nhân TikTok (cắt 3:4) không mất chữ.
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../fonts/")
def font(n, s): return ImageFont.truetype(F + n, s)
W, H, K = 1080, 1920, 1.5

def base():
    im = Image.open('c/266_28.jpg').convert('RGB').resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.08)
    # tối dần phía trên cho chữ nổi
    g = Image.new('L', (1, H)); [g.putpixel((0, y), int(175 * max(0, 1 - y / 900) ** 1.5)) for y in range(H)]
    im.paste(Image.new('RGB', (W, H), (12, 10, 12)), (0, 0), g.resize((W, H)))
    return im.convert('RGBA')

def text(im, xy, s, f, fill, stroke=0, sc='#1A1A1A', anchor='mm', shadow=True):
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0], xy[1] + 6), s, font=f, fill=(0, 0, 0, 150), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(im).text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sc)

def title(im):
    text(im, (W // 2, 315), "Kem mắt mà mình", font("BeVietnamPro-Bold.ttf", 78), "white", 5)
    text(im, (W // 2, 440), "LĂN CẢ MẶT", font("BeVietnamPro-ExtraBold.ttf", 158), "#FFE45C", 9)

def inset(im):
    p = Image.open('c/296_71.1.jpg').convert('RGB')
    p = p.crop((0, 120, 720, 1120)).resize((250, 347), Image.LANCZOS)
    x, y, r = 56, 1320, 30
    m = Image.new('L', p.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *p.size), r, fill=255)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x - 2, y + 10, x + p.width + 2, y + p.height + 14), r, fill=(0, 0, 0, 140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    fr = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(fr).rounded_rectangle((x - 8, y - 8, x + p.width + 8, y + p.height + 8), r + 8, fill="#F6F4F1")
    im.alpha_composite(fr); im.paste(p, (x, y), m)
    f = font("BeVietnamPro-ExtraBold.ttf", 26)
    s = "AHC Pro Shot · Lift 4"
    tw = ImageDraw.Draw(im).textlength(s, font=f)
    cx, cy = x + p.width // 2, y + p.height - 38
    ImageDraw.Draw(im).rounded_rectangle((cx - tw / 2 - 26, cy - 32, cx + tw / 2 + 26, cy + 32), 32, fill="#F8D5DE")
    ImageDraw.Draw(im).text((cx, cy), s, font=f, fill="#5A2233", anchor="mm")

def arrow(d, pts, col=(255, 255, 255, 255), w=9):
    pts = [(x * K, y * K) for x, y in pts]
    seg, on = 26, True   # nét đứt
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L / seg))
        for i in range(n):
            if (i % 2 == 0):
                a, b = i / n, min(1, (i + 1) / n)
                d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=col, width=w)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0); s = 34
    d.polygon([(x1 + 10 * math.cos(ang), y1 + 10 * math.sin(ang)),
               (x1 - s * math.cos(ang - .5), y1 - s * math.sin(ang - .5)),
               (x1 - s * math.cos(ang + .5), y1 - s * math.sin(ang + .5))], fill=col)

def badge(im, xy, n):
    d = ImageDraw.Draw(im); x, y = xy[0] * K, xy[1] * K; r = 36
    d.ellipse((x - r, y - r, x + r, y + r), fill="#FF4F7B", outline="white", width=5)
    d.text((x, y + 2), str(n), font=font("BeVietnamPro-ExtraBold.ttf", 44), fill="white", anchor="mm")

def map_lines(im):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    arrow(d, [(160, 590), (100, 600), (35, 575)], w=11)            # 1 dưới mắt: trong -> ngoài
    arrow(d, [(128, 745), (112, 690), (92, 640)], w=11)            # 2 rãnh cười: đi lên
    arrow(d, [(205, 885), (110, 860), (28, 745)], w=11)            # 3 viền hàm: ra mang tai
    sh = lay.copy(); sh.putalpha(lay.getchannel('A').point(lambda a: a * 0.5))
    im.alpha_composite(Image.merge('RGBA', (*[Image.new('L', im.size, 0)] * 3, sh.getchannel('A'))).filter(ImageFilter.GaussianBlur(6)))
    im.alpha_composite(lay)
    for p, n in [((180, 590), 1), ((150, 752), 2), ((232, 888), 3)]:
        badge(im, p, n)
    text(im, (W // 2 + 30, 588), "3 đường lăn mỗi tối", font("PlayfairDisplay-Italic.ttf", 84), "#F6C9D3", 0)

a = base(); title(a); text(a, (W // 2, 560), "cho mắt · rãnh cười · viền hàm", font("PlayfairDisplay-Italic.ttf", 64), "#F6C9D3"); inset(a)
a.convert('RGB').save('thumb_A.jpg', quality=93)
b = base(); title(b); map_lines(b); inset(b)
b.convert('RGB').save('thumb_B.jpg', quality=93)

def title_b(im):
    text(im, (W // 2, 290), "Cú đêm mà mắt", font("BeVietnamPro-Bold.ttf", 78), "white", 5)
    text(im, (W // 2, 465), "VẪN TƯƠI?", font("BeVietnamPro-ExtraBold.ttf", 158), "#FFE45C", 9)

c = base(); title_b(c); map_lines(c); inset(c)
c.convert('RGB').save('thumb_hookB.jpg', quality=93)
