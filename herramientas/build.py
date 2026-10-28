# Genera el proyecto GDevelop "Lumi y el Corazón de Cristal" (lumi.json) a partir de los recursos creados.
import json, os, uuid, random
from PIL import Image
ROOT = '/home/claude/epe/proyecto/'
IMG = ROOT + 'assets/img/'
R = random.Random(42)
def uid(): return str(uuid.UUID(int=R.getrandbits(128)))

# ------------------------------------------------------------------ recursos
resources = []
for f in sorted(os.listdir(IMG)):
    resources.append({"alwaysLoaded": False, "file": f"assets/img/{f}", "kind": "image", "metadata": "", "name": f, "smoothed": False, "userAdded": True})
for f in sorted(os.listdir(ROOT + 'assets/snd')):
    music = f.startswith('musica') or f.startswith('ambiente')
    resources.append({"file": f"assets/snd/{f}", "kind": "audio", "metadata": "", "name": f, "preloadAsMusic": music, "preloadAsSound": not music, "preloadInCache": False, "userAdded": True})
resources.append({"file": "assets/video/transicion_nivel2.mp4", "kind": "video", "metadata": "", "name": "transicion_nivel2.mp4", "userAdded": True})
def size(img): return Image.open(IMG + img).size

# ------------------------------------------------------------------ objetos
def frame(img, mask=None):
    fr = {"hasCustomCollisionMask": mask is not None, "image": img, "points": [],
          "originPoint": {"name": "origine", "x": 0, "y": 0}, "centerPoint": {"automatic": True, "name": "centre", "x": 0, "y": 0},
          "customCollisionMask": []}
    if mask:
        x0, y0, x1, y1 = mask
        fr["customCollisionMask"] = [[{"x": x0, "y": y0}, {"x": x1, "y": y0}, {"x": x1, "y": y1}, {"x": x0, "y": y1}]]
    return fr
def anim(name, imgs, t=0.1, loop=True, mask=None):
    return {"name": name, "useMultipleDirections": False,
            "directions": [{"looping": loop, "timeBetweenFrames": t, "sprites": [frame(i, mask) for i in imgs]}]}
def var(name, value):
    t = "string" if isinstance(value, str) else ("boolean" if isinstance(value, bool) else "number")
    return {"name": name, "type": t, "value": value}
def sprite(name, anims, behaviors=(), variables=()):
    return {"adaptCollisionMaskAutomatically": False, "assetStoreId": "", "name": name, "type": "Sprite", "updateIfNotVisible": False,
            "variables": list(variables), "effects": [], "behaviors": list(behaviors), "animations": anims}
def tiled(name, texture, w, h, ptype=None):
    beh = [] if ptype is None else [{"name": "Platform", "type": "PlatformBehavior::PlatformBehavior", "canBeGrabbed": False, "platformType": ptype, "yGrabOffset": 0}]
    return {"assetStoreId": "", "height": h, "name": name, "texture": texture, "type": "TiledSpriteObject::TiledSprite", "width": w,
            "variables": [], "effects": [], "behaviors": beh}
def text(name, s, size=24, color="255;255;255", bold=True, align="left"):
    return {"assetStoreId": "", "bold": bold, "italic": False, "name": name, "smoothed": True, "type": "TextObject::Text", "underlined": False,
            "variables": [], "effects": [], "behaviors": [], "string": s, "font": "", "textAlignment": align, "characterSize": size,
            "color": {"r": int(color.split(';')[0]), "g": int(color.split(';')[1]), "b": int(color.split(';')[2])},
            "content": {"bold": bold, "isOutlineEnabled": True, "isShadowEnabled": False, "italic": False, "outlineColor": "20;10;40",
                        "outlineThickness": 3, "shadowAngle": 90, "shadowBlurRadius": 2, "shadowColor": "0;0;0", "shadowDistance": 4,
                        "shadowOpacity": 127, "smoothed": True, "underlined": False, "text": s, "font": "", "textAlignment": align,
                        "verticalTextAlignment": "top", "characterSize": size, "lineHeight": 0, "color": color}}
PLATFORMER = {"name": "PlatformerObject", "type": "PlatformBehavior::PlatformerObjectBehavior", "canGoDownFromJumpthru": True,
              "acceleration": 1500, "deceleration": 1800, "gravity": 1300, "jumpSpeed": 640, "jumpSustainTime": 0.18,
              "ladderClimbingSpeed": 200, "maxFallingSpeed": 750, "maxSpeed": 240, "canGrabPlatforms": False,
              "ignoreDefaultControls": False, "slopeMaxAngle": 60, "useLegacyTrajectory": False, "xGrabTolerance": 10, "yGrabOffset": 0}

g_objects = [
    sprite("Lumi", [
        anim("Quieto", ["lumi_quieto_1.png", "lumi_quieto_2.png"], 0.45, True, (12, 6, 39, 60)),
        anim("Caminar", [f"lumi_caminar_{i}.png" for i in range(1, 5)], 0.11, True, (12, 6, 39, 60)),
        anim("Saltar", ["lumi_saltar.png"], 0.1, False, (12, 6, 39, 60)),
        anim("Caer", ["lumi_caer.png"], 0.1, False, (12, 6, 39, 60)),
        anim("Herido", ["lumi_herido.png"], 0.1, False, (12, 6, 39, 60))], [PLATFORMER]),
    sprite("Hongo", [anim("Caminar", ["hongo_caminar_1.png", "hongo_caminar_2.png"], 0.2, True, (3, 6, 45, 48))], variables=[var("dir", -1)]),
    sprite("Murcielago", [anim("Volar", ["murcielago_volar_1.png", "murcielago_volar_2.png"], 0.12, True, (9, 6, 39, 30))],
           variables=[var("baseX", 0), var("baseY", 0)]),
    sprite("Buho", [anim("Reposo", ["buho_1.png"] * 10 + ["buho_2.png"], 0.25, True)]),
    sprite("Cristal", [anim("Brillo", [f"cristal_{i}.png" for i in range(1, 5)], 0.14, True)]),
    sprite("Pocion", [anim("Burbujas", ["pocion_1.png", "pocion_2.png"], 0.35, True)]),
    sprite("Runa", [anim("Inactiva", ["runa_inactiva.png"]), anim("Activa", ["runa_activa_1.png", "runa_activa_2.png"], 0.3, True)]),
    sprite("Destello", [anim("Explosion", [f"destello_{i}.png" for i in range(1, 5)], 0.06, False)]),
    sprite("TopeIzq", [anim("Tope", ["tope.png"])]),
    sprite("TopeDer", [anim("Tope", ["tope.png"])]),
    sprite("TeclaE", [anim("Aviso", ["tecla_e.png"])]),
    sprite("PanelDialogo", [anim("Panel", ["panel_dialogo.png"])]),
    sprite("IconoCorazon", [anim("Icono", ["hud_corazon.png"])]),
    sprite("IconoCristal", [anim("Icono", ["hud_cristal.png"])]),
    sprite("Flor", [anim("Deco", ["deco_flor.png"])]),
    sprite("HongoLuz", [anim("Deco", ["deco_hongo_luz.png"])]),
    sprite("Cartel", [anim("Deco", ["deco_cartel.png"])]),
    sprite("CristalGrande", [anim("Deco", ["deco_cristal_grande.png"])]),
    text("TextoVidas", "x 3", 26), text("TextoCristales", "x 0", 26), text("TextoPuntaje", "Puntaje: 0", 26, "255;230;140"),
    text("TextoDialogo", "", 24, "255;248;220", True), text("TextoAviso", "", 26, "190;240;255", True, "center"),
]
g_groups = [{"name": "Enemigos", "objects": [{"name": "Hongo"}, {"name": "Murcielago"}]}]
g_vars = [var("Vidas", 3), var("Cristales", 0), var("Puntaje", 0)]

# ------------------------------------------------------------------ eventos (ayudantes)
def I(t, *p, inv=False):
    d = {"type": {"value": t}, "parameters": list(p)}
    if inv: d["type"]["inverted"] = True
    return d
def E(conds, acts, subs=()):
    e = {"type": "BuiltinCommonInstructions::Standard", "conditions": conds, "actions": acts}
    if subs: e["events"] = list(subs)
    return e
def C(texto, color=(255, 230, 150)):
    return {"type": "BuiltinCommonInstructions::Comment", "color": {"r": color[0], "g": color[1], "b": color[2], "textR": 0, "textG": 0, "textB": 0}, "comment": texto}
def G(nombre, eventos, color=(74, 176, 228)):
    return {"type": "BuiltinCommonInstructions::Group", "name": nombre, "source": "", "creationTime": 0,
            "colorR": color[0], "colorG": color[1], "colorB": color[2], "parameters": [], "events": list(eventos)}
def q1(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
def q(s): return " + NewLine() + ".join(q1(x) for x in s.split("\n"))
P = "PlatformerObject"
begins = I("SceneJustBegins", "")
once = I("BuiltinCommonInstructions::Once")
def setv(v, op, val): return I("SetNumberVariable", v, op, str(val))
def isv(v, op, val, inv=False): return I("NumberVariable", v, op, str(val), inv=inv)
def sound(f, vol=70): return I("PlaySound", "", f, "", str(vol), "1")
def settext(obj, expr): return I("TextObject::String", obj, "=", expr)
def aviso(expr): return [settext("TextoAviso", expr), I("Show", "TextoAviso", ""), I("ResetTimer", "", q("aviso"))]
def scene(name): return I("Scene", "", q(name), "")
def key_released(k): return I("KeyFromTextReleased", "", q(k))

# ------------------------------------------------------------------ escenas
LAYERS = lambda: [
    {"ambientLightColorB": 200, "ambientLightColorG": 200, "ambientLightColorR": 200, "camera2DPlaneMaxDrawingDistance": 5000, "camera3DFarPlaneDistance": 10000,
     "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 3, "cameraType": "", "followBaseLayerCamera": False, "isLightingLayer": False, "isLocked": False,
     "name": "", "renderingType": "", "visibility": True,
     "cameras": [{"defaultSize": True, "defaultViewport": True, "height": 0, "viewportBottom": 1, "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}], "effects": []},
    {"ambientLightColorB": 200, "ambientLightColorG": 200, "ambientLightColorR": 200, "camera2DPlaneMaxDrawingDistance": 5000, "camera3DFarPlaneDistance": 10000,
     "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 3, "cameraType": "", "followBaseLayerCamera": False, "isLightingLayer": False, "isLocked": False,
     "name": "HUD", "renderingType": "2d", "visibility": True, "cameras": [], "effects": []}]
SHARED = [{"name": "Platform", "type": "PlatformBehavior::PlatformBehavior"}, {"name": "PlatformerObject", "type": "PlatformBehavior::PlatformerObjectBehavior"}]

def layout(name, objects, instances, events, variables=(), bg=(20, 16, 36), groups=()):
    return {"b": bg[2], "disableInputWhenNotFocused": True, "mangledName": name, "name": name, "r": bg[0], "standardSortMethod": True,
            "stopSoundsOnStartup": True, "title": "", "v": bg[1],
            "uiSettings": {"grid": False, "gridType": "rectangular", "gridWidth": 32, "gridHeight": 32, "gridDepth": 32, "gridOffsetX": 0, "gridOffsetY": 0,
                           "gridOffsetZ": 0, "gridColor": 10401023, "gridAlpha": 0.8, "snap": False, "zoomFactor": 0.4, "windowMask": False, "selectedLayer": "",
                           "gameEditorMode": "instances-editor"},
            "objectsGroups": list(groups), "variables": list(variables), "instances": instances, "objects": objects,
            "objectsFolderStructure": {"folderName": "__ROOT"}, "events": events, "layers": LAYERS(), "behaviorsSharedData": SHARED}

def inst(name, x, y, z=1, w=None, h=None, layer=""):
    d = {"angle": 0, "customSize": w is not None, "height": h or 0, "layer": layer, "name": name, "persistentUuid": uid(),
         "width": w or 0, "x": x, "y": y, "zOrder": z, "numberProperties": [], "stringProperties": [], "initialVariables": []}
    return d

def hud_instances():
    return [inst("IconoCorazon", 20, 16, 50, layer="HUD"), inst("TextoVidas", 56, 14, 50, layer="HUD"),
            inst("IconoCristal", 150, 12, 50, layer="HUD"), inst("TextoCristales", 180, 14, 50, layer="HUD"),
            inst("TextoPuntaje", 700, 14, 50, layer="HUD"),
            inst("PanelDialogo", 100, 60, 60, layer="HUD"), inst("TextoDialogo", 130, 82, 61, layer="HUD"),
            inst("TextoAviso", 80, 230, 62, 800, 40, layer="HUD")]

# ---------------- niveles
GROUND_Y = 476
def build_level(n):
    bosque = n == 1
    W = 4800
    objs = []
    for i in range(1, 6):
        img = f"fondo_{'bosque' if bosque else 'cueva'}_{i}.png"
        objs.append(sprite(f"Fondo{i}", [anim("Fondo", [img])]))
    suelo = "SueloBosque" if bosque else "SueloCueva"
    plat = "PlataformaMadera" if bosque else "PlataformaCristal"
    objs.append(tiled(suelo, "suelo_bosque.png" if bosque else "suelo_cueva.png", 32, 64, "NormalPlatform"))
    objs.append(tiled(plat, "plataforma_madera.png" if bosque else "plataforma_cristal.png", 32, 16, "Jumpthru"))
    meta = None
    if bosque:
        objs.append(sprite("Portal", [anim("Sellado", ["portal_sellado.png"]), anim("Abierto", [f"portal_abierto_{i}.png" for i in range(1, 5)], 0.12, True)]))
        meta = "Portal"
    else:
        objs.append(sprite("Corazon", [anim("Dormido", ["corazon_dormido.png"]), anim("Despierto", ["corazon_despierto_1.png", "corazon_despierto_2.png"], 0.4, True)]))
        meta = "Corazon"
    I_ = []
    for i in range(5): I_.append(inst(f"Fondo{i+1}", 960 * i, 0, -100))
    if bosque:
        ground = [(0, 1100), (1220, 2000), (2110, 3100), (3230, 4800)]
        plats = [(470, 380, 128), (720, 310, 128), (1110, 380, 128), (1450, 370, 160), (1690, 300, 128), (2010, 370, 96),
                 (2380, 350, 160), (2620, 270, 128), (2880, 350, 128), (3120, 380, 128), (3600, 360, 160), (3900, 300, 128), (4180, 370, 128)]
        hongos = [(420, 900), (1300, 1880), (2200, 2900), (3300, 3700), (3950, 4380)]
        bats = [(1650, 190), (2700, 160)]
        runas = [1560, 2960]
        pociones = [(1730, 255), (3940, 255)]
        buho = 3380
        meta_xy = (4528, 380)
        crist = [(520, 340), (560, 340), (770, 270), (810, 270), (1150, 300), (1500, 330), (1540, 330), (1740, 200),
                 (2040, 330), (2430, 310), (2470, 310), (2670, 230), (2710, 230), (2930, 310), (3170, 340), (3650, 320),
                 (3690, 320), (4230, 330), (1000, 420), (2500, 420)]
        decos = [("Flor", x, GROUND_Y - 24) for x in (60, 200, 640, 980, 1350, 2260, 2700, 3480, 4100, 4700)] + [("Cartel", 150, GROUND_Y - 40)]
    else:
        ground = [(0, 900), (1040, 1700), (1830, 2600), (2760, 3500), (3640, 4800)]
        plats = [(400, 370, 128), (650, 300, 128), (880, 360, 160), (1200, 360, 128), (1450, 290, 128), (1690, 380, 160),
                 (2000, 340, 128), (2260, 270, 128), (2560, 360, 224), (2950, 340, 128), (3200, 270, 160), (3470, 370, 192),
                 (3800, 300, 128), (4100, 350, 128)]
        hongos = [(250, 860), (1100, 1640), (1900, 2560), (2800, 3450), (3700, 4100)]
        bats = [(700, 170), (1550, 160), (2350, 150), (3300, 160)]
        runas = [1300, 2900]
        pociones = [(1500, 245), (3250, 225)]
        buho = 3900
        meta_xy = (4560, 396)
        crist = [(440, 330), (690, 260), (730, 260), (940, 320), (980, 320), (1240, 320), (1490, 250), (1530, 250),
                 (1740, 340), (1780, 340), (2040, 300), (2300, 230), (2340, 230), (2620, 320), (2670, 320), (2990, 300),
                 (3250, 230), (3290, 230), (3520, 330), (3570, 330), (3840, 260), (4140, 310)]
        decos = [("HongoLuz", x, GROUND_Y - 24) for x in (120, 520, 1300, 2050, 2400, 3050, 3700, 4300)] + [("CristalGrande", x, GROUND_Y - 40) for x in (800, 2150, 3300, 4420)]
    for (a, b) in ground: I_.append(inst(suelo, a, GROUND_Y, 1, b - a, 64))
    for (x, y, w) in plats: I_.append(inst(plat, x, y, 1, w, 16))
    for (a, b) in hongos:
        I_.append(inst("TopeIzq", a - 16, GROUND_Y - 32, 2)); I_.append(inst("TopeDer", b, GROUND_Y - 32, 2))
        I_.append(inst("Hongo", (a + b) // 2, GROUND_Y - 48, 5))
    for (x, y) in bats: I_.append(inst("Murcielago", x, y, 6))
    for x in runas: I_.append(inst("Runa", x, GROUND_Y - 44, 3))
    for (x, y) in pociones: I_.append(inst("Pocion", x, y, 4))
    for (x, y) in crist: I_.append(inst("Cristal", x, y, 4))
    for (o, x, y) in decos: I_.append(inst(o, x, y, 0))
    I_.append(inst("Buho", buho, GROUND_Y - 66, 3)); I_.append(inst("TeclaE", buho + 12, GROUND_Y - 110, 7))
    I_.append(inst(meta, *meta_xy, 2))
    I_.append(inst("Lumi", 80, GROUND_Y - 60, 10))
    I_ += hud_instances()

    paso = "paso_pasto.ogg" if bosque else "paso_roca.ogg"
    musica = "musica_bosque.ogg" if bosque else "musica_cueva.ogg"
    amb = "ambiente_bosque.ogg" if bosque else "ambiente_cueva.ogg"
    nombre_nivel = "Nivel 1: El Bosque de Lumen" if bosque else "Nivel 2: Las Cavernas de Cristal"
    if bosque:
        dialogo = ["¡Hola, Lumi! Soy Orión, guardián del bosque.",
                   "Las sombras robaron el Corazón de Cristal\ny el bosque está perdiendo su luz.",
                   "He abierto el portal antiguo. ¡Crúzalo y\nrecupera el Corazón en las cavernas!"]
    else:
        dialogo = ["Llegaste, pequeña. Este es el último tramo.",
                   "El Corazón solo despierta ante quien trae\nal menos 10 cristales de esta caverna.",
                   "Reúne los cristales y toca el Corazón.\n¡El bosque confía en ti!"]

    ev = []
    ev.append(C(f"{nombre_nivel}. Las hojas de eventos se organizan en grupos: inicio, avatar, NPCs, objetos, diálogo, meta, HUD y cámara.\n"
                "Lumi usa el comportamiento Plataformero (flechas para moverse, Espacio o Shift para saltar)."))
    # --- inicio
    ev.append(G("1. Inicio de la escena", [
        C("Al comenzar: música incidental en el canal 1, sonido ambiental en bucle en el canal 2, checkpoint inicial y elementos ocultos."),
        E([begins], [
            I("PlayMusicOnChannel", "", musica, "1", "yes", "45", "1"),
            I("PlaySoundOnChannel", "", amb, "2", "yes", "55", "1"),
            setv("CheckX", "=", "Lumi.X()"), setv("CheckY", "=", "Lumi.Y()"),
            I("Hide", "TopeIzq"), I("Hide", "TopeDer"), I("Hide", "PanelDialogo"), I("Hide", "TextoDialogo"), I("Hide", "TeclaE"),
            I("ResetObjectTimer", "Lumi", q("invul")), I("ResetObjectTimer", "Lumi", q("paso")),
            I("SetNumberObjectVariable", "Murcielago", "baseX", "=", "Murcielago.X()"),
            I("SetNumberObjectVariable", "Murcielago", "baseY", "=", "Murcielago.Y()"),
            I("SetAnimationName", meta, q("Sellado" if bosque else "Dormido")),
        ] + aviso(q(nombre_nivel + ("\n¡Busca al Sabio Orión!" if bosque else "\nReúne 10 cristales")))),
    ], (80, 160, 90)))
    # --- avatar
    ev.append(G("2. Avatar: animaciones, orientación y sonidos", [
        C("Cambio de animación según el estado del comportamiento Plataformero."),
        E([I("PlatformBehavior::IsJumping", "Lumi", P)], [I("SetAnimationName", "Lumi", q("Saltar"))]),
        E([I("PlatformBehavior::IsFalling", "Lumi", P)], [I("SetAnimationName", "Lumi", q("Caer"))]),
        E([I("PlatformBehavior::IsOnFloor", "Lumi", P), I("PlatformBehavior::IsMoving", "Lumi", P)], [I("SetAnimationName", "Lumi", q("Caminar"))]),
        E([I("PlatformBehavior::IsOnFloor", "Lumi", P), I("PlatformBehavior::IsMoving", "Lumi", P, inv=True)], [I("SetAnimationName", "Lumi", q("Quieto"))]),
        C("Efecto espejo: así no se necesitan animaciones duplicadas hacia la izquierda."),
        E([I("KeyFromTextPressed", "", q("Left"))], [I("FlipX", "Lumi", "yes")]),
        E([I("KeyFromTextPressed", "", q("Right"))], [I("FlipX", "Lumi", "no")]),
        C("Sonido de pasos cada 0,3 s mientras camina, y sonido al saltar (solo una vez por salto)."),
        E([I("PlatformBehavior::IsOnFloor", "Lumi", P), I("PlatformBehavior::IsMoving", "Lumi", P), I("CompareObjectTimer", "Lumi", q("paso"), ">=", "0.3")],
          [sound(paso, 55), I("ResetObjectTimer", "Lumi", q("paso"))]),
        E([I("PlatformBehavior::IsJumping", "Lumi", P), once], [sound("salto.ogg", 50)]),
        C("Invulnerabilidad de 1,5 s tras recibir daño: el avatar parpadea."),
        E([I("CompareObjectTimer", "Lumi", q("invul"), "<", "1.5")], [I("OpacityCapability::OpacityBehavior::SetValue", "Lumi", "Opacity", "=", "80 + 175 * mod(round(TimeFromStart() * 12), 2)")]),
        E([I("CompareObjectTimer", "Lumi", q("invul"), ">=", "1.5")], [I("OpacityCapability::OpacityBehavior::SetValue", "Lumi", "Opacity", "=", "255")]),
    ], (74, 176, 228)))
    # --- NPCs
    ev.append(G("3. NPC tipo 1: Hongo Gruñón (patrulla entre topes invisibles)", [
        C("El hongo se desplaza con una fuerza instantánea; al tocar un tope invierte su dirección (variable de objeto dir) y se refleja."),
        E([], [I("AddForceXY", "Hongo", "Hongo.Variable(dir) * 70", "0", "0")]),
        E([I("CollisionNP", "Hongo", "TopeIzq", "", "", "")], [I("SetNumberObjectVariable", "Hongo", "dir", "=", "1")]),
        E([I("CollisionNP", "Hongo", "TopeDer", "", "", "")], [I("SetNumberObjectVariable", "Hongo", "dir", "=", "-1")]),
        E([I("NumberObjectVariable", "Hongo", "dir", "=", "1")], [I("FlipX", "Hongo", "no")]),
        E([I("NumberObjectVariable", "Hongo", "dir", "=", "-1")], [I("FlipX", "Hongo", "yes")]),
    ], (200, 90, 80)))
    ev.append(G("4. NPC tipo 2: Murciélago Sombrío (vuela y persigue)", [
        C("Si Lumi está a menos de 260 px, el murciélago la persigue; si no, revolotea alrededor de su posición inicial."),
        E([I("Distance", "Murcielago", "Lumi", "260", "")], [I("AddForceTowardObject", "Murcielago", "Lumi", "115", "0")],
          [E([once], [sound("murcielago.ogg", 60)])]),
        E([I("Distance", "Murcielago", "Lumi", "260", "", inv=True)], [
            I("AddForceXY", "Murcielago", "90 * cos(TimeFromStart() * 1.6)", "45 * cos(TimeFromStart() * 3.1)", "0"),
            I("AddForceTowardPosition", "Murcielago", "Murcielago.Variable(baseX)", "Murcielago.Variable(baseY)", "40", "0")]),
        E([I("PosX", "Murcielago", "<", "Lumi.X()")], [I("FlipX", "Murcielago", "no")]),
        E([I("PosX", "Murcielago", ">=", "Lumi.X()")], [I("FlipX", "Murcielago", "yes")]),
    ], (140, 90, 200)))
    ev.append(G("5. Avatar frente a enemigos: aplastar o recibir daño", [
        C("Mecánica tipo Mario: si Lumi cae sobre un enemigo, lo elimina y rebota. El orden de los eventos importa: este evento va antes del daño."),
        E([I("CollisionNP", "Lumi", "Enemigos", "", "", ""), I("PlatformBehavior::IsFalling", "Lumi", P)], [
            I("Create", "", "Destello", "Enemigos.X()", "Enemigos.Y()", q("")), I("Delete", "Enemigos", ""),
            I("PlatformBehavior::SetCanJump", "Lumi", P), I("PlatformBehavior::SimulateJumpKey", "Lumi", P),
            sound("aplastar.ogg", 80), setv("Puntaje", "+", 20)]),
        C("Si el contacto es lateral y no está en invulnerabilidad, pierde una vida y vuelve al último checkpoint."),
        E([I("CollisionNP", "Lumi", "Enemigos", "", "", ""), I("CompareObjectTimer", "Lumi", q("invul"), ">=", "1.5")], [
            setv("Vidas", "-", 1), sound("herido.ogg", 80), I("ResetObjectTimer", "Lumi", q("invul")),
            I("SetXY", "Lumi", "=", "Variable(CheckX)", "=", "Variable(CheckY)")] + aviso(q("¡Auch! Vuelves a la última runa"))),
        C("Caer a un abismo también cuesta una vida."),
        E([I("PosY", "Lumi", ">", "620")], [
            setv("Vidas", "-", 1), sound("herido.ogg", 80), I("ResetObjectTimer", "Lumi", q("invul")),
            I("SetXY", "Lumi", "=", "Variable(CheckX)", "=", "Variable(CheckY)")] + aviso(q("¡Cuidado con los abismos!"))),
        E([isv("Vidas", "<=", 0)], [scene("FinDelJuego")]),
    ], (220, 120, 60)))
    # --- objetos del entorno
    ev.append(G("6. Avatar frente a objetos del entorno", [
        C("Cristales: suman al puntaje global (persiste entre niveles) y al contador del nivel, con sonido y destello."),
        E([I("CollisionNP", "Lumi", "Cristal", "", "", "")], [
            I("Create", "", "Destello", "Cristal.X()", "Cristal.Y()", q("")), I("Delete", "Cristal", ""),
            setv("Cristales", "+", 1), setv("CristalesNivel", "+", 1), setv("Puntaje", "+", 10), sound("cristal.ogg", 60)]),
        E([I("AnimationEnded", "Destello")], [I("Delete", "Destello", "")]),
        C("Poción: recupera una vida (máximo 5)."),
        E([I("CollisionNP", "Lumi", "Pocion", "", "", "")], [I("Delete", "Pocion", ""), sound("pocion.ogg", 70)] + aviso(q("+1 vida")),
          [E([isv("Vidas", "<", 5)], [setv("Vidas", "+", 1)])]),
        C("Runas: checkpoints que guardan la posición en variables de escena."),
        E([I("CollisionNP", "Lumi", "Runa", "", "", ""), I("AnimationName", "Runa", q("Activa"), inv=True)], [
            I("SetAnimationName", "Runa", q("Activa")), setv("CheckX", "=", "Runa.X()"), setv("CheckY", "=", "Runa.Y() - 20"),
            sound("runa.ogg", 70)] + aviso(q("Runa activada: punto de control guardado"))),
    ], (90, 190, 200)))
    # --- diálogo
    dlg = [
        C("NPC tipo 3: Sabio Orión. Al acercarse aparece la tecla E; cada pulsación avanza el diálogo (variable de escena Dialogo)."),
        E([I("Distance", "Lumi", "Buho", "150", "")], [I("Show", "TeclaE", "")], [
            E([key_released("e")], [setv("Dialogo", "+", 1), sound("buho.ogg", 70)]),
        ]),
        E([I("Distance", "Lumi", "Buho", "150", "", inv=True)], [I("Hide", "TeclaE"), setv("Dialogo", "=", 0)]),
        E([isv("Dialogo", "=", 0)], [I("Hide", "PanelDialogo"), I("Hide", "TextoDialogo")]),
        E([isv("Dialogo", ">", 0), isv("Dialogo", "<", 4)], [I("Show", "PanelDialogo", ""), I("Show", "TextoDialogo", "")]),
    ]
    for i, linea in enumerate(dialogo):
        acts = [settext("TextoDialogo", q("Orión: " + linea + "\n\n[E] continuar"))]
        if i == 2:
            acts += [setv("HabloConBuho", "=", 1)]
        dlg.append(E([isv("Dialogo", "=", i + 1)], acts))
    dlg.append(E([isv("Dialogo", ">=", 4)], [setv("Dialogo", "=", 0)]))
    if bosque:
        dlg.append(E([isv("HabloConBuho", "=", 1), I("AnimationName", meta, q("Sellado"))], [I("SetAnimationName", meta, q("Abierto")), sound("runa.ogg", 70)]))
    ev.append(G("7. Diálogo con el Sabio Orión", dlg, (230, 200, 90)))
    # --- meta
    if bosque:
        meta_ev = [
            C("El portal solo funciona después de hablar con Orión. Lleva a la escena de transición con video."),
            E([I("CollisionNP", "Lumi", "Portal", "", "", ""), isv("HabloConBuho", "=", 1), once],
              [sound("portal.ogg", 80), I("StopMusicChannel", "", "1"), scene("Transicion")]),
            E([I("CollisionNP", "Lumi", "Portal", "", "", ""), isv("HabloConBuho", "=", 0), once],
              [sound("sellado.ogg", 70)] + aviso(q("El portal está sellado. Habla con el Sabio Orión."))),
        ]
    else:
        meta_ev = [
            C("El Corazón despierta cuando Lumi habló con Orión y reunió 10 cristales en este nivel."),
            E([isv("HabloConBuho", "=", 1), isv("CristalesNivel", ">=", 10), I("AnimationName", "Corazon", q("Dormido"))],
              [I("SetAnimationName", "Corazon", q("Despierto")), sound("runa.ogg", 80)] + aviso(q("¡El Corazón de Cristal despertó!"))),
            E([I("CollisionNP", "Lumi", "Corazon", "", "", ""), I("AnimationName", "Corazon", q("Despierto")), once],
              [sound("portal.ogg", 80), setv("Puntaje", "+", "Variable(CristalesNivel) * 5 + GlobalVariable(Vidas) * 50"), scene("Victoria")]),
            E([I("CollisionNP", "Lumi", "Corazon", "", "", ""), I("AnimationName", "Corazon", q("Dormido")), once],
              [sound("sellado.ogg", 70)] + aviso('"El Corazón duerme. Cristales: " + ToString(Variable(CristalesNivel)) + " de 10" + '
                                                 '(Variable(HabloConBuho) = 0 ? "" : "")')),
        ]
        meta_ev[-1]["actions"][1]["parameters"][2] = '"El Corazón duerme. Cristales: " + ToString(Variable(CristalesNivel)) + " de 10. ¿Hablaste con Orión?"'
    ev.append(G("8. Meta del nivel", meta_ev, (160, 110, 220)))
    # --- HUD y cámara
    ev.append(G("9. HUD y cámara", [
        C("El HUD está en la capa HUD, que no se mueve con la cámara."),
        E([], [settext("TextoVidas", '"x " + ToString(GlobalVariable(Vidas))'),
               settext("TextoCristales", '"x " + ToString(GlobalVariable(Cristales))'),
               settext("TextoPuntaje", '"Puntaje: " + ToString(GlobalVariable(Puntaje))')]),
        E([I("CompareTimer", "", q("aviso"), ">=", "3")], [I("Hide", "TextoAviso")]),
        C("La cámara sigue a Lumi y no sale de los límites del nivel (10 pantallas en total: 5 por nivel)."),
        E([], [I("CenterCameraOnObject", "", "Lumi", "", "", ""), I("ClampCamera", "", "0", "0", str(W), "540", "", "")]),
    ], (120, 120, 120)))
    variables = [var("CheckX", 0), var("CheckY", 0), var("Dialogo", 0), var("HabloConBuho", 0), var("CristalesNivel", 0)]
    return layout(f"Nivel{n}", objs, I_, ev, variables, (110, 170, 230) if bosque else (20, 16, 36))

# ---------------- menú, transición, fin del juego, victoria
def simple_screen(name, bg_img, musica, textos, events_extra, loop_music=True):
    objs = [sprite("Fondo", [anim("Fondo", [bg_img])])] + [text(n, s, sz, col, True, "center") for (n, s, sz, col, x, y) in textos]
    insts = [inst("Fondo", 0, 0, -10)] + [inst(n, x, y, 5, 960, sz + 20) for (n, s, sz, col, x, y) in textos]
    ev = [E([begins], [I("PlayMusicOnChannel", "", musica, "1", "yes" if loop_music else "no", "50", "1")])] + events_extra
    return layout(name, objs, insts, ev)

menu = simple_screen("Menu", "fondo_menu.png", "musica_menu.ogg", [
    ("TextoInicio", "Presiona ENTER para comenzar", 30, "255;255;255", 0, 300),
    ("TextoControles", "Flechas: moverse   ·   Espacio: saltar   ·   E: hablar", 22, "200;230;255", 0, 380),
    ("TextoMision", "Recupera el Corazón de Cristal y devuelve la luz al bosque", 22, "255;230;160", 0, 420),
    ("TextoCredito", "Juego de ejemplo · Docente: Sabina Romero · Taller de Programación de Videojuegos · IPChile", 17, "255;230;160", 0, 500)],
    [C("Menú principal: reinicia las variables globales y comienza el Nivel 1."),
     E([], [I("OpacityCapability::OpacityBehavior::SetValue", "TextoInicio", "Opacity", "=", "150 + 105 * sin(TimeFromStart() * 4)")]),
     E([key_released("Return")], [setv("Vidas", "=", 3), setv("Cristales", "=", 0), setv("Puntaje", "=", 0), scene("Nivel1")])])

gameover = simple_screen("FinDelJuego", "fondo_gameover.png", "musica_gameover.ogg", [
    ("TextoResumen", "Cristales: 0   ·   Puntaje: 0", 28, "255;220;220", 0, 270),
    ("TextoVolver", "Presiona ENTER para volver al menú", 26, "255;255;255", 0, 340)],
    [E([begins], [settext("TextoResumen", '"Cristales: " + ToString(GlobalVariable(Cristales)) + "   ·   Puntaje: " + ToString(GlobalVariable(Puntaje))')]),
     E([key_released("Return")], [scene("Menu")])], loop_music=False)

victoria = simple_screen("Victoria", "fondo_victoria.png", "musica_victoria.ogg", [
    ("TextoResumen", "", 30, "255;240;180", 0, 280),
    ("TextoVolver", "Presiona ENTER para volver al menú", 26, "255;255;255", 0, 380)],
    [E([begins], [settext("TextoResumen", '"Cristales: " + ToString(GlobalVariable(Cristales)) + "   ·   Puntaje final: " + ToString(GlobalVariable(Puntaje))')]),
     E([key_released("Return")], [scene("Menu")])], loop_music=False)

video_obj = {"assetStoreId": "", "name": "Video", "type": "Video::VideoObject", "variables": [], "effects": [], "behaviors": [],
             "content": {"opacity": 255, "loop": False, "volume": 100, "videoResource": "transicion_nivel2.mp4"}}
trans = layout("Transicion", [video_obj, text("TextoSaltar", "ESPACIO: saltar escena", 18, "220;220;240", False, "right")],
               [inst("Video", 0, 0, 1, 960, 540), inst("TextoSaltar", 0, 506, 5, 940, 30, "HUD")],
               [C("Escena de transición entre niveles: reproduce un video MP4 (H.264 + AAC). Al terminar, o con Espacio, pasa al Nivel 2."),
                E([begins], [I("Video::Play", "Video")]),
                E([I("Video::Ended", "Video")], [scene("Nivel2")]),
                E([key_released("Space")], [scene("Nivel2")])], bg=(0, 0, 0))

project = {
    "firstLayout": "Menu",
    "gdVersion": {"build": 280, "major": 5, "minor": 6, "revision": 0},
    "properties": {
        "adaptGameResolutionAtRuntime": True, "antialiasingMode": "none", "antialisingEnabledOnMobile": False, "folderProject": False,
        "orientation": "landscape", "packageName": "cl.ipchile.lumi", "pixelsRounding": True, "projectUuid": uid(), "scaleMode": "nearest",
        "sizeOnStartupMode": "adaptWidth", "templateSlug": "", "useDeprecatedZeroAsDefaultStringVariable": False, "version": "1.0.0",
        "name": "Lumi y el Corazón de Cristal", "description": "Proyecto modelo de nivel Destacado: plataformas de fantasía con 2 niveles, 3 tipos de NPC y transición en video.",
        "author": "Sabina Romero", "windowWidth": 960, "windowHeight": 540, "latestCompilationDirectory": "", "maxFPS": 60, "minFPS": 20,
        "verticalSync": False, "platformSpecificAssets": {},
        "loadingScreen": {"backgroundColor": 1314852, "backgroundFadeInDuration": 0.2, "backgroundImageResourceName": "", "gdevelopLogoStyle": "light",
                          "logoAndProgressFadeInDuration": 0.2, "logoAndProgressLogoFadeInDelay": 0.2, "minDuration": 1, "progressBarColor": 16777215,
                          "progressBarHeight": 20, "progressBarMaxWidth": 200, "progressBarMinWidth": 40, "progressBarWidthPercent": 30,
                          "showGDevelopSplash": True, "showProgressBar": True},
        "watermark": {"placement": "bottom-left", "showWatermark": True},
        "authorIds": [], "authorUsernames": [], "categories": [], "playableDevices": ["keyboard"], "extensionProperties": [],
        "platforms": [{"name": "GDevelop JS platform"}], "currentPlatform": "GDevelop JS platform"},
    "resources": {"resources": resources, "resourceFolders": []},
    "objects": g_objects, "objectsFolderStructure": {"folderName": "__ROOT"}, "objectsGroups": g_groups,
    "variables": g_vars,
    "layouts": [menu, build_level(1), trans, build_level(2), victoria, gameover],
    "externalEvents": [], "eventsFunctionsExtensions": [], "externalLayouts": []}

json.dump(project, open(ROOT + 'lumi.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ok', len(resources), 'recursos;', sum(len(l['instances']) for l in project['layouts']), 'instancias')
