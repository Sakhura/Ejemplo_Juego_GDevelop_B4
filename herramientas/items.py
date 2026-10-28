# Objetos, plataformas e interfaz.
import sys, math, random; sys.path.insert(0, '/home/claude/epe/gen')
from pix import Canvas, hexc
from PIL import Image, ImageDraw, ImageFont
OUT = '/home/claude/epe/proyecto/assets/img/'
R = random.Random(7)

def cristal(f):
    c = Canvas(12, 16)
    pts = {(x, y) for y in range(16) for x in range(12) if abs(x - 5.5) <= (y + 1) * 0.75 and y < 8 or (y >= 8 and abs(x - 5.5) <= (16 - y) * 0.7)}
    for (x, y) in pts: c.p(x, y, '#2fb8d8' if x > 5 else '#5fe0f0')
    for y in range(2, 14): c.p(5, y, '#bff6ff')
    hl = [(3, 5), (4, 7), (7, 9), (8, 11)][f]
    c.p(*hl, '#ffffff'); c.p(hl[0], hl[1] + 1, '#ffffff')
    c.outline('#123a5a'); return c.out(2)

def pocion(f):
    c = Canvas(12, 14)
    c.rect(4, 0, 7, 1, '#8a5a32'); c.rect(5, 2, 6, 3, '#d8e8f0')
    c.ellipse(5.5, 8.5, 4.6, 4.6, '#e8f4ff')
    c.ellipse(5.5, 9.5, 3.6, 3.4, '#e83a5a' if f == 0 else '#ff5a7a')
    c.p(3, 7, '#ffffff'); c.p(3, 8, '#ffffff')
    c.outline('#2a1020'); return c.out(2)

def runa(active, f=0):
    c = Canvas(14, 22)
    c.rect(1, 19, 12, 21, '#5a5a6a')
    c.ellipse(6.5, 10, 5, 9.5, '#8a8aa0'); c.rect(2, 10, 11, 19, '#8a8aa0')
    c.rect(9, 4, 11, 18, '#6c6c82')
    glow = ('#40f0ff' if f == 0 else '#a0ffff') if active else '#4a4a5a'
    for (x, y) in [(6, 5), (6, 6), (5, 7), (7, 7), (6, 8), (6, 9), (6, 10), (4, 12), (8, 12), (5, 13), (7, 13), (6, 14), (6, 15)]:
        c.p(x, y, glow)
    if active:
        for (x, y) in [(0, 3), (13, 6), (1, 14), (12, 1)]: c.p(x, y, '#a0ffff')
    c.outline('#22222e'); return c.out(2)

def portal(open_, f=0):
    c = Canvas(32, 48)
    c.ellipse(15.5, 18, 15, 17, '#6a6a78'); c.rect(1, 18, 30, 47, '#6a6a78')
    c.ellipse(15.5, 19, 11, 13, '#000000'); c.rect(5, 19, 26, 47, '#000000')
    # interior
    for y in range(6, 48):
        for x in range(4, 28):
            if c.px[x, y][:3] == (0, 0, 0):
                if open_:
                    a = math.atan2(y - 26, x - 15.5); r = math.hypot(x - 15.5, (y - 26) * 0.7)
                    v = (math.sin(a * 3 + r * 0.6 - f * 1.57) + 1) / 2
                    col = (int(90 + 120 * v), int(40 + 60 * v), int(170 + 80 * v), 255)
                else:
                    col = (30, 26, 44, 255)
                c.px[x, y] = col
    for (x, y) in [(3, 12), (28, 12), (2, 30), (29, 30), (15, 1)]:
        c.p(x, y, '#ffd060' if open_ else '#4a4a5a')
    c.rect(0, 46, 31, 47, '#4a4a58')
    c.outline('#1a1424'); return c.out(2)

def destello(f):
    c = Canvas(16, 16)
    r = [2, 4, 6, 7][f]; col = ['#ffffff', '#c0f8ff', '#80e8ff', '#40c0e0'][f]
    for i in range(-r, r + 1):
        c.p(8 + i, 8, col); c.p(8, 8 + i, col)
    if f >= 1:
        d = r // 2 + 1
        for (x, y) in [(8 - d, 8 - d), (8 + d, 8 - d), (8 - d, 8 + d), (8 + d, 8 + d)]: c.p(x, y, col)
    return c.out(2)

def burbuja():
    c = Canvas(14, 14)
    c.ellipse(6.5, 6, 6, 5.5, '#fff8e0'); c.p(5, 12, '#fff8e0'); c.p(4, 13, '#fff8e0')
    c.grid(['xxx', 'x..', 'xx.', 'x..', 'xxx'], {'x': '#3a2410'}, 5, 3)
    c.outline('#3a2410'); return c.out(2)

def tope():
    c = Canvas(8, 16); c.rect(0, 0, 7, 15, '#ff00ff'); return c.out(2)

def suelo_bosque():
    c = Canvas(16, 32)
    c.rect(0, 0, 15, 31, '#6b4426')
    rr = random.Random(1)
    for _ in range(26): c.p(rr.randrange(16), rr.randrange(6, 32), rr.choice(['#5a381e', '#7d5230', '#4c2f18']))
    for (x, y) in [(3, 14), (11, 22), (6, 27)]: c.rect(x, y, x + 1, y, '#8a8a8a')
    c.rect(0, 0, 15, 4, '#4f9a3a'); c.rect(0, 0, 15, 1, '#7cc24f')
    for x in range(0, 16, 3): c.p(x, 5, '#4f9a3a'); c.p(x + 1, 6, '#3c7a2c')
    return c.out(2)

def suelo_cueva():
    c = Canvas(16, 32)
    c.rect(0, 0, 15, 31, '#3a3550')
    rr = random.Random(2)
    for _ in range(30): c.p(rr.randrange(16), rr.randrange(4, 32), rr.choice(['#2e2a42', '#47415f', '#332e48']))
    c.p(4, 12, '#5fe0f0'); c.p(5, 12, '#2fb8d8'); c.p(12, 24, '#c080ff')
    c.rect(0, 0, 15, 2, '#5c5680'); c.rect(0, 0, 15, 0, '#7a74a0')
    return c.out(2)

def tabla():
    c = Canvas(16, 8)
    c.rect(0, 0, 15, 5, '#9a6a3a'); c.rect(0, 0, 15, 0, '#c08a50'); c.rect(0, 5, 15, 5, '#6b4426')
    c.p(2, 2, '#4a2a10'); c.p(13, 2, '#4a2a10'); c.rect(7, 1, 7, 4, '#7a5028')
    c.rect(3, 6, 4, 7, '#6b4426'); c.rect(11, 6, 12, 7, '#6b4426')
    return c.out(2)

def repisa_cristal():
    c = Canvas(16, 8)
    c.rect(0, 0, 15, 4, '#5a5480'); c.rect(0, 0, 15, 0, '#8a84b0')
    for x in (2, 7, 12): c.rect(x, 5, x + 1, 6, '#2fb8d8'); c.p(x, 7, '#5fe0f0')
    return c.out(2)

def deco(nombre):
    if nombre == 'flor':
        c = Canvas(10, 12); c.rect(4, 5, 4, 11, '#3c7a2c'); c.p(5, 8, '#4f9a3a'); c.p(3, 9, '#4f9a3a')
        for (x, y) in [(4, 1), (2, 3), (6, 3), (4, 5), (3, 2), (5, 2)]: c.p(x, y, '#f07ab0')
        c.p(4, 3, '#ffe060'); c.outline('#2a1a20')
    elif nombre == 'hongo_luz':
        c = Canvas(10, 12); c.rect(4, 6, 5, 11, '#e8e0f0'); c.ellipse(4.5, 4.5, 4, 3, '#40e0c0'); c.p(3, 3, '#c0fff0'); c.outline('#14202a')
    elif nombre == 'cartel':
        c = Canvas(20, 20); c.rect(9, 8, 10, 19, '#6b4426'); c.rect(1, 2, 18, 9, '#9a6a3a'); c.rect(1, 2, 18, 2, '#c08a50')
        c.rect(4, 5, 14, 5, '#4a2a10'); c.rect(4, 7, 11, 7, '#4a2a10'); c.p(16, 5, '#4a2a10'); c.p(17, 6, '#4a2a10'); c.p(16, 7, '#4a2a10'); c.outline('#2a1a10')
    elif nombre == 'cristal_grande':
        c = Canvas(16, 20)
        for y in range(20):
            w = int(min(y, 19 - y * 0.2) * 0.5)
            c.rect(8 - w, y, 8 + w, y, '#b070f0' if y % 5 else '#d0a0ff')
        c.rect(7, 2, 7, 18, '#e8d0ff'); c.outline('#2a1440')
    return c.out(2)

def corazon(lleno=True):
    c = Canvas(10, 9)
    c.grid(['.xx...xx.', 'xxxx.xxxx', 'xxxxxxxxx', 'xxxxxxxxx', '.xxxxxxx.', '..xxxxx..', '...xxx...', '....x....'],
           {'x': '#e83a5a' if lleno else '#4a3040'}, 0, 0)
    c.p(1, 1, '#ffb0c0'); c.outline('#2a1020'); return c.out(3)

def panel_dialogo():
    W, H = 760, 150
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, H - 1], 18, fill=(40, 28, 60, 235), outline=(255, 214, 120, 255), width=4)
    d.rounded_rectangle([10, 10, W - 11, H - 11], 12, outline=(140, 100, 200, 255), width=2)
    return im

if __name__ == '__main__':
    for i in range(4): cristal(i).save(OUT + f'cristal_{i+1}.png')
    for i in range(2): pocion(i).save(OUT + f'pocion_{i+1}.png')
    runa(False).save(OUT + 'runa_inactiva.png')
    for i in range(2): runa(True, i).save(OUT + f'runa_activa_{i+1}.png')
    portal(False).save(OUT + 'portal_sellado.png')
    for i in range(4): portal(True, i).save(OUT + f'portal_abierto_{i+1}.png')
    for i in range(4): destello(i).save(OUT + f'destello_{i+1}.png')
    burbuja().save(OUT + 'tecla_e.png'); tope().save(OUT + 'tope.png')
    suelo_bosque().save(OUT + 'suelo_bosque.png'); suelo_cueva().save(OUT + 'suelo_cueva.png')
    tabla().save(OUT + 'plataforma_madera.png'); repisa_cristal().save(OUT + 'plataforma_cristal.png')
    for n in ['flor', 'hongo_luz', 'cartel', 'cristal_grande']: deco(n).save(OUT + f'deco_{n}.png')
    corazon(True).save(OUT + 'hud_corazon.png')
    cristal(0).resize((24, 32), Image.NEAREST).save(OUT + 'hud_cristal.png')
    panel_dialogo().save(OUT + 'panel_dialogo.png')
    print('ok')

def corazon_cristal(state, f=0):
    c = Canvas(28, 40)
    if state != 'dormido':
        r = 13 if f == 0 else 14
        for y in range(40):
            for x in range(28):
                dd = ((x - 13.5) ** 2 + (y - 18) ** 2) ** .5
                if dd < r: c.p(x, y, (255, 220, 255, int(70 * (1 - dd / r))))
    base = {'dormido': ('#5a4a7a', '#7a6a9a', '#9a8ab8'), 'despierto': ('#b070f0', '#d8a8ff', '#ffffff')}[state if state == 'dormido' else 'despierto']
    for y in range(4, 36):
        w = int((y - 4) * 0.55) if y < 18 else int((36 - y) * 0.45)
        for x in range(14 - w, 14 + w + 1): c.p(x, y, base[0] if x > 14 else base[1])
    for y in range(8, 32): c.p(13, y, base[2])
    c.rect(6, 36, 21, 39, '#3a3550')
    return c.out(2)
if __name__ == '__main__':
    corazon_cristal('dormido').save(OUT + 'corazon_dormido.png')
    for i in range(2): corazon_cristal('despierto', i).save(OUT + f'corazon_despierto_{i+1}.png')
    print('corazon ok')
