"""Bước 1: chuẩn hoá về 1080x1920 và cắt các khoảng lặng (jump cut).

  python cut.py raw.mp4 -o cut.mp4                  # cắt khoảng lặng
  python cut.py raw.mp4 -o cut.mp4 --remove 12.4-13.1 --remove 20-21.5   # cắt thêm chỗ vấp
  python cut.py a.mp4 b.mp4 -o base.mp4 --no-silence   # chỉ ghép + chuẩn hoá (video không lời)

Ghi kèm <out>.json: danh sách đoạn giữ lại (file nguồn, in, out, vị trí trên timeline mới).
"""
import argparse, json, re, subprocess, sys

W, H, FPS = 1080, 1920, 30


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:stream=codec_type,color_transfer",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    streams = j["streams"]
    return dict(
        duration=float(j["format"]["duration"]),
        audio=any(s["codec_type"] == "audio" for s in streams),
        hdr=any(s.get("color_transfer") in ("arib-std-b67", "smpte2084") for s in streams),
    )


def silences(path, noise, min_sil):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-map", "0:a:0",
                          "-af", f"silencedetect=n={noise}dB:d={min_sil}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def keep_ranges(dur, cuts, pad, min_keep):
    ranges, t = [], 0.0
    for s, e in sorted(cuts):
        e = dur if e is None else e
        s2, e2 = s + pad, e - pad
        if e2 <= s2:
            continue
        if s2 - t >= min_keep:
            ranges.append((t, s2))
        t = max(t, e2)
    if dur - t >= min_keep:
        ranges.append((t, dur))
    return ranges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--noise", type=float, default=-35, help="ngưỡng im lặng (dB)")
    ap.add_argument("--min-silence", type=float, default=0.35, help="khoảng lặng tối thiểu để cắt (s)")
    ap.add_argument("--pad", type=float, default=0.08, help="chừa lại trước/sau mỗi câu (s)")
    ap.add_argument("--remove", action="append", default=[], help="cắt thêm a-b (giây, theo file đầu vào đầu tiên)")
    ap.add_argument("--no-silence", action="store_true", help="không cắt khoảng lặng")
    ap.add_argument("--punch", type=float, default=1.08, help="zoom xen kẽ giữa các jump cut (1 = tắt)")
    a = ap.parse_args()

    parts = []  # (input index, in, out)
    for i, path in enumerate(a.inputs):
        info = probe(path)
        cuts = []
        if not a.no_silence and info["audio"]:
            cuts += silences(path, a.noise, a.min_silence)
        if i == 0:
            for r in a.remove:
                s, e = r.split("-")
                cuts.append((float(s) - a.pad, float(e) + a.pad))
        for s, e in keep_ranges(info["duration"], cuts, a.pad if cuts else 0, 0.25):
            parts.append((i, s, e, info))

    has_audio = all(p[3]["audio"] for p in parts)
    tm = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
          "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")
    lines, cat = [], []
    for k, (i, s, e, info) in enumerate(parts):
        z = a.punch if (k % 2 == 1 and a.punch > 1) else 1.0
        zw, zh = int(W * z) // 2 * 2, int(H * z) // 2 * 2
        lines.append(
            f"[{i}:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS,{tm if info['hdr'] else ''}"
            f"scale={zw}:{zh}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={W}:{H},fps={FPS},setsar=1,format=yuv420p[v{k}]")
        cat.append(f"[v{k}]")
        if has_audio:
            d = e - s
            lines.append(f"[{i}:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
                         f"afade=t=in:d=0.01,afade=t=out:st={max(d - 0.015, 0):.3f}:d=0.015[a{k}]")
            cat.append(f"[a{k}]")
    lines.append("".join(cat) + f"concat=n={len(parts)}:v=1:a={1 if has_audio else 0}"
                 + ("[v][a]" if has_audio else "[v]"))
    script = a.out + ".filter.txt"
    open(script, "w").write(";\n".join(lines))

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for p in a.inputs:
        cmd += ["-i", p]
    cmd += ["-filter_complex_script", script, "-map", "[v]"]
    if has_audio:
        cmd += ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", a.out]
    subprocess.run(cmd, check=True)

    t, segs = 0.0, []
    for i, s, e, _ in parts:
        segs.append(dict(src=a.inputs[i], src_in=round(s, 3), src_out=round(e, 3), at=round(t, 3)))
        t += e - s
    json.dump(dict(duration=round(t, 3), segments=segs), open(a.out + ".json", "w"), indent=1, ensure_ascii=False)
    total = sum(probe(p)["duration"] for p in a.inputs)
    print(f"{len(parts)} đoạn, {total:.1f}s -> {t:.1f}s ({a.out})", file=sys.stderr)


if __name__ == "__main__":
    main()
