# Personajes: Lumi (avatar), Hongo Gruñón, Murciélago Sombrío, Sabio Búho Orión.
import sys; sys.path.insert(0, '/home/claude/epe/gen')
from pix import Canvas
OUT = '/home/claude/epe/proyecto/assets/img/'
S = 3  # escala de personajes

# ---------- Lumi, espíritu del bosque (16x20, mira a la derecha) ----------
def lumi(pose='idle', f=0):
    c = Canvas(16, 20)
    bob = 0
    if pose == 'idle': bob = 1 if f == 1 else 0
    if pose == 'walk': bob = 1 if f in (1, 3) else 0
    # bufanda roja que flamea hacia atrás
    sw = {'idle': [0, 1][f % 2], 'walk': [0, 1, 0, 1][f % 4], 'jump': 1, 'fall': 0, 'hurt': 0}[pose]
    c.rect(2, 10 + bob, 5, 11 + bob, '#d8452e')
    c.rect(1, 11 + bob + sw, 3, 12 + bob + sw, '#b8321f')
    # piernas / botas
    legs = {
        'idle': [(6, 7), (9, 10)], 'jump': [(5, 6), (9, 10)], 'fall': [(6, 7), (10, 11)], 'hurt': [(6, 7), (9, 10)],
    }
    if pose == 'walk':
        L = [[(5, 6), (10, 11)], [(6, 7), (9, 10)], [(7, 8), (8, 9)], [(6, 7), (9, 10)]][f % 4]
    else:
        L = legs[pose]
    ly = 16 + (0 if pose != 'jump' else -1)
    for (a, b) in L:
        c.rect(a, ly, b, ly + 1, '#6b4426')
        c.rect(a, ly + 2, b + 1, ly + 2, '#3e2614')
    # cuerpo / túnica
    c.rect(5, 9 + bob, 10, 15, '#2f7a3a')
    c.rect(5, 13, 10, 13, '#7a4a22')   # cinturón
    c.p(8, 13, '#e9c44a')                # hebilla
    c.rect(6, 9 + bob, 9, 9 + bob, '#3f9a4a')
    c.p(8, 10 + bob, '#ffe680')          # colgante luminoso
    # brazos
    arm_y = 10 + bob if pose not in ('jump', 'hurt') else 8 + bob
    c.rect(4, arm_y, 4, arm_y + 2, '#f2d3b0')
    c.rect(11, arm_y, 11, arm_y + 2, '#f2d3b0')
    # capucha
    c.ellipse(8, 5 + bob, 4.6, 4.3, '#3f9a4a')
    c.rect(4, 6 + bob, 4, 9 + bob, '#2f7a3a')
    c.p(7, 0 + bob, '#8fd16a'); c.p(8, 0 + bob, '#8fd16a'); c.p(9, 1 + bob, '#8fd16a')  # hoja en la punta
    c.p(8, 1 + bob, '#5cb64a')
    # cara
    c.rect(7, 4 + bob, 11, 7 + bob, '#f6dcc0')
    c.p(12, 5 + bob, '#f6dcc0')
    if pose == 'hurt':
        c.p(8, 5 + bob, '#1a1020'); c.p(10, 5 + bob, '#1a1020'); c.p(9, 7 + bob, '#aa3333')
    else:
        c.p(9, 5 + bob, '#1a1020'); c.p(11, 5 + bob, '#1a1020')
        c.p(9, 4 + bob, '#ffffff')
        c.p(10, 7 + bob, '#e89a8a')
    c.p(7, 6 + bob, '#f0a090')  # mejilla
    c.outline()
    return c.out(S)

# ---------- Hongo Gruñón (16x16, mira a la derecha) ----------
def hongo(f=0, squash=False):
    c = Canvas(16, 16)
    if squash:
        c.ellipse(7.5, 11, 7, 3, '#c0392b'); c.rect(3, 13, 12, 14, '#f3e2c7')
        for (x, y) in [(4, 10), (9, 9), (11, 11)]: c.p(x, y, '#ffffff')
        c.outline(); return c.out(S)
    up = f % 2
    # pies
    if up: c.rect(4, 14, 6, 15, '#5b3a1e'); c.rect(9, 13, 11, 14, '#5b3a1e')
    else:  c.rect(4, 13, 6, 14, '#5b3a1e'); c.rect(9, 14, 11, 15, '#5b3a1e')
    # tallo
    c.rect(4, 8, 11, 13, '#f3e2c7'); c.rect(4, 12, 11, 12, '#e2cba8')
    # ojos enojados
    EYES = True
    # sombrero
    c.ellipse(7.5, 5, 7.4, 4.5, '#c0392b')
    c.rect(1, 7, 14, 7, '#9b2a20')
    for (x, y) in [(3, 4), (7, 2), (11, 4), (5, 6), (10, 6), (13, 6)]:
        c.p(x, y, '#ffffff')
    c.p(4, 4, '#ffffff'); c.p(8, 2, '#ffffff'); c.p(12, 4, '#ffffff')
    # ojos enojados (debajo del sombrero)
    c.rect(7, 10, 8, 10, '#1a1020'); c.rect(10, 10, 11, 10, '#1a1020'); c.p(7, 9, '#1a1020'); c.p(11, 9, '#1a1020')
    c.rect(8, 12, 10, 12, '#7a2a2a')
    c.outline()
    return c.out(S)

# ---------- Murciélago Sombrío (16x12) ----------
def murcielago(f=0):
    c = Canvas(16, 12)
    up = f % 2 == 0
    body = '#5a3d7a'; wing = '#3b2656'; mem = '#7d5aa6'
    if up:
        for i in range(6):
            c.rect(6 - i, 5 - i // 2, 6 - i, 6 - i // 2 + 1, wing)
            c.rect(9 + i, 5 - i // 2, 9 + i, 6 - i // 2 + 1, wing)
        c.p(1, 2, mem); c.p(14, 2, mem)
    else:
        for i in range(6):
            c.rect(6 - i, 5 + i // 2, 6 - i, 6 + i // 2, wing)
            c.rect(9 + i, 5 + i // 2, 9 + i, 6 + i // 2, wing)
        c.p(1, 9, mem); c.p(14, 9, mem)
    c.ellipse(7.5, 5.5, 2.6, 3.2, body)
    c.p(6, 2, body); c.p(9, 2, body); c.p(6, 1, body); c.p(9, 1, body)  # orejas
    c.p(6, 5, '#ff4040'); c.p(9, 5, '#ff4040')
    c.p(7, 7, '#ffffff'); c.p(8, 7, '#ffffff')  # colmillos
    c.outline()
    return c.out(S)

# ---------- Sabio Búho Orión (16x22) ----------
def buho(f=0):
    c = Canvas(16, 22)
    # rama
    c.rect(0, 20, 15, 21, '#6b4426'); c.p(3, 19, '#4f8f3a'); c.p(13, 19, '#4f8f3a')
    # cuerpo
    c.ellipse(7.5, 13, 5.5, 6, '#8a5a32')
    c.ellipse(7.5, 14.5, 3.5, 4, '#d9b48a')
    for y in (12, 14, 16):
        c.p(6, y, '#b88f62'); c.p(9, y + 1, '#b88f62')
    # garras
    c.p(6, 19, '#f0a030'); c.p(9, 19, '#f0a030')
    # cara
    c.ellipse(5.3, 9.5, 2.3, 2.3, '#f3e6c8'); c.ellipse(10, 9.5, 2.3, 2.3, '#f3e6c8')
    if f == 1:
        c.rect(4, 9, 6, 9, '#3a2410'); c.rect(9, 9, 11, 9, '#3a2410')
    else:
        c.p(5, 9, '#1a1020'); c.p(10, 9, '#1a1020'); c.p(5, 10, '#f0c020'); c.p(10, 10, '#f0c020')
    c.p(7, 11, '#f08a20'); c.p(8, 11, '#f08a20'); c.p(7, 12, '#c06010')
    # cejas
    c.rect(3, 7, 6, 7, '#e8e0d0'); c.rect(9, 7, 12, 7, '#e8e0d0')
    # sombrero de mago con estrella
    c.rect(2, 6, 13, 6, '#4a2f8a')
    c.rect(4, 4, 11, 5, '#5b3aa8'); c.rect(5, 2, 10, 3, '#5b3aa8'); c.rect(7, 0, 9, 1, '#5b3aa8')
    c.p(10, 1, '#5b3aa8')
    c.p(7, 4, '#ffe060'); c.p(8, 3, '#ffe060')
    c.outline()
    return c.out(S)

if __name__ == '__main__':
    for i in range(2): lumi('idle', i).save(OUT + f'lumi_quieto_{i+1}.png')
    for i in range(4): lumi('walk', i).save(OUT + f'lumi_caminar_{i+1}.png')
    lumi('jump').save(OUT + 'lumi_saltar.png'); lumi('fall').save(OUT + 'lumi_caer.png')
    lumi('hurt').save(OUT + 'lumi_herido.png')
    for i in range(2): hongo(i).save(OUT + f'hongo_caminar_{i+1}.png')
    for i in range(2): murcielago(i).save(OUT + f'murcielago_volar_{i+1}.png')
    for i in range(2): buho(i).save(OUT + f'buho_{i+1}.png')
    print('ok')
