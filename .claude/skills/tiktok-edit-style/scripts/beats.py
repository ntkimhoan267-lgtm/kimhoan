"""Tìm phách nhạc để cắt cảnh đúng nhịp (montage không lời: quán cà phê, du lịch, outfit).

  python beats.py music.mp3                       # in tempo + mốc phách
  python beats.py music.mp3 -o work/beats.json --every 2 --start 0.5 --end 12

--every N: lấy 1 mốc mỗi N phách (vd 2 = cắt mỗi 2 phách). Kết quả beats.json:
  {"bpm": 128.0, "beats": [...mọi phách...], "cuts": [...mốc nên cắt...]}
Dùng "cuts" làm "until" cho từng cảnh trong shots.json; cảnh có "trans": "whip" thì vết nhoè rơi đúng phách.
Nhịp gợi ý (học từ video mẫu): mở đầu dồn dập 2–4 cảnh cắt mỗi phách (~0,45s), rồi giãn ra mỗi 4 phách (~1,8s)
cho cảnh đẹp / món chính; cảnh cuối giữ lâu nhất.
"""
import argparse, json, subprocess, sys
import numpy as np

SR = 22050
HOP = 256


def onset_env(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = 1024
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::HOP] * np.hanning(n)
    mag = np.log1p(100 * np.abs(np.fft.rfft(frames, axis=1)))
    flux = np.maximum(np.diff(mag, axis=0), 0).sum(axis=1)
    flux = np.concatenate([[0], flux])
    flux -= np.convolve(flux, np.ones(16) / 16, "same")  # bỏ nền chậm
    return np.maximum(flux, 0), len(x) / SR


def tempo(env, lo=70, hi=180):
    fps = SR / HOP
    ac = np.correlate(env, env, "full")[len(env) - 1:]
    lags = np.arange(int(fps * 60 / hi), int(fps * 60 / lo) + 1)
    lag = lags[np.argmax(ac[lags])]
    return 60 * fps / lag, lag


def beat_track(env, lag):
    # chọn pha của lưới phách khớp nhiều đỉnh onset nhất, rồi bám đỉnh gần nhất (±10% chu kỳ)
    phase = max(range(lag), key=lambda p: env[p::lag].sum())
    w = max(1, lag // 10)
    out = []
    for c in range(phase, len(env), lag):
        a, b = max(c - w, 0), min(c + w + 1, len(env))
        out.append(a + int(np.argmax(env[a:b])))
    return np.array(out) * HOP / SR


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("music")
    ap.add_argument("-o", "--out")
    ap.add_argument("--every", type=int, default=1)
    ap.add_argument("--start", type=float, default=0.0, help="bỏ phách trước mốc này (giây trong file nhạc)")
    ap.add_argument("--end", type=float, default=None)
    a = ap.parse_args()
    env, dur = onset_env(a.music)
    bpm, lag = tempo(env)
    beats = [round(float(t), 3) for t in beat_track(env, lag)
             if t >= a.start and (a.end is None or t <= a.end)]
    cuts = beats[::a.every]
    res = dict(bpm=round(bpm, 1), duration=round(dur, 2), beats=beats, cuts=cuts)
    if a.out:
        json.dump(res, open(a.out, "w"), indent=1)
    print(f"{bpm:.1f} BPM, {len(beats)} phách, chu kỳ {60 / bpm:.3f}s", file=sys.stderr)
    print(" ".join(f"{t:.2f}" for t in cuts))


if __name__ == "__main__":
    main()
