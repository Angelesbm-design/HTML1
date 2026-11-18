# Portal de Servicios Ciudadanos — Práctica M2

Sitio web **responsivo y demostrativo** realizado como práctica escolar de Desarrollo de páginas web. Se desarrolló a partir de las instrucciones del manual «M2. Práctica 2: Portal de Servicios Ciudadanos, responsivo».

> **Aviso:** No es un sitio gubernamental ni ofrece trámites, citas, domicilios o formularios oficiales. Todas las referencias a oficinas son ilustrativas. El formulario funciona exclusivamente dentro del navegador y **no envía ni guarda información**.

## Cómo ejecutar

1. Descomprime la carpeta `portal-servicios` si recibiste un ZIP.
2. Abre `index.html` en Chrome, Firefox o Edge (sin instalar dependencias).
3. Usa el menú para navegar a Inicio, Servicios, Requisitos, Ubicación y Contacto.
4. Selecciona «Ver detalle del servicio» para abrir `detalle.html?servicio=...`.
5. Opcional: abre la carpeta en VS Code y utiliza Live Server o ejecuta `python -m http.server 8000` desde la raíz; visita `http://localhost:8000`.

## Estructura

```text
portal-servicios/
├── index.html                 Página principal con las cinco secciones
├── detalle.html               Plantilla de detalle de cada servicio
├── assets/
│   ├── css/style.css          Estilos, Grid, Flexbox, variables, @media
│   ├── img/*.svg              Seis íconos SVG originales y locales
│   └── js/script.js           Búsqueda, ficha de servicio y formulario simulado
├── evidencias/                Capturas reales en varias resoluciones
├── tests/test_structure.py    Comprobaciones automatizadas estructurales
├── tests/probar_responsividad.py  Comprobaciones visuales opcionales
└── README.md                  Este documento
```

## Diseño y accesibilidad

- HTML5 semántico: `header`, `nav`, `main`, `section`, `article`, `footer`.
- Adaptación **mobile-first**: 1 columna bajo 768 px, 2 desde 768 px, 3 desde 1024 px.
- CSS Grid: estructura del sitio, distribución de tarjetas y secciones.
- Flexbox: menú, botones y agrupación de controles.
- Variables CSS, unidades `rem`, porcentajes y tipografía fluida `clamp()`.
- Colores de alto contraste, alternativa oscura `prefers-color-scheme: dark` y adaptación a `prefers-reduced-motion`.
- Acceso por teclado y enlace «Ir al contenido principal», indicadores de enfoque, `aria-label`, roles de estado, títulos y textos `alt` descriptivos.
- Enlaces de tarjetas a fichas detalladas con requisitos y pasos de ejemplo.
- Buscador con recuento en vivo; formulario con validación nativa y confirmación local.

## Verificaciones

Ejecuta desde la raíz del proyecto:

```bash
python -m unittest discover -s tests -v
```

Opcionalmente, para repetir las comprobaciones de navegador y regenerar las capturas, instala Playwright (`pip install playwright` y `python -m playwright install chromium`) y ejecuta `python tests/probar_responsividad.py`. Las capturas de esta entrega se obtuvieron con Chromium, cargando el HTML, CSS, JS y los SVG locales directamente en la prueba (sin solicitudes de red).

Para revisar visualmente: abre herramientas de desarrollo con F12, activa el modo dispositivo y establece anchos de 390 px, 820 px y 1366 px. Revisa el menú y las tarjetas, y confirma que no haya desplazamiento horizontal.

## Publicar en GitHub Pages (opcional)

1. Crea un repositorio y sube el **contenido** de `portal-servicios` (con `index.html` en la raíz).
2. En GitHub ve a **Settings > Pages**.
3. Selecciona **Deploy from a branch**, la rama principal y carpeta **/(root)**.
4. Al terminar la publicación, GitHub Pages mostrará tu URL pública; todos los enlaces son relativos y funcionan allí.

## Referencia

Material proporcionado por la actividad: *Manual de práctica: Portal de Servicios Ciudadanos, responsivo*, M2. Desarrollo de páginas web, pp. 1–11. Las descripciones y requisitos del sitio son **ejemplos pedagógicos**, no información oficial.
