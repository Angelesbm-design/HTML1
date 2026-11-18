"""Pruebas estáticas sin dependencias externas: python -m unittest discover -s tests -v"""
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = set()
        self.links = []
        self.images = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag == 'img': self.images.append(a)
        if tag == 'script' and a.get('src'): self.scripts.append(a['src'])

class PruebasPortal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = Extractor(); cls.home.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
        cls.detail = Extractor(); cls.detail.feed((ROOT / 'detalle.html').read_text(encoding='utf-8'))
        cls.css = (ROOT / 'assets/css/style.css').read_text(encoding='utf-8')
        cls.js = (ROOT / 'assets/js/script.js').read_text(encoding='utf-8')

    def test_secciones_requeridas(self):
        for nombre in ['inicio','servicios','requisitos','ubicacion','contacto']:
            with self.subTest(seccion=nombre): self.assertIn(nombre, self.home.ids)

    def test_etiquetas_semanticas(self):
        for etiqueta in ['header','nav','main','section','article','footer']:
            with self.subTest(etiqueta=etiqueta): self.assertIn(etiqueta, self.home.tags)

    def test_imagenes_locales_y_alt(self):
        for img in self.home.images + self.detail.images:
            self.assertTrue(img.get('alt'), f'Falta texto alt en {img}')
            self.assertTrue((ROOT / img['src']).is_file(), f'Imagen inexistente: {img["src"]}')
        for ruta in (ROOT / 'assets/img').glob('*.svg'):
            ET.parse(ruta)  # SVG válido como XML.

    def test_enlaces_internos_existentes(self):
        for parser in [self.home, self.detail]:
            for href in parser.links:
                destino = urlparse(href)
                ruta = destino.path
                if ruta:
                    self.assertTrue((ROOT / ruta).is_file(), f'Ruta rota: {href}')
                if destino.fragment and not ruta:
                    self.assertIn(destino.fragment, parser.ids, f'Ancla rota: {href}')
                if destino.fragment and ruta:
                    otro = self.home if ruta == 'index.html' else self.detail
                    self.assertIn(destino.fragment, otro.ids, f'Ancla rota: {href}')

    def test_seis_tarjetas_con_detalle(self):
        html = (ROOT / 'index.html').read_text(encoding='utf-8')
        self.assertEqual(len(re.findall('class="tarjeta-servicio"', html)), 6)
        self.assertEqual(len(re.findall(r'href="detalle\.html\?servicio=', html)), 6)

    def test_estilos_responsivos(self):
        for token in ['display: grid','display: flex','@media (min-width: 768px)','@media (min-width: 1024px)','clamp(',':root','prefers-color-scheme: dark']:
            with self.subTest(css=token): self.assertIn(token, self.css)

    def test_js_y_dependencias_locales(self):
        for script in self.home.scripts + self.detail.scripts:
            self.assertTrue((ROOT / script).is_file(), f'Falta script: {script}')
        for nombre in ['configurarBusqueda','configurarPaginaDetalle','configurarFormulario']:
            self.assertIn(nombre, self.js)

    def test_formulario_explicito_demostracion(self):
        html = (ROOT / 'index.html').read_text(encoding='utf-8')
        self.assertIn('No se envían datos', html)
        self.assertIn('formulario-contacto', html)
        self.assertIn('evento.preventDefault()', self.js)

if __name__ == '__main__':
    unittest.main()
