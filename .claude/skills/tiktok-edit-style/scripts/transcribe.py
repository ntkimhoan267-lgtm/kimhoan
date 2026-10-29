"""Bước 2: tạo phụ đề theo cụm ngắn (3–6 chữ) từ video đã cắt.

  python transcribe.py cut.mp4 -o captions.json [--model small] [--lang vi]

Cần faster-whisper (pip install faster-whisper) hoặc openai-whisper (pip install openai-whisper).
Không có thì thoát với mã 2: khi đó viết captions.json bằng tay từ kịch bản.
Định dạng: [{"start": 0.0, "end": 1.4, "text": "đối với những bạn newbie"}, ...]
"""
import argparse, json, sys


def decode16k(path):
    """Giải mã bằng ffmpeg (PyAV của faster-whisper lỗi với một số file m4a / mov)."""
    import subprocess
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def words_faster(path, model, lang):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, compute_type="int8")
    segs, _ = m.transcribe(decode16k(path), language=lang, word_timestamps=True, vad_filter=True)
    return [(w.start, w.end, w.word.strip()) for s in segs for w in s.words]


def words_openai(path, model, lang):
    import whisper
    r = whisper.load_model(model).transcribe(path, language=lang, word_timestamps=True)
    return [(w["start"], w["end"], w["word"].strip()) for s in r["segments"] for w in s["words"]]


def chunk(words, max_words, max_dur):
    out, cur = [], []
    for w in words:
        cur.append(w)
        text = w[2]
        if (len(cur) >= max_words or cur[-1][1] - cur[0][0] >= max_dur
                or text.endswith((".", ",", "?", "!", "…"))):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    res = []
    for c in out:
        t = " ".join(w[2] for w in c).strip(" ,.")
        if t:
            res.append(dict(start=round(c[0][0], 2), end=round(c[-1][1], 2), text=t))
    # nối liền các câu để phụ đề không nhấp nháy
    for a, b in zip(res, res[1:]):
        if b["start"] - a["end"] < 0.3:
            a["end"] = b["start"]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--lang", default="vi")
    ap.add_argument("--max-words", type=int, default=6)
    ap.add_argument("--max-dur", type=float, default=2.2)
    a = ap.parse_args()
    words = None
    for fn in (words_faster, words_openai):
        try:
            words = fn(a.video, a.model, a.lang)
            break
        except ImportError:
            continue
    if words is None:
        print("Chưa cài faster-whisper / openai-whisper. Cài: pip install faster-whisper, "
              "hoặc viết captions.json bằng tay.", file=sys.stderr)
        sys.exit(2)
    caps = chunk(words, a.max_words, a.max_dur)
    json.dump(caps, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"{len(caps)} câu phụ đề -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
