"""Thumbnail series TRIP 'Bắc Kinh không xa' (1080x1920) + nhãn logo TRIP cho video."""
import sys
sys.path.insert(0, '/home/user/kimhoan/.claude/skills/tiktok-edit-style/scripts')
import render as r
from PIL import Image, ImageDraw, ImageEnhance
W, H = 1080, 1920
B = 'brand/'

def badge(h=96):
    """Logo TRIP ngang trên nhãn trắng bo góc (chữ navy đọc được trên nền tối)."""
    lg = Image.open(B + 'trip_ngang_crop.png').convert('RGBA')
    lw = int(lg.width * (h - 28) / lg.height); lg = lg.resize((lw, h - 28), Image.LANCZOS)
    b = Image.new('RGBA', (lw + 44, h), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 0, b.width - 1, h - 1), h // 2, fill=(255, 255, 255, 236))
    b.alpha_composite(lg, (22, 14)); return b

def overlay_logo(path):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); im.alpha_composite(badge(84), (40, 150)); im.save(path)

def cover(bg, cx, out, lines, chips, y=.30, big=False):
    src = Image.open(bg).convert('RGB'); s = H / src.height
    src = src.resize((int(src.width * s), H), Image.LANCZOS)
    x0 = int(min(max(cx * src.width - W / 2, 0), src.width - W)); im = src.crop((x0, 0, x0 + W, H))
    im = ImageEnhance.Contrast(im).enhance(1.06).convert('RGBA')
    g = Image.new('L', (1, H)); [g.putpixel((0, yy), int(165 * max(0, 1 - abs(yy / H - y) / .26) ** 1.2)) for yy in range(H)]
    im.paste(Image.new('RGB', (W, H), (10, 12, 18)), (0, 0), g.resize((W, H)))
    im.alpha_composite(r.make_stack(dict(y=y, lines=lines)))
    for k, (t, c) in enumerate(chips):
        im.alpha_composite(r.make_label(dict(text=t, color=c, y=y + .13 + k * (.075 if big else .062), size=64 if big else 50)))
    bd = badge(110); im.alpha_composite(bd, ((W - bd.width) // 2, int(H * .80)))
    im.convert('RGB').save(out, quality=93)

overlay_logo('brand/logo_overlay.png')
L = lambda t, st='small', **k: dict(text=t, style=st, **k)
cover(B + 'bg1.png', .42, 'brand/thumb_v1.jpg',
      [L('Đi Bắc Kinh 5 ngày'), L('hết bao nhiêu tiền?', 'caps', color='#FFB347', size=78)],
      [('Tự túc ≈ 20 triệu', 'blue'), ('Tour TRIP 13.990.000đ', 'yellow')], big=True)
cover(B + 'bg2.png', .5, 'brand/thumb_v2.jpg',
      [L('Đi Trung Quốc lần đầu'), L('đừng mắc 3 lỗi này', 'caps', color='#FF7A6B', size=78),
       L('kẻo mất toi cả ngày', 'serif', color='#F7C6D9')],
      [('1 · Google, Facebook', 'blue'), ('2 · Chỉ mang tiền mặt', 'yellow'), ('3 · Mua vé tại cổng', 'pink')], y=.26)
cover(B + 'bg3.png', .33, 'brand/thumb_v3.jpg',
      [L('Visa Trung Quốc'), L('5 thứ cần chuẩn bị', 'caps', color='#FFE45C', size=80),
       L('để không bị trả hồ sơ', 'serif', color='#BFE6F7')],
      [], y=.28)
