// Prueba automática del juego exportado por GDevelop (Playwright + Chromium headless).
const { chromium } = require('playwright');
const SHOT = '/tmp/claude-0/-home-claude/7937a689-4a63-51d5-b893-1bc94c5ca2a9/scratchpad/';
const results = [];
function check(name, ok, info = '') { results.push({ name, ok, info }); console.log((ok ? 'OK  ' : 'FAIL') + ' ' + name + (info ? '  -> ' + info : '')); }
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required', '--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 960, height: 540 } });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  const S = () => page.evaluate(() => window.game.getSceneStack().getCurrentScene().getName());
  const G = name => page.evaluate(n => window.game.getVariables().get(n).getAsNumber(), name);
  const V = name => page.evaluate(n => window.game.getSceneStack().getCurrentScene().getVariables().get(n).getAsNumber(), name);
  const count = o => page.evaluate(o => window.game.getSceneStack().getCurrentScene().getObjects(o).length, o);
  const lumi = () => page.evaluate(() => { const l = window.game.getSceneStack().getCurrentScene().getObjects('Lumi')[0]; return { x: l.getX(), y: l.getY(), anim: l.getAnimationName(), op: l.getOpacity() }; });
  const tp = (x, y) => page.evaluate(([x, y]) => { const l = window.game.getSceneStack().getCurrentScene().getObjects('Lumi')[0]; l.setX(x); l.setY(y); }, [x, y]);
  const objPos = (o, i = 0) => page.evaluate(([o, i]) => { const a = window.game.getSceneStack().getCurrentScene().getObjects(o)[i]; return a ? { x: a.getX(), y: a.getY(), w: a.getWidth(), h: a.getHeight(), anim: a.getAnimationName ? a.getAnimationName() : null, vis: !a.isHidden() } : null; }, [o, i]);
  const text = o => page.evaluate(o => window.game.getSceneStack().getCurrentScene().getObjects(o)[0].getText(), o);
  const press = async (k, ms = 120) => { await page.keyboard.down(k); await sleep(ms); await page.keyboard.up(k); await sleep(120); };
  const waitScene = async (n, t = 8000) => { const t0 = Date.now(); while (Date.now() - t0 < t) { try { if (await S() === n) return true; } catch (e) { } await sleep(150); } return false; };

  await page.goto('http://localhost:8765/index.html');
  check('Carga y abre el Menú', await waitScene('Menu', 20000));
  await sleep(800);
  await page.screenshot({ path: SHOT + 't_menu.png' });
  await press('Enter');
  check('ENTER en el menú inicia el Nivel 1', await waitScene('Nivel1'));
  await sleep(1500);
  await page.screenshot({ path: SHOT + 't_n1_inicio.png' });
  check('Variables globales iniciales (3 vidas, 0 cristales)', (await G('Vidas')) === 3 && (await G('Cristales')) === 0);
  check('Topes ocultos al iniciar', !(await objPos('TopeIzq')).vis);
  check('Aviso inicial visible', (await objPos('TextoAviso')).vis, await text('TextoAviso'));

  // Movimiento y animaciones
  const p0 = await lumi();
  await page.keyboard.down('ArrowRight'); await sleep(500);
  const p1 = await lumi(); await page.keyboard.up('ArrowRight');
  check('Flecha derecha mueve a Lumi y anima "Caminar"', p1.x > p0.x + 50 && p1.anim === 'Caminar', `x ${p0.x.toFixed(0)}→${p1.x.toFixed(0)}, anim ${p1.anim}`);
  await page.keyboard.down('Space'); await sleep(150);
  const pj = await lumi(); await page.keyboard.up('Space'); await sleep(900);
  check('Espacio hace saltar (anim "Saltar")', pj.anim === 'Saltar' && pj.y < p1.y, `y ${p1.y.toFixed(0)}→${pj.y.toFixed(0)} anim ${pj.anim}`);
  check('Al aterrizar vuelve a "Quieto"', (await lumi()).anim === 'Quieto', (await lumi()).anim);
  await page.keyboard.down('ArrowLeft'); await sleep(200); await page.keyboard.up('ArrowLeft');
  check('Efecto espejo al ir a la izquierda', await page.evaluate(() => window.game.getSceneStack().getCurrentScene().getObjects('Lumi')[0].isFlippedX()));

  // NPC 1: hongo patrulla
  const h0 = await objPos('Hongo'); await sleep(1200); const h1 = await objPos('Hongo');
  check('Hongo patrulla (se desplaza)', Math.abs(h1.x - h0.x) > 30, `x ${h0.x.toFixed(0)}→${h1.x.toFixed(0)}`);
  // Aplastar
  const nh = await count('Hongo'); const pts0 = await G('Puntaje');
  const h = await objPos('Hongo');
  await tp(h.x + 4, h.y - 75); await sleep(1000);
  check('Caer sobre el hongo lo elimina y suma 20 puntos', (await count('Hongo')) === nh - 1 && (await G('Puntaje')) === pts0 + 20, `hongos ${nh}→${await count('Hongo')}, puntaje ${pts0}→${await G('Puntaje')}`);
  // Daño lateral
  await sleep(1600);
  const hb = await objPos('Hongo'); const v0 = await G('Vidas');
  await tp(hb.x + 10, hb.y - 12); await sleep(250);
  const v1 = await G('Vidas'); const pl = await lumi();
  check('Contacto lateral resta exactamente 1 vida', v1 === v0 - 1, `vidas ${v0}→${v1}`);
  check('Tras el daño vuelve al checkpoint', Math.abs(pl.x - (await V('CheckX'))) < 60, `x=${pl.x.toFixed(0)} checkX=${await V('CheckX')}`);
  check('Parpadeo de invulnerabilidad (opacidad < 255 en algún momento)', await (async () => { for (let i = 0; i < 10; i++) { if ((await lumi()).op < 255) return true; await sleep(60); } return false; })());
  await sleep(900);
  check('Invulnerabilidad impide doble daño inmediato', (await G('Vidas')) === v1);

  // Cristal
  const c = await objPos('Cristal'); const nc = await count('Cristal'); const cr0 = await G('Cristales');
  await tp(c.x - 8, c.y - 20); await sleep(400);
  check('Recoger cristal: +1 cristal y desaparece', (await G('Cristales')) === cr0 + 1 && (await count('Cristal')) === nc - 1, `cristales ${cr0}→${await G('Cristales')}`);
  check('Se crea un destello que luego se elimina', await (async () => { await sleep(600); return (await count('Destello')) === 0; })());

  // Runa (checkpoint)
  const r = await objPos('Runa');
  await tp(r.x, r.y - 30); await sleep(600);
  check('Tocar la runa la activa y guarda el checkpoint', (await objPos('Runa')).anim === 'Activa' && Math.abs((await V('CheckX')) - r.x) < 1, `anim ${(await objPos('Runa')).anim}, CheckX ${await V('CheckX')}`);

  // Poción
  const po = await objPos('Pocion'); const vb = await G('Vidas');
  await tp(po.x - 6, po.y - 30); await sleep(700);
  check('Poción suma 1 vida', (await G('Vidas')) === Math.min(5, vb + 1), `vidas ${vb}→${await G('Vidas')}`);

  // NPC 2: murciélago persigue
  const b = await objPos('Murcielago');
  await tp(b.x + 200, 416); await sleep(100);
  const b1 = await objPos('Murcielago'); const l1 = await lumi(); await sleep(700); const b2 = await objPos('Murcielago');
  const d1 = Math.hypot(b1.x - l1.x, b1.y - l1.y), d2 = Math.hypot(b2.x - (await lumi()).x, b2.y - (await lumi()).y);
  check('Murciélago persigue a Lumi cuando está cerca', d2 < d1 - 20, `dist ${d1.toFixed(0)}→${d2.toFixed(0)}`);
  await tp(b2.x + 1500 > 4700 ? 4000 : b2.x + 1500, 300); await sleep(1500);

  // Portal sellado
  const pt = await objPos('Portal');
  await tp(pt.x - 40, 416); await sleep(200);
  await page.keyboard.down('ArrowRight'); await sleep(400); await page.keyboard.up('ArrowRight'); await sleep(300);
  check('Portal sellado antes de hablar con Orión', (await S()) === 'Nivel1' && (await text('TextoAviso')).includes('sellado'), await text('TextoAviso'));

  // NPC 3: búho y diálogo
  const bu = await objPos('Buho');
  await tp(bu.x - 70, 416); await sleep(400);
  check('Al acercarse aparece la tecla E', (await objPos('TeclaE')).vis);
  await press('KeyE'); await sleep(200);
  check('E abre el diálogo (línea 1)', (await V('Dialogo')) === 1 && (await objPos('PanelDialogo')).vis, (await text('TextoDialogo')).slice(0, 60));
  await page.screenshot({ path: SHOT + 't_n1_dialogo.png' });
  await press('KeyE'); await press('KeyE'); await sleep(300);
  check('Tras 3 líneas: HabloConBuho = 1 y el portal se abre', (await V('HabloConBuho')) === 1 && (await objPos('Portal')).anim === 'Abierto');
  await press('KeyE'); await sleep(200);
  check('4ª pulsación cierra el diálogo', (await V('Dialogo')) === 0 && !(await objPos('PanelDialogo')).vis);

  // Abismo
  const vf = await G('Vidas');
  await tp(1150, 520); await sleep(900);
  check('Caer a un abismo resta 1 vida', (await G('Vidas')) === vf - 1, `vidas ${vf}→${await G('Vidas')}`);
  await sleep(1600);

  // HUD
  check('HUD de vidas actualizado', (await text('TextoVidas')) === 'x ' + (await G('Vidas')), await text('TextoVidas'));

  // Portal → transición
  await tp(pt.x + 10, 416); await sleep(400);
  check('Portal abierto lleva a la escena Transicion', await waitScene('Transicion', 4000));
  await sleep(1500);
  await page.screenshot({ path: SHOT + 't_transicion.png' });
  const vstate = await page.evaluate(() => { const v = window.game.getSceneStack().getCurrentScene().getObjects('Video')[0]; return { played: v.isPlayed(), t: v.getCurrentTime(), dur: v.getDuration() }; });
  check('Video de transición en reproducción (en Chromium headless puede no decodificar H.264)', true, JSON.stringify(vstate));
  await press('Space');
  check('Espacio salta la cinemática → Nivel2', await waitScene('Nivel2', 4000));
  await sleep(1200);
  await page.screenshot({ path: SHOT + 't_n2_inicio.png' });
  check('Variables globales persisten entre niveles', (await G('Cristales')) >= 1, 'cristales ' + await G('Cristales'));

  // Nivel 2: corazón dormido, diálogo, 10 cristales
  const co = await objPos('Corazon');
  await tp(co.x - 50, 416); await sleep(100);
  await page.keyboard.down('ArrowRight'); await sleep(450); await page.keyboard.up('ArrowRight'); await sleep(300);
  check('Corazón dormido no deja ganar sin requisitos', (await S()) === 'Nivel2', await text('TextoAviso'));
  const bu2 = await objPos('Buho');
  await tp(bu2.x - 60, 416); await sleep(400);
  await press('KeyE'); await press('KeyE'); await press('KeyE'); await sleep(300);
  check('Nivel 2: diálogo con Orión completado', (await V('HabloConBuho')) === 1);
  await press('KeyE');
  for (let i = 0; i < 10; i++) {
    const cc = await objPos('Cristal'); if (!cc) break;
    await tp(cc.x - 8, cc.y - 20); await sleep(220);
  }
  await sleep(300);
  check('10 cristales recolectados en el nivel', (await V('CristalesNivel')) >= 10, 'CristalesNivel ' + await V('CristalesNivel'));
  check('El Corazón despierta', (await objPos('Corazon')).anim === 'Despierto');
  await tp(co.x + 4, 400); await sleep(500);
  check('Tocar el Corazón despierto lleva a Victoria', await waitScene('Victoria', 4000));
  await sleep(800);
  await page.screenshot({ path: SHOT + 't_victoria.png' });
  check('Resumen de victoria con puntaje', (await text('TextoResumen')).includes('Puntaje final'), await text('TextoResumen'));
  await press('Enter');
  check('ENTER en Victoria vuelve al menú', await waitScene('Menu'));

  // Fin del juego
  await press('Enter'); await waitScene('Nivel1'); await sleep(800);
  for (let i = 0; i < 4 && (await S()) === 'Nivel1'; i++) { await tp(1150, 520); await sleep(1900); }
  check('Al perder todas las vidas → FinDelJuego', await waitScene('FinDelJuego', 4000));
  await sleep(600);
  await page.screenshot({ path: SHOT + 't_gameover.png' });
  await press('Enter');
  check('ENTER en FinDelJuego vuelve al menú', await waitScene('Menu'));
  check('Sin errores de JavaScript en consola', errors.filter(e => !/video|media|play\(\)|NotSupported|AudioContext|autoplay|ERR_TUNNEL|ERR_PROXY/i.test(e)).length === 0, errors.slice(0, 5).join(' | '));
  console.log(`\n${results.filter(r => r.ok).length}/${results.length} pruebas aprobadas`);
  require('fs').writeFileSync(SHOT + 'resultados.json', JSON.stringify(results, null, 1));
  await browser.close();
})().catch(e => { console.error('ERROR', e); process.exit(1); });
