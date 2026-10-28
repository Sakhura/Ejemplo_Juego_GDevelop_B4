# Fondos: 5 pantallas del Bosque de Lumen + 5 pantallas de las Cavernas de Cristal (continuas entre sí),
# además de las pantallas de menú, fin del juego y victoria.
import sys, math, random; sys.path.insert(0, '/home/claude/epe/gen')
from PIL import Image, ImageDraw, ImageFont
import numpy as np
OUT = '/home/claude/epe/proyecto/assets/img/'
W, H = 480, 270  # se dibuja a media resolución y se escala x2 (estilo pixel art)

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def noise1(x, seed, octs=((0.004, 1), (0.011, 0.5), (0.027, 0.25))):
    v = 0
    for i, (f, a) in enumerate(octs):
        v += a * math.sin(x * f * 6.283 + seed * (i + 1) * 1.7) + a * 0.5 * math.sin(x * f * 13.1 + seed * 3.3 + i)
    return v

def tree(d, x, base, h, col, crown):
    d.rectangle([x - 2, base - h, x + 2, base], fill=col)
    for i in range(3):
        r = h * (0.45 - i * 0.1); cy = base - h - i * h * 0.25 + h * 0.15
        d.ellipse([x - r, cy - r * 0.8, x + r, cy + r * 0.8], fill=crown)

def pine(d, x, base, h, col):
    for i in range(4):
        w = h * (0.35 - i * 0.07); y0 = base - h * (0.25 + i * 0.22)
        d.polygon([(x - w, y0 + h * 0.3), (x + w, y0 + h * 0.3), (x, y0 - h * 0.05)], fill=col)
    d.rectangle([x - 1, base - h * 0.25, x + 1, base], fill=col)

def bosque(screen):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); gx0 = screen * W
    # cielo: de mañana (pantalla 1) a atardecer (pantalla 5)
    for y in range(H):
        for x in range(0, W, 4):
            t = (gx0 + x) / (5 * W)
            top = lerp((110, 180, 240), (70, 60, 140), t); bot = lerp((200, 235, 250), (250, 160, 110), t)
            c = lerp(top, bot, y / H)
            d.line([(x, y), (x + 3, y)], fill=c)
    # sol / luna
    t = (gx0 + 240) / (5 * W)
    sx = 380 - screen * 60; sy = 50 + screen * 18
    d.ellipse([sx - 18, sy - 18, sx + 18, sy + 18], fill=lerp((255, 245, 200), (255, 200, 140), t))
    # nubes
    for gcx in range((gx0 // 130) * 130 - 130, gx0 + W + 130, 130):
        rr = random.Random(gcx * 17)
        cx, cy = gcx - gx0 + rr.randrange(0, 60), rr.randrange(20, 90)
        for k in range(4): d.ellipse([cx + k * 14 - 16, cy - 8 + (k % 2) * 4, cx + k * 14 + 16, cy + 10], fill=lerp((255, 255, 255), (255, 210, 200), t))
    # montañas lejanas (continuas)
    far = lerp((140, 170, 210), (120, 100, 160), t)
    pts = [(x, 130 + 30 * noise1(gx0 + x, 1)) for x in range(0, W + 4, 4)]
    d.polygon(pts + [(W, H), (0, H)], fill=far)
    # colinas medias
    mid = lerp((90, 150, 90), (90, 90, 110), t)
    pts = [(x, 170 + 18 * noise1(gx0 + x, 5)) for x in range(0, W + 4, 4)]
    d.polygon(pts + [(W, H), (0, H)], fill=mid)
    # árboles medios
    rr = random.Random(100 + screen)
    for gx in range((gx0 // 22) * 22, gx0 + W + 30, 22):
        r2 = random.Random(gx)
        if r2.random() < 0.7:
            x = gx - gx0; base = 172 + 18 * noise1(gx, 5) + 6
            pine(d, x, base, r2.randrange(28, 48), lerp((50, 110, 70), (60, 60, 90), t))
    # elementos únicos por pantalla
    near = lerp((40, 90, 50), (50, 45, 70), t)
    if screen == 0:  # aldea con molino
        for hx in (90, 150):
            d.rectangle([hx, 180, hx + 34, 210], fill=(170, 120, 80)); d.polygon([(hx - 4, 180), (hx + 38, 180), (hx + 17, 160)], fill=(150, 60, 50))
            d.rectangle([hx + 13, 194, hx + 21, 210], fill=(90, 60, 40)); d.rectangle([hx + 4, 186, hx + 10, 192], fill=(255, 220, 120))
        d.rectangle([330, 150, 342, 210], fill=(200, 190, 170))
        for a in range(4):
            ang = a * math.pi / 2 + 0.4
            d.line([(336, 156), (336 + 30 * math.cos(ang), 156 + 30 * math.sin(ang))], fill=(120, 90, 60), width=4)
    if screen == 1:  # bosque denso con robles grandes
        for x in (40, 160, 300, 420): tree(d, x, 215, 70, (90, 60, 35), (50, 120, 55))
    if screen == 2:  # cascada y río
        d.rectangle([200, 120, 260, 215], fill=(110, 110, 120))
        for y in range(120, 215, 2):
            for x in range(212, 248, 3):
                if random.Random(x * 7 + y).random() < 0.8: d.point((x, y), fill=(170, 220, 250))
        d.rectangle([150, 205, 320, 216], fill=(120, 190, 230))
        tree(d, 80, 215, 60, (90, 60, 35), (60, 130, 60)); tree(d, 400, 215, 55, (90, 60, 35), (60, 130, 60))
    if screen == 3:  # ruinas y árbol ancestral (hogar del búho)
        for cx in (70, 110, 380):
            d.rectangle([cx, 150, cx + 14, 215], fill=(170, 165, 180)); d.rectangle([cx - 3, 146, cx + 17, 152], fill=(190, 185, 200))
        d.rectangle([95, 140, 125, 146], fill=(190, 185, 200))
        d.rectangle([228, 90, 252, 215], fill=(100, 70, 45))
        for (ox, oy, r) in [(240, 80, 55), (200, 100, 38), (282, 100, 38)]: d.ellipse([ox - r, oy - r * 0.75, ox + r, oy + r * 0.75], fill=(60, 120, 60))
        d.ellipse([234, 150, 246, 164], fill=(40, 25, 15))
    if screen == 4:  # crepúsculo con luciérnagas y arco antiguo
        d.arc([300, 120, 420, 240], 180, 360, fill=(150, 145, 165), width=10)
        d.rectangle([300, 178, 310, 215], fill=(150, 145, 165)); d.rectangle([410, 178, 420, 215], fill=(150, 145, 165))
        rr = random.Random(55)
        for _ in range(30):
            x, y = rr.randrange(W), rr.randrange(100, 210); d.point((x, y), fill=(255, 250, 150)); d.point((x + 1, y), fill=(255, 230, 100))
    # arbustos cercanos (continuos)
    for gx in range((gx0 // 30) * 30, gx0 + W + 40, 30):
        r2 = random.Random(gx * 3)
        x = gx - gx0; r = r2.randrange(12, 22)
        d.ellipse([x - r, 222 - r * 0.7, x + r, 222 + r * 0.7], fill=near)
    d.rectangle([0, 222, W, H], fill=near)
    return im.resize((W * 2, H * 2), Image.NEAREST)

def cueva(screen):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); gx0 = screen * W
    t = screen / 4
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(lerp((20, 16, 36), (30, 18, 40), t), lerp((50, 40, 80), (70, 40, 90), t), y / H))
    # paredes de fondo con textura
    rr = random.Random(screen)
    for _ in range(500):
        x, y = rr.randrange(W), rr.randrange(H); d.point((x, y), fill=(45, 38, 70))
    # estalactitas continuas (techo)
    pts = [(x, 30 + 14 * noise1(gx0 + x, 9)) for x in range(0, W + 4, 4)]
    d.polygon([(0, 0), (W, 0)] + pts[::-1], fill=(35, 30, 55))
    for gx in range((gx0 // 18) * 18, gx0 + W + 18, 18):
        r2 = random.Random(gx + 5)
        x = gx - gx0; top = 30 + 14 * noise1(gx, 9); l = r2.randrange(10, 45)
        d.polygon([(x - 6, top), (x + 6, top), (x, top + l)], fill=(42, 36, 64))
    # roca media continua
    pts = [(x, 190 + 16 * noise1(gx0 + x, 13)) for x in range(0, W + 4, 4)]
    d.polygon(pts + [(W, H), (0, H)], fill=(40, 34, 62))
    # cristales luminosos
    for gx in range((gx0 // 40) * 40, gx0 + W + 40, 40):
        r2 = random.Random(gx * 13)
        if r2.random() < 0.55:
            x = gx - gx0; base = 190 + 16 * noise1(gx, 13) + 4; h = r2.randrange(14, 34)
            col = r2.choice([(90, 220, 240), (180, 120, 250), (240, 120, 200)])
            d.ellipse([x - h * 0.8, base - h * 0.9, x + h * 0.8, base + 6], fill=tuple(int(c * 0.35) for c in col))
            d.polygon([(x - 4, base), (x + 4, base), (x, base - h)], fill=col)
            d.polygon([(x + 3, base), (x + 9, base), (x + 7, base - h * 0.6)], fill=tuple(int(c * 0.8) for c in col))
    if screen == 1:  # lago subterráneo
        d.rectangle([60, 205, 420, 222], fill=(40, 90, 140))
        for x in range(70, 410, 12): d.line([(x, 209), (x + 6, 209)], fill=(90, 160, 210))
    if screen == 2:  # hongos gigantes luminosos
        for (x, h) in [(80, 70), (140, 50), (360, 80)]:
            d.rectangle([x - 4, 220 - h, x + 4, 222], fill=(200, 190, 220))
            d.ellipse([x - 26, 205 - h, x + 26, 230 - h], fill=(60, 200, 170)); d.ellipse([x - 10, 210 - h, x - 2, 216 - h], fill=(180, 255, 230))
    if screen == 3:  # minas abandonadas
        for x in (120, 300):
            d.rectangle([x - 30, 150, x - 24, 222], fill=(110, 75, 45)); d.rectangle([x + 24, 150, x + 30, 222], fill=(110, 75, 45))
            d.rectangle([x - 34, 146, x + 34, 154], fill=(130, 90, 55))
            d.ellipse([x - 4, 158, x + 4, 166], fill=(255, 200, 90))
    if screen == 4:  # sala del Corazón de Cristal
        for r in range(70, 0, -10):
            col = lerp((70, 40, 90), (255, 240, 200), 1 - r / 70)
            d.ellipse([360 - r, 120 - r, 360 + r, 120 + r], fill=col)
        d.polygon([(345, 150), (375, 150), (360, 85)], fill=(200, 150, 255)); d.polygon([(360, 150), (375, 150), (368, 100)], fill=(150, 100, 230))
    d.rectangle([0, 222, W, H], fill=(28, 24, 44))
    return im.resize((W * 2, H * 2), Image.NEAREST)

def titulo_texto(im, texto, y, size, col=(255, 230, 140), sombra=(40, 20, 60)):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', size)
    w = d.textlength(texto, font=f); x = (im.width - w) / 2
    for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (3, 3)]: d.text((x + dx, y + dy), texto, font=f, fill=sombra)
    d.text((x, y), texto, font=f, fill=col)

def menu():
    im = bosque(3).copy()
    ov = Image.new('RGBA', im.size, (20, 10, 40, 110)); im = Image.alpha_composite(im.convert('RGBA'), ov)
    titulo_texto(im, 'LUMI', 60, 96)
    titulo_texto(im, 'y el Corazón de Cristal', 170, 40, (200, 240, 255))
    return im

def gameover():
    im = cueva(0).convert('RGBA'); ov = Image.new('RGBA', im.size, (40, 0, 10, 150)); im = Image.alpha_composite(im, ov)
    titulo_texto(im, 'FIN DEL JUEGO', 150, 72, (255, 120, 120)); return im

def victoria():
    im = cueva(4).convert('RGBA'); ov = Image.new('RGBA', im.size, (40, 30, 0, 60)); im = Image.alpha_composite(im, ov)
    titulo_texto(im, '¡VICTORIA!', 70, 80); titulo_texto(im, 'El bosque vuelve a brillar', 175, 36, (200, 255, 220)); return im

if __name__ == '__main__':
    for i in range(5): bosque(i).save(OUT + f'fondo_bosque_{i+1}.png')
    for i in range(5): cueva(i).save(OUT + f'fondo_cueva_{i+1}.png')
    menu().save(OUT + 'fondo_menu.png'); gameover().save(OUT + 'fondo_gameover.png'); victoria().save(OUT + 'fondo_victoria.png')
    print('ok')
