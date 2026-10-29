"""Bước 3: dựng video hoàn chỉnh từ plan.json (b-roll, card, chữ, phụ đề, nhạc).

  python render.py plan.json [--preview]   # --preview: 540x960, nhanh, để duyệt

Xem examples/plan.example.json và SKILL.md cho định dạng plan.
"""
import argparse, json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fonts  # noqa: E402

W, H, FPS = 1080, 1920, 30

STYLE = dict(
    cream="#F6F4F1",          # nền card
    ink="#2B2B2B",            # chữ tối trên card
    pink="#F6C9D3",           # keyword serif trên video
    pink_line="#EFA3B6",      # gạch chân CTA
    orange="#FF8A2B",         # dòng 2 của hook
    yellow="#FFE45C",         # accent hook
    pills=dict(blue=("#CFE3F7", "#1F3B57"), pink=("#F8D5DE", "#5A2233"),
               yellow=("#FFF0A3", "#4A3D00"), green=("#D6F0D2", "#1E4620")),
)

_font_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(fonts.get(name), size)
    return _font_cache[key]


def wrap(text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(img, cy, text, f, fill, stroke=0, stroke_fill=None, shadow=True, max_w=940, gap=1.18):
    """Vẽ chữ căn giữa theo trục ngang, tâm dọc tại cy. Trả về (top, bottom)."""
    lines = wrap(text, f, max_w)
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * gap)
    top = int(cy - lh * len(lines) / 2)
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(sh)
        for i, ln in enumerate(lines):
            d.text((W / 2, top + i * lh + 3), ln, font=f, fill=(0, 0, 0, 150), anchor="ma",
                   stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        d.text((W / 2, top + i * lh), ln, font=f, fill=fill, anchor="ma",
               stroke_width=stroke, stroke_fill=stroke_fill)
    return top, top + lh * len(lines)


def sparkle(d, cx, cy, r, fill):
    pts = [(cx, cy - r), (cx + r * .25, cy - r * .25), (cx + r, cy), (cx + r * .25, cy + r * .25),
           (cx, cy + r), (cx - r * .25, cy + r * .25), (cx - r, cy), (cx - r * .25, cy - r * .25)]
    d.polygon(pts, fill=fill)


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


# ---------- các kiểu chữ ----------

def make_caption(text, dark=False):
    im = layer()
    if dark:
        text_block(im, int(H * .715), text, font("sans_semibold", 44), STYLE["ink"], shadow=False, max_w=900)
    else:
        text_block(im, int(H * .715), text, font("sans_semibold", 46), "white", shadow=True, max_w=900)
    return im


def make_keyword(o):
    im = layer()
    if o.get("small"):
        text_block(im, int(H * .205), o["small"], font("sans_bold", 46), "white", max_w=960)
    color = {"pink": STYLE["pink"], "white": "white"}.get(o.get("color", "pink"), o.get("color"))
    text_block(im, int(H * .262), o["big"], font("serif_italic", o.get("size", 108)), color, max_w=1000)
    return im


def make_hook(o):
    im = layer()
    l1, l2 = (o["lines"] + [""])[:2]
    text_block(im, int(H * .19), l1, font("sans_extrabold", 90), "white", 6, "#1E2A2A", max_w=1000)
    if l2:
        text_block(im, int(H * .255), l2, font("sans_extrabold", 86), STYLE["orange"], 6, "#3B1D0A", max_w=1000)
    if o.get("accent"):
        f = font("sans_bold", 56)
        top, _ = text_block(im, int(H * .322), o["accent"], f, STYLE["yellow"], 4, "#3B2A00", max_w=900)
        half = f.getlength(o["accent"]) / 2
        d = ImageDraw.Draw(im)
        sparkle(d, W / 2 - half - 42, top + 30, 20, STYLE["yellow"])
        sparkle(d, W / 2 + half + 40, top + 8, 16, "white")
    return im


def make_cta(o):
    im = layer()
    if o.get("top"):
        text_block(im, int(H * .40), o["top"], font("sans_extrabold", 72), "#FFF3B0", 5, STYLE["ink"], shadow=False)
    f = font("serif_italic", 112)
    top, bot = text_block(im, int(H * .465), o["big"], f, STYLE["ink"], shadow=False, max_w=1000)
    half = min(f.getlength(o["big"]), 1000) / 2
    d = ImageDraw.Draw(im)
    d.arc([W / 2 - half, bot - 30, W / 2 + half, bot + 26], 200, 340, fill=STYLE["pink_line"], width=7)
    if o.get("sub"):
        text_block(im, int(H * .54), o["sub"], font("sans_semibold", 40), "#555555", shadow=False, max_w=960)
    return im


def make_card_bg(o):
    """Card nền kem: nhãn pill + khung media (ảnh dán sẵn, video ghép sau) + chữ serif lớn."""
    im = Image.new("RGBA", (W, H), STYLE["cream"])
    d = ImageDraw.Draw(im)
    if o.get("label"):
        bg, fg = STYLE["pills"].get(o.get("color", "blue"), STYLE["pills"]["blue"])
        f = font("sans_bold", 54)
        tw = f.getlength(o["label"])
        y = int(H * .115)
        d.rounded_rectangle([W / 2 - tw / 2 - 24, y - 10, W / 2 + tw / 2 + 24, y + 74], 12, fill=bg)
        d.text((W / 2, y), o["label"], font=f, fill=fg, anchor="ma")
    box = media_box(o)
    if box:
        x, y, bw, bh = box
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([x, y + 10, x + bw, y + bh + 10], 18, fill=(0, 0, 0, 60))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
        src = o.get("media")
        if src and src.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            m = Image.open(src).convert("RGBA")
            im.alpha_composite(m.resize((bw, bh), Image.LANCZOS), (x, y))
    if o.get("big"):
        text_block(im, int(H * o.get("big_y", .64)), o["big"], font("serif_italic", 120), STYLE["ink"],
                   shadow=False, max_w=1000)
    return im


def media_size(src):
    if src.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        return Image.open(src).size
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:stream_side_data=rotation", "-of", "json", src],
                         capture_output=True, text=True, check=True).stdout
    st = json.loads(out)["streams"][0]
    w, h = st["width"], st["height"]
    if any(abs(int(d.get("rotation", 0))) == 90 for d in st.get("side_data_list", [])):
        w, h = h, w
    return w, h


def media_box(o):
    """Khung media đã khớp tỉ lệ ảnh/video, căn giữa trong vùng media_box [x, y, w, h]."""
    if not o.get("media"):
        return None
    x, y, bw, bh = o.get("media_box", [90, int(H * .19), W - 180, int(H * .40)])
    mw, mh = media_size(o["media"])
    sc = min(bw / mw, bh / mh)
    fw, fh = int(mw * sc) // 2 * 2, int(mh * sc) // 2 * 2
    return x + (bw - fw) // 2, y + (bh - fh) // 2, fw, fh


# ---------- dựng ----------

def is_image(p):
    return p.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    plan = json.load(open(a.plan))
    os.chdir(os.path.dirname(os.path.abspath(a.plan)))
    tmp = tempfile.mkdtemp(prefix="tes_")
    base = plan["base"]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                base], capture_output=True, text=True, check=True).stdout)
    overlays = plan.get("overlays", [])
    caps = plan.get("captions", [])
    if isinstance(caps, str):
        caps = json.load(open(caps))
    cards = [o for o in overlays if o["type"] == "card"]

    inputs = [["-i", base]]
    chains = []
    grade = dict(none="null",
                 clean="eq=contrast=1.04:saturation=1.06:brightness=0.01",
                 warm="eq=contrast=1.05:saturation=1.04,colorbalance=rs=0.03:gs=0.01:bs=-0.03",
                 film="eq=contrast=1.08:saturation=0.9,curves=b='0/0.03 1/0.97',vignette=PI/5,noise=alls=3:allf=t",
                 )[plan.get("grade", "clean")]
    chains.append(f"[0:v]{grade},format=yuv420p[c0]")
    cur, n = "c0", 0

    def add_input(args):
        inputs.append(args)
        return len(inputs) - 1

    def push(src_label, start, end, x="0", y="0"):
        nonlocal cur, n
        n += 1
        chains.append(f"[{cur}][{src_label}]overlay=x={x}:y={y}:eval=frame:eof_action=pass:"
                      f"enable='between(t,{start:.3f},{end:.3f})'[c{n}]")
        cur = f"c{n}"

    def png_layer(img, start, end, fade=True, slide=False):
        p = os.path.join(tmp, f"l{len(inputs)}.png")
        img.save(p)
        d = end - start
        k = add_input(["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", p])
        f = f"[{k}:v]format=rgba"
        if fade:
            f += f",fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st={max(d - 0.15, 0):.3f}:d=0.15:alpha=1"
        f += f",setpts=PTS-STARTPTS+{start:.3f}/TB[t{k}]"
        chains.append(f)
        y = f"'if(lt(t-{start:.3f},0.3),28*(1-(t-{start:.3f})/0.3),0)'" if slide else "0"
        push(f"t{k}", start, end, y=y)

    cover = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
    tm = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
          "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")

    for o in overlays:
        s, e = float(o["start"]), float(o["end"])
        if o["type"] == "broll":
            src = o["src"]
            if is_image(src):
                k = add_input(["-loop", "1", "-framerate", str(FPS), "-t", f"{e - s:.3f}", "-i", src])
                z = o.get("zoom", 1.08)  # Ken Burns nhẹ cho ảnh tĩnh
                chains.append(f"[{k}:v]{cover},scale=w='trunc({W}*(1+({z}-1)*t/{e - s:.3f})/2)*2':h=-2:"
                              f"eval=frame,crop={W}:{H},fps={FPS},format=yuv420p,setpts=PTS-STARTPTS+{s:.3f}/TB[b{k}]")
            else:
                k = add_input(["-i", src])
                hdr = "arib-std-b67" in subprocess.run(
                    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
                     "-of", "csv=p=0", src], capture_output=True, text=True).stdout
                si = float(o.get("src_in", 0))
                chains.append(f"[{k}:v]trim={si:.3f}:{si + e - s:.3f},setpts=PTS-STARTPTS,{tm if hdr else ''}{cover},"
                              f"fps={FPS},format=yuv420p,{grade},setpts=PTS+{s:.3f}/TB[b{k}]")
            push(f"b{k}", s, e)
        elif o["type"] == "card":
            p = os.path.join(tmp, f"card{len(inputs)}.png")
            make_card_bg(o).convert("RGB").save(p)
            k = add_input(["-loop", "1", "-framerate", str(FPS), "-t", f"{e - s:.3f}", "-i", p])
            lab = f"k{k}"
            chains.append(f"[{k}:v]format=yuv420p[{lab}]")
            m = o.get("media")
            if m and not is_image(m):
                x, y, bw, bh = media_box(o)
                j = add_input(["-i", m])
                si = float(o.get("src_in", 0))
                chains.append(f"[{j}:v]trim={si:.3f}:{si + e - s:.3f},setpts=PTS-STARTPTS,"
                              f"scale={bw}:{bh}:flags=lanczos,setsar=1[m{j}]")
                chains.append(f"[{lab}][m{j}]overlay=x={x}:y={y}:eof_action=repeat[k{k}m]")
                lab = f"k{k}m"
            chains.append(f"[{lab}]setpts=PTS-STARTPTS+{s:.3f}/TB[cd{k}]")
            push(f"cd{k}", s, e)

    for o in overlays:
        s, e = float(o["start"]), float(o["end"])
        if o["type"] == "keyword":
            png_layer(make_keyword(o), s, e, slide=True)
        elif o["type"] == "hook":
            png_layer(make_hook(o), s, e, slide=True)
        elif o["type"] == "cta":
            png_layer(make_cta(o), s, e, slide=True)
        elif o["type"] == "text":  # chữ tự do: {"text", "y": 0.5, "size": 60, "color": "white", "font": "sans_bold"}
            im = layer()
            text_block(im, int(H * o.get("y", .5)), o["text"], font(o.get("font", "sans_bold"), o.get("size", 60)),
                       o.get("color", "white"), o.get("stroke", 0), o.get("stroke_color", "#000000"))
            png_layer(im, s, e)

    for c in caps:
        s, e = float(c["start"]), float(c["end"])
        on_card = any(float(k["start"]) <= s < float(k["end"]) for k in cards)
        png_layer(make_caption(c["text"], dark=on_card), s, e, fade=False)

    out_size = "540:960" if a.preview else f"{W}:{H}"
    chains.append(f"[{cur}]scale={out_size}:flags=lanczos,format=yuv420p[vout]")

    has_audio = "audio" in subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
                                          "-of", "csv=p=0", base], capture_output=True, text=True).stdout
    amap = []
    mus = plan.get("music")
    if mus:
        k = add_input(["-stream_loop", "-1", "-i", mus["src"]])
        vol = mus.get("volume", 0.12 if has_audio else 0.8)
        chains.append(f"[{k}:a]atrim=0:{dur:.3f},volume={vol},afade=t=in:d=0.5,"
                      f"afade=t=out:st={max(dur - 1.5, 0):.3f}:d=1.5[mus]")
        if has_audio:
            chains.append("[0:a][mus]amix=inputs=2:duration=first:normalize=0[aout]")
        else:
            chains.append("[mus]anull[aout]")
        amap = ["-map", "[aout]"]
    elif has_audio:
        amap = ["-map", "0:a"]

    script = os.path.join(tmp, "graph.txt")
    open(script, "w").write(";\n".join(chains))
    out = plan.get("output", "final.mp4")
    if a.preview:
        out = os.path.splitext(out)[0] + "_preview.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y"] + [x for i in inputs for x in i] + [
        "-filter_complex_script", script, "-map", "[vout]"] + amap + [
        "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "23" if a.preview else "18",
        "-preset", "veryfast" if a.preview else "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(f"-> {out} ({dur:.1f}s)", file=sys.stderr)


if __name__ == "__main__":
    main()
