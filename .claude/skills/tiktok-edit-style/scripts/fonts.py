"""Font lookup: skill fonts/ folder -> download from Google Fonts repo -> system fallbacks."""
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")

GF = "https://github.com/google/fonts/raw/main/ofl/"
FONTS = {
    # big italic serif keyword ("newbie", "agent edit video", "3–4 tiếng")
    "serif_italic": ("PlayfairDisplay-Italic.ttf", GF + "playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf", [
        "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
        "C:/Windows/Fonts/georgiai.ttf",
    ]),
    "sans_bold": ("BeVietnamPro-Bold.ttf", GF + "bevietnampro/BeVietnamPro-Bold.ttf", [
        "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]),
    "sans_extrabold": ("BeVietnamPro-ExtraBold.ttf", GF + "bevietnampro/BeVietnamPro-ExtraBold.ttf", [
        "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "C:/Windows/Fonts/ariblk.ttf",
    ]),
    "sans_semibold": ("BeVietnamPro-SemiBold.ttf", GF + "bevietnampro/BeVietnamPro-SemiBold.ttf", [
        "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]),
}


def get(name):
    fname, url, fallbacks = FONTS[name]
    path = os.path.join(FONT_DIR, fname)
    if os.path.exists(path):
        return path
    try:
        os.makedirs(FONT_DIR, exist_ok=True)
        urllib.request.urlretrieve(url, path + ".part")
        os.replace(path + ".part", path)
        return path
    except Exception:
        if os.path.exists(path + ".part"):
            os.remove(path + ".part")
    for f in fallbacks:
        if os.path.exists(f):
            return f
    raise SystemExit(f"Không tìm thấy font cho '{name}'. Đặt file {fname} vào {FONT_DIR}")


if __name__ == "__main__":
    for k in FONTS:
        print(k, "->", get(k))
