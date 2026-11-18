import base64, json, re
from pathlib import Path
from shutil import which
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]
CSS=(R/'assets/css/style.css').read_text(encoding='utf8')
JS=(R/'assets/js/script.js').read_text(encoding='utf8')

def embed(page_name):
    html=(R/page_name).read_text(encoding='utf8')
    html=html.replace('<link rel="stylesheet" href="assets/css/style.css">',f'<style>\n{CSS}\n</style>')
    html=html.replace('<script src="assets/js/script.js" defer></script>', '')
    # Both SVG icons and source CSS are placed inline solely in the QA browser.
    for image in (R/'assets/img').glob('*.svg'):
        data=base64.b64encode(image.read_bytes()).decode('ascii')
        html=html.replace('assets/img/'+image.name, 'data:image/svg+xml;base64,'+data)
    return html.replace('</body>', f'<script>\n{JS}\n</script>\n</body>')

home_html=embed('index.html')
detail_html=embed('detalle.html')
probes=[]
def check(cond, desc):
    probes.append({'prueba':desc,'resultado':'CORRECTO' if cond else 'FALLÓ'})
    if not cond: print('FALLO',desc)
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=which('chromium') or which('chromium-browser') or None, headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
    for label,width,height,cols in [('movil',390,844,1),('tableta',820,980,2),('escritorio',1366,900,3)]:
        page=browser.new_page(viewport={'width':width,'height':height}, device_scale_factor=1, color_scheme='light')
        errors=[]
        page.on('pageerror',lambda ex:errors.append(str(ex)))
        page.set_content(home_html,wait_until='load')
        page.screenshot(path=str(R/'evidencias'/f'{label}_inicio.png'))
        n=len(page.evaluate('getComputedStyle(document.querySelector(".grid-servicios")).gridTemplateColumns.trim().split(/\\s+/).filter(Boolean)'))
        check(n==cols,f'Grid {label}: {n} columnas (esperadas {cols})')
        overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1')
        check(not overflow,f'Sin desplazamiento horizontal en {label} ({width}px)')
        page.locator('.grid-servicios').scroll_into_view_if_needed()
        page.screenshot(path=str(R/'evidencias'/f'{label}_servicios.png'))
        check(not errors,f'Sin errores JavaScript en {label}')
        if label=='escritorio':
            page.locator('#buscar-servicio').fill('reciclaje')
            check(page.locator('.tarjeta-servicio:visible').count()==1,'Buscador: 1 coincidencia para reciclaje')
            page.locator('#buscar-servicio').fill('')
            check(page.locator('.tarjeta-servicio:visible').count()==6,'Buscador restaura las 6 tarjetas')
            check(page.locator('a[href="detalle.html?servicio=agua"]').count()==1,'Enlace de detalle de agua definido correctamente')
            page.locator('#nombre').fill('Nombre Ejemplo')
            page.locator('#correo').fill('ejemplo@correo.com')
            page.locator('#servicio-contacto').select_option(label='Reciclaje y residuos')
            page.locator('#mensaje').fill('Consulta de ejemplo para comprobar el formulario.')
            page.get_by_role('button',name='Simular solicitud').click()
            check(page.locator('#respuesta-formulario').is_visible(),'Formulario muestra confirmación de simulación')
            check('No se envió información' in page.locator('#respuesta-formulario').inner_text(),'Formulario aclara que no hay envío de datos')
            page.locator('#contacto').scroll_into_view_if_needed()
            page.screenshot(path=str(R/'evidencias'/'formulario_validacion.png'))
            page.set_content(home_html,wait_until='load')
            page.keyboard.press('Tab')
            check(page.evaluate('document.activeElement.classList.contains("saltar-contenido")'),'Primer enlace de teclado salta al contenido')
            check(page.evaluate('getComputedStyle(document.activeElement).outlineStyle')!='none','Enlace de salto tiene foco visual')
        page.close()
    detail=browser.new_page(viewport={'width':900,'height':860},color_scheme='light')
    detail.goto('about:blank?servicio=agua')
    detail.set_content(detail_html,wait_until='load')
    check(detail.locator('#detalle-titulo').inner_text()=='Agua y saneamiento','Página de detalle renderiza agua según parámetro URL')
    check(detail.locator('#detalle-pasos li').count()==3,'Detalle muestra 3 pasos de orientación')
    detail.locator('#detalle-imagen').evaluate('(el, uri) => el.src = uri', 'data:image/svg+xml;base64,'+base64.b64encode((R/'assets/img/agua.svg').read_bytes()).decode('ascii'))
    detail.screenshot(path=str(R/'evidencias'/'detalle_agua.png'))
    detail.close()
    invalid=browser.new_page(viewport={'width':900,'height':860})
    invalid.goto('about:blank?servicio=inexistente')
    invalid.set_content(detail_html)
    check(invalid.locator('#detalle-titulo').inner_text()=='Servicio no encontrado','Ruta inválida muestra mensaje claro')
    invalid.close()
    dark=browser.new_page(viewport={'width':390,'height':844}, color_scheme='dark')
    dark.set_content(home_html)
    check(dark.evaluate('getComputedStyle(document.body).backgroundColor')=='rgb(15, 23, 42)','Modo oscuro aplicado según preferencia del sistema')
    dark.locator('.grid-servicios').scroll_into_view_if_needed()
    dark.screenshot(path=str(R/'evidencias'/'movil_modo_oscuro.png'))
    dark.close()
    browser.close()
(R/'evidencias'/'validaciones.json').write_text(json.dumps(probes, ensure_ascii=False,indent=2),encoding='utf8')
(R/'evidencias'/'resultados_pruebas.txt').write_text('PRUEBAS DE NAVEGADOR (CHROMIUM, contenido local incrustado solo en QA)\n'+ '\n'.join(f"{r['resultado']}: {r['prueba']}" for r in probes)+'\n',encoding='utf8')
print(json.dumps(probes,ensure_ascii=False,indent=2))
