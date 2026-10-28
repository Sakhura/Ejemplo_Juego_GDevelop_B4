# Cinemática de transición entre el Nivel 1 y el Nivel 2 (MP4 H.264 + AAC, recomendado por GDevelop).
import sys, math, random, subprocess; sys.path.insert(0, '/home/claude/epe/gen')
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
IMG = '/home/claude/epe/proyecto/assets/img/'; SND = '/home/claude/epe/proyecto/assets/snd/'
OUTV = '/home/claude/epe/proyecto/assets/video/transicion_nivel2.mp4'
W, H, FPS, DUR = 960, 540, 24, 9.0
F = lambda p: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', p)
bos = Image.open(IMG + 'fondo_bosque_5.png').convert('RGBA')
cue = Image.open(IMG + 'fondo_cueva_1.png').convert('RGBA')
portal = [Image.open(IMG + f'portal_abierto_{i}.png').resize((128, 192), Image.NEAREST) for i in range(1, 5)]
lumi_w = [Image.open(IMG + f'lumi_caminar_{i}.png').resize((72, 90), Image.NEAREST) for i in range(1, 5)]
lumi_f = Image.open(IMG + 'lumi_caer.png').resize((72, 90), Image.NEAREST)
lumi_q = Image.open(IMG + 'lumi_quieto_1.png').resize((72, 90), Image.NEAREST)
stars = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.2, 1)) for _ in range(260)]

def texto(im, s, y, size, col, alpha):
    if alpha <= 0: return
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); f = F(size)
    x = (W - d.textlength(s, font=f)) / 2
    for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)]: d.text((x + dx, y + dy), s, font=f, fill=(20, 10, 40, int(255 * alpha)))
    d.text((x, y), s, font=f, fill=col + (int(255 * alpha),))
    im.alpha_composite(lay)

def frame(t):
    if t < 2.4:  # Lumi entra al portal
        im = bos.copy(); im.alpha_composite(portal[int(t * 8) % 4], (700, 284))
        x = int(120 + t / 2.4 * 640)
        if x < 730:
            im.alpha_composite(lumi_w[int(t * 10) % 4], (x, 386))
        glow = max(0, (t - 1.6) / 0.8)
        if glow > 0: im = Image.blend(im, Image.new('RGBA', im.size, (255, 255, 255, 255)), min(1, glow))
        texto(im, 'El portal se abre...', 40, 40, (255, 230, 160), min(1, t / 0.6) * (1 - glow))
        return im
    if t < 5.2:  # túnel mágico
        k = (t - 2.4) / 2.8
        im = Image.new('RGBA', (W, H), (int(30 + 40 * math.sin(t * 3)), 10, 60, 255)); d = ImageDraw.Draw(im)
        for (sx, sy, sp) in stars:
            z = ((t * sp * 0.9) + sp * 3) % 1.0
            r0, r1 = z * 600, (z + 0.06 * sp) * 600
            ang = math.atan2(sy, sx)
            col = (int(150 + 100 * sp), int(120 + 120 * z), 255)
            d.line([(W / 2 + math.cos(ang) * r0, H / 2 + math.sin(ang) * r0), (W / 2 + math.cos(ang) * r1, H / 2 + math.sin(ang) * r1)], fill=col, width=2)
        sc = 0.4 + 0.9 * k; lu = lumi_f.resize((int(72 * sc), int(90 * sc)), Image.NEAREST).rotate(t * 240, expand=True)
        im.alpha_composite(lu, (int(W / 2 - lu.width / 2), int(H / 2 - lu.height / 2)))
        if t < 2.8: im = Image.blend(Image.new('RGBA', im.size, (255, 255, 255, 255)), im, (t - 2.4) / 0.4)
        texto(im, 'Atravesando el velo entre mundos', 470, 30, (220, 200, 255), min(1, (t - 2.6) / 0.5, (5.2 - t) / 0.4))
        return im
    # llegada a la cueva
    k = t - 5.2
    im = cue.copy()
    if k < 0.3: im = Image.blend(Image.new('RGBA', im.size, (255, 255, 255, 255)), im, k / 0.3)
    y = min(386, -90 + k * 900)
    im.alpha_composite(lumi_f if y < 386 else lumi_q, (440, int(y)))
    a = max(0, min(1, (k - 0.8) / 0.6))
    texto(im, 'Capítulo II', 130, 56, (255, 230, 140), a)
    texto(im, 'Las Cavernas de Cristal', 205, 40, (190, 240, 255), a)
    fade = max(0, (t - 8.4) / 0.6)
    if fade > 0: im = Image.blend(im, Image.new('RGBA', im.size, (0, 0, 0, 255)), min(1, fade))
    return im

if __name__ == '__main__':
    # audio: portal + música de la cueva con fundido
    aud = '/tmp/claude-0/-home-claude/7937a689-4a63-51d5-b893-1bc94c5ca2a9/scratchpad/trans_audio.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', SND + 'portal.ogg', '-i', SND + 'musica_cueva.ogg', '-i', SND + 'cristal.ogg',
                    '-filter_complex', '[0]adelay=1500|1500,volume=1.4[a];[0]adelay=3200|3200,volume=0.8[c];[1]atrim=0:6,adelay=4800|4800,afade=t=in:st=4.8:d=1,afade=t=out:st=9.8:d=1.2[b];[2]adelay=5300|5300[d];[a][c][b][d]amix=inputs=4:normalize=0,atrim=0:9',
                    '-ac', '2', aud], check=True)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', aud, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-profile:v', 'main',
                          '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', OUTV], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('ok', p.returncode)
