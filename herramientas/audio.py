# Efectos de sonido, música incidental y sonidos ambientales sintetizados (originales, sin licencias de terceros).
import numpy as np, subprocess, os, random
SR = 44100
OUT = '/home/claude/epe/proyecto/assets/snd/'
TMP = '/tmp/claude-0/-home-claude/7937a689-4a63-51d5-b893-1bc94c5ca2a9/scratchpad/wav/'
os.makedirs(TMP, exist_ok=True)
rng = np.random.default_rng(3)

def t_(d): return np.arange(int(SR * d)) / SR
def env(n, a=0.005, r=0.1, d=None):
    e = np.ones(n); A = int(SR * a); Rr = int(SR * r)
    if A: e[:A] = np.linspace(0, 1, A)
    if Rr: e[-Rr:] *= np.linspace(1, 0, Rr) ** 2
    return e
def expdec(n, k): return np.exp(-np.arange(n) / SR * k)
def lowpass(x, a):  # filtro de un polo
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
def sweep(f0, f1, d, wave='sq'):
    t = t_(d); f = np.linspace(f0, f1, len(t)); ph = np.cumsum(f) / SR * 2 * np.pi
    return np.sign(np.sin(ph)) if wave == 'sq' else (np.sin(ph) if wave == 'sin' else 2 * ((ph / (2 * np.pi)) % 1) - 1)
def note(freq, d, wave='tri', k=4.0):
    t = t_(d); ph = 2 * np.pi * freq * t
    if wave == 'tri': w = 2 / np.pi * np.arcsin(np.sin(ph))
    elif wave == 'sq': w = np.sign(np.sin(ph)) * 0.6
    elif wave == 'bell': w = np.sin(ph) + 0.4 * np.sin(2.76 * ph) + 0.2 * np.sin(5.4 * ph)
    elif wave == 'pad': w = np.sin(ph) + 0.3 * np.sin(2 * ph + 0.3) + 0.15 * np.sin(3 * ph)
    else: w = np.sin(ph)
    return w * expdec(len(t), k) * env(len(t), 0.004, min(0.05, d / 3))
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def mix_at(buf, x, start):
    i = int(start * SR); j = min(len(buf), i + len(x)); buf[i:j] += x[:j - i]
def norm(x, peak=0.8): return x / (np.max(np.abs(x)) + 1e-9) * peak
def save(name, x, peak=0.8, loop=False):
    x = norm(x, peak)
    if not loop:
        f = min(len(x), int(SR * 0.01)); x[-f:] *= np.linspace(1, 0, f)
    wav = TMP + name + '.wav'
    import wave
    with wave.open(wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '5', OUT + name + '.ogg'], check=True)

def echo(x, delay=0.25, fb=0.35, n=4):
    y = np.concatenate([x, np.zeros(int(SR * delay * n))])
    for k in range(1, n + 1):
        d = int(SR * delay * k); y[d:d + len(x)] += x * fb ** k
    return y

# ---------------- efectos ----------------
def sfx():
    save('salto', sweep(280, 760, 0.16) * env(int(SR * .16), 0.002, 0.08) * 0.5)
    n = rng.standard_normal(int(SR * 0.08))
    save('paso_pasto', lowpass(n, 0.12) * expdec(len(n), 45), 0.5)
    n = rng.standard_normal(int(SR * 0.06))
    save('paso_roca', (lowpass(n, 0.35) + 0.4 * note(180, 0.06, 'sin', 60)) * expdec(len(n), 70), 0.5)
    b = np.zeros(int(SR * 0.6))
    for i, m in enumerate([88, 92, 95, 100]): mix_at(b, note(mtof(m), 0.4, 'bell', 9), i * 0.05)
    save('cristal', b, 0.6)
    b = np.zeros(int(SR * 0.5))
    for i in range(6): mix_at(b, sweep(400 + i * 90, 700 + i * 90, 0.06, 'sin') * env(int(SR * .06), .003, .03), i * 0.06)
    save('pocion', b, 0.6)
    save('herido', sweep(420, 110, 0.32, 'saw') * expdec(int(SR * .32), 5) * 0.6)
    n = rng.standard_normal(int(SR * 0.22))
    save('aplastar', lowpass(n, 0.08) * expdec(len(n), 18) + 0.6 * sweep(200, 60, 0.22, 'sin') * expdec(int(SR * .22), 12), 0.7)
    b = np.zeros(int(SR * 1.4))
    for i, m in enumerate([72, 76, 79, 84, 88]): mix_at(b, note(mtof(m), 1.0, 'bell', 3.5), i * 0.08)
    save('runa', b, 0.6)
    b = np.zeros(int(SR * 1.0))
    for i, (f, d) in enumerate([(392, 0.28), (330, 0.42)]):
        t = t_(d); vib = np.sin(2 * np.pi * 6 * t) * 6
        w = np.sin(2 * np.pi * np.cumsum(f + vib) / SR) * env(len(t), 0.05, 0.15)
        mix_at(b, w + 0.15 * rng.standard_normal(len(t)) * env(len(t), .05, .15) * 0.3, i * 0.35)
    save('buho', b, 0.6)
    d = 1.6; n = rng.standard_normal(int(SR * d)); e = np.sin(np.linspace(0, np.pi, len(n)))
    wh = np.zeros_like(n); acc = 0.0; cut = np.linspace(0.02, 0.4, len(n))
    for i in range(len(n)): acc += cut[i] * (n[i] - acc); wh[i] = acc
    save('portal', wh * e + 0.5 * sweep(200, 1200, d, 'sin') * e, 0.7)
    save('sellado', sweep(110, 90, 0.35, 'sq') * env(int(SR * .35), .005, .1) * 0.4, 0.5)
    b = np.zeros(int(SR * 0.3))
    for i, f in enumerate([2400, 2900]): mix_at(b, note(f, 0.07, 'sin', 30), i * 0.08)
    save('murcielago', b, 0.35)

# ---------------- música ----------------
def song(bars, bpm, chords, melody, wave_mel='tri', wave_arp='tri', mel_oct=0, pad=True, bass=True, arp=True, wet=0.0):
    beat = 60 / bpm; bar = beat * 4; L = bars * bar
    out = np.zeros(int(SR * (L + 2)))
    for b in range(bars):
        root, kind = chords[b % len(chords)]
        tri = [root, root + (3 if kind == 'm' else 4), root + 7]
        if pad:
            for m in tri: mix_at(out, note(mtof(m + 12), bar, 'pad', 0.6) * 0.10, b * bar)
        if bass:
            for k in (0, 2): mix_at(out, note(mtof(root - 12), beat * 1.8, 'tri', 2.5) * 0.35, b * bar + k * beat)
        if arp:
            seq = tri + [tri[1] + 12] + tri[::-1] + [tri[0] + 12]
            for k, m in enumerate(seq): mix_at(out, note(mtof(m + 12), beat * 0.5, wave_arp, 6) * 0.12, b * bar + k * beat / 2)
    tpos = 0.0
    for (m, dur) in melody * (int(L // (sum(d for _, d in melody) * beat)) or 1):
        if tpos >= L: break
        if m is not None: mix_at(out, note(mtof(m + 12 * mel_oct), dur * beat * 1.1, wave_mel, 2.2) * 0.30, tpos)
        tpos += dur * beat
    if wet: out = out[:int(SR * L)] + 0  # mantener largo exacto
    res = out[:int(SR * L)].copy()
    tail = out[int(SR * L):int(SR * (L + 2))]; res[:len(tail)] += tail  # cola envuelta: loop sin cortes
    return res

def musica():
    # Bosque: Do mayor, alegre y aventurera
    ch = [(60, 'M'), (57, 'm'), (65, 'M'), (67, 'M')]
    mel = [(72, 1), (74, .5), (76, .5), (79, 1), (76, 1), (74, 1), (72, .5), (74, .5), (76, 2),
           (77, 1), (76, .5), (74, .5), (72, 1), (69, 1), (71, 1), (72, .5), (74, .5), (67, 2),
           (72, 1), (76, 1), (79, 1.5), (81, .5), (79, 1), (76, 1), (74, 2),
           (72, 1), (74, .5), (72, .5), (69, 1), (71, 1), (72, 4)]
    save('musica_bosque', song(16, 112, ch, mel), 0.7, loop=True)
    # Cueva: La menor, misteriosa
    ch = [(57, 'm'), (53, 'M'), (55, 'M'), (52, 'm')]
    mel = [(69, 2), (72, 1), (71, 1), (69, 2), (64, 2), (65, 2), (67, 1), (65, 1), (64, 4),
           (69, 2), (72, 1), (76, 1), (74, 2), (72, 2), (71, 2), (68, 2), (69, 4)]
    save('musica_cueva', echo(song(16, 84, ch, mel, 'sin', 'bell'), 0.36, 0.3)[:int(SR * 16 * 4 * 60 / 84)], 0.7, loop=True)
    # Menú
    ch = [(62, 'M'), (59, 'm'), (55, 'M'), (57, 'M')]
    mel = [(74, 1.5), (78, .5), (81, 2), (79, 1), (78, 1), (76, 2), (74, 1.5), (76, .5), (78, 1), (71, 1), (74, 4)]
    save('musica_menu', song(8, 96, ch, mel, 'tri', 'bell'), 0.7, loop=True)
    # Victoria (fanfarria) y fin del juego
    b = np.zeros(int(SR * 6))
    for i, (m, d) in enumerate([(67, .2), (72, .2), (76, .2), (79, .6), (76, .2), (79, 1.6)]):
        mix_at(b, note(mtof(m), d + 0.3, 'sq', 2) * 0.5, sum(x[1] for x in [(67, .2), (72, .2), (76, .2), (79, .6), (76, .2), (79, 1.6)][:i]))
    for m in (60, 64, 67, 72): mix_at(b, note(mtof(m), 3, 'pad', 0.8) * 0.2, 1.4)
    save('musica_victoria', b, 0.7)
    b = np.zeros(int(SR * 4))
    for i, m in enumerate([67, 66, 65, 64]): mix_at(b, note(mtof(m - 12), 0.7 if i < 3 else 2.0, 'tri', 1.5) * 0.6, i * 0.45)
    save('musica_gameover', b, 0.7)

def ambientes():
    d = 20
    n = rng.standard_normal(SR * d)
    wind = lowpass(n, 0.01) * (0.6 + 0.4 * np.sin(np.linspace(0, 2 * np.pi * 3, SR * d)))
    rr = random.Random(9)
    for _ in range(14):
        st = rr.uniform(0.5, d - 1); f0 = rr.uniform(2500, 4200)
        for k in range(rr.randint(2, 4)):
            mix_at(wind, sweep(f0, f0 * 1.3, 0.07, 'sin') * env(int(SR * .07), .005, .04) * 0.08, st + k * 0.11)
    save('ambiente_bosque', wind, 0.35, loop=True)
    n = rng.standard_normal(SR * d)
    rum = lowpass(n, 0.004) * 1.5
    for _ in range(22):
        st = rr.uniform(0.3, d - 1); f = rr.uniform(900, 1600)
        mix_at(rum, sweep(f, f * 1.8, 0.05, 'sin') * expdec(int(SR * .05), 60) * 0.25, st)
    save('ambiente_cueva', echo(rum, 0.18, 0.4, 3)[:SR * d], 0.35, loop=True)

if __name__ == '__main__':
    sfx(); musica(); ambientes(); print(sorted(os.listdir(OUT)))
