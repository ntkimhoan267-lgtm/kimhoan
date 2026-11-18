"""Ảnh bìa skincare mặc định: ảnh chân dung người dùng (đã tách nền) + nền gradient + chữ hook + bong bóng sản phẩm.

  python thumb_portrait.py cfg.json
cfg: {"portrait": "cut.png", "out": "thumb.jpg", "small": "...", "caps": "...", "serif": "...",
      "bg": ["#E6F3FA", "#A9D3EA"], "caps_color": "#E8590C", "ink": "#0B2545",
      "product": {"frame": "f.png", "cx": 385, "cy": 800, "r": 230}, "label": "Halio 5 in 1"}
Ảnh chân dung KHÔNG để trong repo (repo công khai) — lấy từ Drive (xem README skincare), tách nền bằng rembg.
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "fonts")
F = lambda n, s: ImageFont.truetype(os.path.join(FD, n), s)


def hexc(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def fit(text, name, size, maxw):
    while F(name, size).getlength(text) > maxw and size > 30: size -= 2
    return F(name, size)


def main(c):
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    top, bot = map(hexc, c.get("bg", ["#E6F3FA", "#A9D3EA"]))
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], tuple(int(top[i] * (1 - k) + bot[i] * k) for i in range(3)))
    im = im.convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([60, 640, 1020, 1600], fill=(255, 255, 255, 170))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    # chân dung: rộng 1150, đáy chạm mép dưới
    p = Image.open(P(c["portrait"])).convert("RGBA")
    pw = c.get("portrait_w", 1150); ph = int(p.height * pw / p.width)
    p = p.resize((pw, ph), Image.LANCZOS)
    sh = Image.new("RGBA", p.size, (0, 0, 0, 0)); sh.putalpha(p.getchannel("A").point(lambda v: v * 0.25))
    x0, y0 = (W - pw) // 2, H - ph + c.get("portrait_dy", 0)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x0 + 10, y0 + 14))
    im.alpha_composite(p, (x0, y0))
    d = ImageDraw.Draw(im)
    ink = hexc(c.get("ink", "#0B2545"))
    y = 260
    if c.get("small"):
        f = fit(c["small"], "BeVietnamPro-SemiBold.ttf", 56, 960)
        d.text((W // 2, y), c["small"], font=f, fill=ink, anchor="mt"); y += 78
    if c.get("caps"):
        f = fit(c["caps"], "BeVietnamPro-ExtraBold.ttf", 124, 1000)
        d.text((W // 2, y), c["caps"], font=f, fill=hexc(c.get("caps_color", "#E8590C")), anchor="mt",
               stroke_width=8, stroke_fill=(255, 255, 255)); y += f.size + 18
    if c.get("serif"):
        f = F("CormorantGaramond-Italic-VF.ttf", 104)
        try: f.set_variation_by_axes([600])
        except Exception: pass
        d.text((W // 2, y), c["serif"], font=f, fill=ink, anchor="mt", stroke_width=5, stroke_fill=(255, 255, 255))
    if c.get("product"):
        pr = c["product"]; fr = Image.open(P(pr["frame"])).convert("RGB")
        r = pr["r"]; crop = fr.crop((pr["cx"] - r, pr["cy"] - r, pr["cx"] + r, pr["cy"] + r)).resize((300, 300), Image.LANCZOS)
        m = Image.new("L", (300, 300), 0); ImageDraw.Draw(m).ellipse([0, 0, 299, 299], fill=255)
        bub = Image.new("RGBA", (324, 324), (0, 0, 0, 0)); ImageDraw.Draw(bub).ellipse([0, 0, 323, 323], fill=(255, 255, 255, 255))
        bub.paste(crop, (12, 12), m)
        bx, by = pr.get("x", 700), pr.get("y", 1180)
        shb = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(shb).ellipse([bx + 8, by + 14, bx + 332, by + 338], fill=(0, 0, 0, 70))
        im.alpha_composite(shb.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(bub, (bx, by))
        if c.get("label"):
            f = F("BeVietnamPro-ExtraBold.ttf", 46); tw = int(f.getlength(c["label"]))
            lx, ly = bx + 162 - tw // 2 - 30, by + 336
            ImageDraw.Draw(im).rounded_rectangle([lx, ly, lx + tw + 60, ly + 76], 38, fill=ink)
            ImageDraw.Draw(im).text((lx + 30 + tw // 2, ly + 38), c["label"], font=f, fill=(255, 255, 255), anchor="mm")
    im.convert("RGB").save(P(c["out"]), quality=93)
    print("->", P(c["out"]))


if __name__ == "__main__":
    main(json.load(open(sys.argv[1])))
