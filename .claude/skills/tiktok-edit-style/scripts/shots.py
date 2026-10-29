"""Bước 1 (cách 2): dựng base 1080x1920 từ danh sách cảnh, crop dọc theo vị trí khuôn mặt từng cảnh.

  python shots.py shots.json -o work/base.mp4

Dùng khi footage quay NGANG (hoặc cần chọn đúng khung trong khung hình), video không lời / lồng tiếng
sau. Khác cut.py: mỗi cảnh tự chọn đoạn, vị trí crop, tốc độ; render từng cảnh riêng nên không tốn RAM.

shots.json: danh sách cảnh nối tiếp nhau trên timeline:
  [{"src": "raw/IMG_7336.MOV", "in": 0.0, "dur": 3.25, "cx": 0.44},
   {"src": "raw/IMG_7331.MOV", "in": 1.0, "until": 7.72, "cx": 0.55, "speed": 0.8}]
  - "dur" (giây trên timeline) hoặc "until" (mốc kết thúc trên timeline).
  - "cx": tâm crop theo chiều ngang (0 = mép trái, 1 = mép phải). Mặc định 0.5. "cy" tương tự.
  - "speed": < 1 là quay chậm. Bỏ trống thì tự quay chậm khi clip không đủ dài.
  - "zoom": mặc định xen kẽ 1.0 / 1.08 giữa các cảnh để che vết cắt.
Video HDR (iPhone) tự chuyển về SDR, video xoay tự quay đúng chiều. Cảnh không đổi được dùng lại từ cache.
Ghi kèm <out>.json: mốc bắt đầu / thời lượng từng cảnh trên timeline.
"""
import argparse, hashlib, json, os, subprocess, sys

W, H, FPS = 1080, 1920, 30
TM = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")
_probe = {}


def probe(path):
    if path not in _probe:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height,color_transfer:stream_side_data=rotation:format=duration",
                              "-of", "json", path], capture_output=True, text=True, check=True).stdout
        j = json.loads(out)
        st = j["streams"][0]
        w, h = st["width"], st["height"]
        if any(abs(int(d.get("rotation", 0))) == 90 for d in st.get("side_data_list", [])):
            w, h = h, w
        _probe[path] = dict(w=w, h=h, dur=float(j["format"]["duration"]),
                            hdr=st.get("color_transfer") in ("arib-std-b67", "smpte2084"))
    return _probe[path]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--cache", default=None, help="thư mục cache các cảnh (mặc định <out>_segs/)")
    ap.add_argument("--crf", type=int, default=16)
    a = ap.parse_args()
    shots = json.load(open(a.shots))
    base_dir = os.path.dirname(os.path.abspath(a.shots))
    cache = a.cache or os.path.splitext(a.out)[0] + "_segs"
    os.makedirs(cache, exist_ok=True)

    t, listing, segs = 0.0, [], []
    for k, s in enumerate(shots):
        src = s["src"] if os.path.isabs(s["src"]) else os.path.join(base_dir, s["src"])
        info = probe(src)
        dur = s["dur"] if "dur" in s else s["until"] - t
        if dur <= 0.2:
            sys.exit(f"Cảnh {k} ({s['src']}) quá ngắn: {dur:.2f}s")
        si = float(s.get("in", 0))
        speed = s.get("speed") or min(1.0, max(info["dur"] - si - 0.05, 0.1) / dur)
        z = s.get("zoom", 1.08 if k % 2 else 1.0)
        # khung crop 9:16 lớn nhất trong khung gốc, rồi zoom thêm
        if info["w"] / info["h"] > W / H:
            ch = info["h"]; cw = ch * W / H
        else:
            cw = info["w"]; ch = cw * H / W
        cw, ch = cw / z, ch / z
        x = min(max(s.get("cx", .5) * info["w"] - cw / 2, 0), info["w"] - cw)
        y = min(max(s.get("cy", .5) * info["h"] - ch / 2, 0), info["h"] - ch)
        vf = (f"setpts=(PTS-STARTPTS)/{speed:.5f},{TM if info['hdr'] else ''}"
              f"crop={cw:.0f}:{ch:.0f}:{x:.0f}:{y:.0f},scale={W}:{H}:flags=lanczos,"
              f"fps={FPS},setsar=1,format=yuv420p")
        key = hashlib.md5(f"{src}|{si}|{dur:.3f}|{vf}|{a.crf}".encode()).hexdigest()[:12]
        seg = os.path.join(cache, f"{k:03d}_{key}.mp4")
        if not os.path.exists(seg):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{si:.3f}", "-t", f"{dur * speed + 0.3:.3f}",
                            "-i", src, "-an", "-vf", vf, "-t", f"{dur:.3f}", "-c:v", "libx264",
                            "-crf", str(a.crf), "-preset", "medium", "-pix_fmt", "yuv420p", seg], check=True)
        listing.append(f"file '{os.path.abspath(seg)}'")
        segs.append(dict(src=s["src"], src_in=si, at=round(t, 3), dur=round(dur, 3), speed=round(speed, 3)))
        t += dur
    lst = os.path.join(cache, "list.txt")
    open(lst, "w").write("\n".join(listing) + "\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    a.out], check=True)
    json.dump(dict(duration=round(t, 3), segments=segs), open(a.out + ".json", "w"), indent=1, ensure_ascii=False)
    print(f"{len(shots)} cảnh -> {t:.1f}s ({a.out})", file=sys.stderr)


if __name__ == "__main__":
    main()
