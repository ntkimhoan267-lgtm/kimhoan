"""Lồng tiếng: làm sạch giọng, lấy mốc từng chữ, tìm chỗ ngắt hơi, xếp giọng lên timeline.

  python voiceover.py clean  voice.m4a -o work/voice_clean.wav
  python voiceover.py words  voice.m4a -o work/words.json [--model large-v3] [--prompt "tên riêng, thương hiệu"]
  python voiceover.py pauses work/voice_clean.wav [--th -45]        # in các khoảng lặng để chọn điểm cắt
  python voiceover.py layout pieces.json -o work/voice_track.wav [--words work/words.json]

pieces.json: các đoạn giọng giữ lại (giây theo file ghi âm gốc) + khoảng nghỉ chèn sau mỗi đoạn:
  {"src": "work/voice_clean.wav", "lead": 0.3, "total": 90,
   "pieces": [{"name": "P1", "in": 1.50, "out": 7.92, "gap": 1.0}, ...]}
  - Bỏ câu đọc vấp / câu nói thêm: chỉ cần không đưa vào pieces.
  - Bỏ một cụm chữ ở cuối câu (vd tên hãng đổi): cho "out" dừng ngay trước chữ đó (xem words.json + pauses).
layout ghi: voice_track.wav (đúng độ dài total), <out>.json (mốc từng đoạn trên timeline) và, nếu có
--words, <out>.words.json: từng chữ với mốc mới "t" để căn keyword / card / hiệu ứng đúng lúc nói.
"""
import argparse, json, os, subprocess, sys, wave
import numpy as np

SR = 48000


def decode(path, sr):
    """Giải mã bằng ffmpeg sang mono float32 (tránh lỗi PyAV của faster-whisper với một số file m4a)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def write_wav(path, x, sr=SR):
    w = wave.open(path, "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def cmd_clean(a):
    # lọc ù, khử ồn nền, bớt đục, thêm rõ, nén cho đều, chuẩn hoá độ to cho mạng xã hội
    af = ("highpass=f=85,afftdn=nf=-42:tn=1,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2.5,"
          "acompressor=threshold=-22dB:ratio=3:attack=8:release=120,loudnorm=I=-15:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.input, "-af", af, "-ar", str(SR), "-ac", "1", a.out],
                   check=True)
    print(f"-> {a.out}", file=sys.stderr)


def cmd_words(a):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Chưa cài faster-whisper: pip install faster-whisper")
    m = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(decode(a.input, 16000), language=a.lang, word_timestamps=True, beam_size=5,
                           initial_prompt=a.prompt or None)
    out = []
    for s in segs:
        out.append(dict(start=round(s.start, 2), end=round(s.end, 2), text=s.text.strip(),
                        words=[dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for w in s.words]))
        print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print(f"-> {a.out}  (whisper hay đặt đầu chữ sớm hơn thực tế; kiểm tra lại bằng 'pauses')", file=sys.stderr)


def envelope_db(x, sr, hop_s=0.01):
    hop = int(sr * hop_s)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), "same")[::hop])
    return 20 * np.log10(rms + 1e-9)


def cmd_pauses(a):
    x = decode(a.input, 16000)
    db = envelope_db(x, 16000)
    th = a.th if a.th is not None else np.percentile(db, 10) + 8
    quiet = db < th
    i, n = 0, len(db)
    print(f"ngưỡng {th:.1f} dB — khoảng lặng ≥ {a.min:.2f}s (điểm cắt tốt nhất = giữa khoảng):")
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) / 100 >= a.min:
                print(f"  {i / 100:7.2f} – {j / 100:7.2f}  ({(j - i) / 100:.2f}s)  cắt ở {(i + j) / 200:.2f}")
            i = j
        else:
            i += 1


def cmd_layout(a):
    spec = json.load(open(a.pieces))
    base = os.path.dirname(os.path.abspath(a.pieces))
    src = spec["src"] if os.path.isabs(spec["src"]) else os.path.join(base, spec["src"])
    v = decode(src, SR)
    t, lay = float(spec.get("lead", 0.3)), []
    for p in spec["pieces"]:
        lay.append(dict(name=p.get("name", f"P{len(lay) + 1}"), raw_in=p["in"], raw_out=p["out"],
                        at=round(t, 3), end=round(t + p["out"] - p["in"], 3)))
        t += p["out"] - p["in"] + p.get("gap", 0.4)
    total = float(spec.get("total") or t)
    if lay[-1]["end"] > total:
        sys.exit(f"Giọng dài {lay[-1]['end']:.2f}s, vượt total {total}s: giảm gap hoặc tăng total")
    track = np.zeros(int(total * SR), np.float32)
    fade = int(0.02 * SR)
    for p in lay:
        seg = v[int(p["raw_in"] * SR):int(p["raw_out"] * SR)].copy()
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        at = int(p["at"] * SR)
        track[at:at + len(seg)] += seg[:len(track) - at]
    write_wav(a.out, track)
    json.dump(dict(total=total, pieces=lay), open(a.out + ".json", "w"), indent=1)
    for p in lay:
        print(f"  {p['name']:5s} {p['at']:6.2f} – {p['end']:6.2f}   (gốc {p['raw_in']:.2f} – {p['raw_out']:.2f})")
    print(f"-> {a.out}  giọng kết thúc {lay[-1]['end']:.2f}s / {total:.2f}s", file=sys.stderr)
    if a.words:
        words = []
        for s in json.load(open(a.words)):
            for w in s["words"]:
                for p in lay:
                    if p["raw_in"] - 0.05 <= w["s"] < p["raw_out"]:
                        words.append(dict(w=w["w"], piece=p["name"], raw=w["s"],
                                          t=round(p["at"] + max(w["s"] - p["raw_in"], 0), 3)))
                        break
        json.dump(words, open(a.out + ".words.json", "w"), ensure_ascii=False, indent=1)
        print(f"-> {a.out}.words.json ({len(words)} chữ)", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("clean"); c.add_argument("input"); c.add_argument("-o", "--out", required=True)
    c.set_defaults(fn=cmd_clean)
    w = sub.add_parser("words"); w.add_argument("input"); w.add_argument("-o", "--out", required=True)
    w.add_argument("--model", default="large-v3"); w.add_argument("--lang", default="vi")
    w.add_argument("--prompt", default=""); w.set_defaults(fn=cmd_words)
    p = sub.add_parser("pauses"); p.add_argument("input"); p.add_argument("--th", type=float, default=None)
    p.add_argument("--min", type=float, default=0.15); p.set_defaults(fn=cmd_pauses)
    l = sub.add_parser("layout"); l.add_argument("pieces"); l.add_argument("-o", "--out", required=True)
    l.add_argument("--words", default=None); l.set_defaults(fn=cmd_layout)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
