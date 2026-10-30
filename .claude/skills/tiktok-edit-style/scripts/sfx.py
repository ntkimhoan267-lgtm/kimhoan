"""Hiệu ứng âm thanh chuyển cảnh (tự tổng hợp, không bản quyền) + trộn với giọng thành 1 track.

  python sfx.py events.json -o work/mix.wav --voice work/voice_track.wav --total 90
  python sfx.py --export work/sfx/        # xuất từng âm ra .wav để nghe thử

events.json: [["whoosh", 0.0], ["pop", 0.3], {"sfx": "ding", "t": 13.3, "gain": 1.2}, ...]
Thư viện:
  whoosh  — vút dài 0,45s: card mới, đổi phần lớn (đặt sớm ~0,12s trước mốc)
  swish   — vút ngắn 0,22s: đổi cảnh thường
  pop     — tách nhẹ: chữ keyword hiện ra, nhắc tới "link"
  ding    — chuông: nhãn "Bước n", CTA
  sparkle — lấp lánh: khoảnh khắc "đây rồi", kết quả
  click   — tick giao diện: tick vào checklist, bật công tắc, chữ số đếm
Âm "chói" (tần số cao, làm người xem ngoái lại) — chỉ dùng ở mở đầu và ~1 lần / 7s:
  anvil   — đe kim loại cao, ngân dài: 0–0,3s đầu video, câu chốt gây sốc
  hitech  — chuỗi bíp tăng dần kiểu "biến hình": hiện tiêu đề / ảnh chụp màn hình quan trọng
  glitch  — nhiễu số giật cục: chuyển cảnh flash / glitch
Khi đang có giọng nói, hiệu ứng tự nhỏ lại (x0.6) để không lấn lời. Không có --voice thì chỉ có hiệu ứng.
"""
import argparse, json, os, subprocess, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def bandpass(x, f0, q):
    """Biquad band-pass, tần số trung tâm thay đổi theo từng mẫu."""
    y = np.zeros_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for n in range(len(x)):
        w0 = 2 * np.pi * f0[n] / SR
        al = np.sin(w0) / (2 * q)
        a0 = 1 + al
        yn = (al * x[n] - al * x2 + 2 * np.cos(w0) * y1 - (1 - al) * y2) / a0
        x2, x1, y2, y1 = x1, x[n], y1, yn
        y[n] = yn
    return y


def norm(y):
    return (y / np.abs(y).max()).astype(np.float32)


def whoosh(d=0.45, f_lo=300, f_hi=3500):
    n = int(d * SR)
    t = np.linspace(0, 1, n)
    f = f_lo * (f_hi / f_lo) ** np.sin(np.pi * t / 2)
    return norm(bandpass(rng.standard_normal(n), f, 1.2) * np.sin(np.pi * t) ** 1.5)


def pop():
    t = np.arange(int(0.09 * SR)) / SR
    f = 900 * np.exp(-t * 28) + 260
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(t / 0.002, 1) * np.exp(-t / 0.025))


def ding():
    t = np.arange(int(1.1 * SR)) / SR
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k)
            for f, a, k in [(1568, 1.0, 4.0), (3136, .35, 6.0), (4704, .12, 9.0), (2093, .3, 5.0)])
    return norm(y * np.minimum(t / 0.003, 1))


def sparkle():
    n = int(0.9 * SR)
    y = np.zeros(n)
    for i, f in enumerate([2637, 3136, 3951, 4699, 5274, 3520]):
        st = int((0.02 + i * 0.09 + rng.uniform(0, .03)) * SR)
        t = np.arange(int(0.35 * SR)) / SR
        seg = np.sin(2 * np.pi * f * t) * np.exp(-t * 14) * (0.9 - i * 0.08)
        y[st:st + len(t)] += seg[:n - st]
    return norm(y)


def click():
    t = np.arange(int(0.12 * SR)) / SR
    y = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 90)
    t2 = t[:int(0.06 * SR)]
    y[int(0.045 * SR):int(0.045 * SR) + len(t2)] += 0.7 * np.sin(2 * np.pi * 2100 * t2) * np.exp(-t2 * 110)
    return norm(y)


def anvil():
    t = np.arange(int(1.4 * SR)) / SR
    # bội âm không điều hoà = tiếng kim loại; tần số cao = "chói"
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k)
            for f, a, k in [(2489, 1.0, 3.0), (3951, .7, 4.0), (5588, .45, 5.5), (7244, .3, 7.0), (1245, .25, 3.5)])
    y[:int(0.01 * SR)] += rng.standard_normal(int(0.01 * SR)) * np.linspace(1.5, 0, int(0.01 * SR))
    return norm(y * np.minimum(t / 0.001, 1))


def hitech():
    n = int(0.7 * SR)
    y = np.zeros(n)
    for i in range(12):
        st = int(i * 0.045 * SR)
        t = np.arange(int(0.04 * SR)) / SR
        y[st:st + len(t)] += np.sign(np.sin(2 * np.pi * (1800 + i * 260) * t)) * np.exp(-t * 60) * (0.5 + i / 24)
    return norm(bandpass(y, np.full(n, 4000.0), 0.7) + 0.3 * y)


def glitch():
    n = int(0.32 * SR)
    y = np.zeros(n)
    k = 0
    while k < n:
        L = int(rng.uniform(0.01, 0.035) * SR)
        if rng.random() < 0.7:
            f = rng.choice([900, 1600, 2600, 4200])
            t = np.arange(L) / SR
            y[k:k + L] = (np.sign(np.sin(2 * np.pi * f * t)) * 0.6 + rng.standard_normal(L) * 0.4)[:n - k]
        k += L + int(rng.uniform(0, 0.012) * SR)
    return norm(y)


HOT = {"anvil", "hitech", "glitch"}  # âm chói: tối đa ~1 lần / 7s, nếu không nghe nhức đầu


def library():
    # (âm, mức trộn mặc định so với giọng đã chuẩn hoá -15 LUFS)
    return dict(whoosh=(whoosh(0.45), 0.22), swish=(whoosh(0.22, 800, 5000), 0.10), pop=(pop(), 0.16),
                ding=(ding(), 0.13), sparkle=(sparkle(), 0.12), click=(click(), 0.12),
                anvil=(anvil(), 0.15), hitech=(hitech(), 0.12), glitch=(glitch(), 0.10))


def read(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def write(path, x):
    w = wave.open(path, "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("events", nargs="?")
    ap.add_argument("-o", "--out")
    ap.add_argument("--voice", default=None)
    ap.add_argument("--total", type=float, default=None)
    ap.add_argument("--level", type=float, default=1.0, help="nhân toàn bộ mức hiệu ứng (vd 0.7 = nhỏ hơn)")
    ap.add_argument("--export", default=None, help="xuất từng âm trong thư viện ra thư mục này")
    a = ap.parse_args()
    lib = library()
    if a.export:
        os.makedirs(a.export, exist_ok=True)
        for k, (s, g) in lib.items():
            write(os.path.join(a.export, f"{k}.wav"), s * 0.8)
        print(f"-> {a.export}: {', '.join(lib)}", file=sys.stderr)
        if not a.events:
            return
    if not (a.events and a.out):
        ap.error("cần events.json và -o")
    voice = read(a.voice) if a.voice else np.zeros(0, np.float32)
    total = a.total or (len(voice) / SR if len(voice) else None)
    if not total:
        ap.error("cần --total khi không có --voice")
    mix = np.zeros(int(total * SR) + 2 * SR, np.float32)
    mix[:min(len(voice), len(mix))] += voice[:len(mix)]
    speaking = np.abs(mix) > 1e-3
    last_hot = None
    for ev in sorted(json.load(open(a.events)), key=lambda e: e["t"] if isinstance(e, dict) else e[1]):
        name, t, gain = (ev["sfx"], ev["t"], ev.get("gain", 1.0)) if isinstance(ev, dict) else (ev[0], ev[1], 1.0)
        if name in HOT:
            if last_hot is not None and t - last_hot < 7:
                print(f"! {name} ở {t:.2f}s cách âm chói trước {t - last_hot:.1f}s (<7s) — dễ nhức đầu, cân nhắc đổi "
                      f"sang swish/pop", file=sys.stderr)
            last_hot = t
        s, g = lib[name]
        at = max(int(t * SR), 0)
        duck = 0.6 if speaking[at:at + int(0.3 * SR)].mean() > 0.3 else 1.0
        seg = s * g * gain * duck * a.level
        mix[at:at + len(seg)] += seg[:len(mix) - at]
    mix = mix[:int(total * SR)]
    peak = float(np.abs(mix).max())
    if peak > 0.95:
        mix *= 0.95 / peak
    write(a.out, mix)
    print(f"-> {a.out} ({total:.1f}s, peak {peak:.2f})", file=sys.stderr)


if __name__ == "__main__":
    main()
