# Text-to-Speech Videos

Aplicación local para generar voces narradas en español a partir de textos o guiones, usando Microsoft Edge TTS. El proyecto combina una interfaz web moderna con una herramienta de línea de comandos para producir archivos de audio listos para usar en videos, anuncios, tutoriales y presentaciones.

## Descripción general

Este repositorio permite:

- convertir textos largos o cortos en audio con voces naturales de Microsoft Edge TTS;
- ajustar velocidad y tono de la voz;
- generar archivos MP3 locales;
- probar fragmentos de audio antes de renderizar el archivo completo;
- operar desde navegador o desde consola.

La solución está pensada para uso profesional, local y rápido, sin depender de servicios externos complejos ni de un backend pesado.

## Características principales

- Interfaz web con diseño oscuro y estilo premium.
- Generación de audio con voces neuronales en español.
- Soporte para texto directo o archivos .txt.
- Ajuste de velocidad y tono mediante controles visuales.
- Reproducción previa de fragmentos antes de exportar.
- Exportación de archivos MP3 en la carpeta de salida.
- CLI para automatizar generación por lotes o scripts.

## Estructura del proyecto

```text
.
+-- app.py               # Servidor web y lógica backend local
+-- index.html           # Frontend web de la interfaz de usuario
+-- narrador.py          # Script de consola para TTS por CLI
+-- requirements.txt     # Dependencias del proyecto
+-- texto_ejemplo.txt    # Texto de ejemplo para pruebas
+-- README.md            # Documentación del proyecto
+-- salidas/             # Carpeta de salida para archivos audio
+-- logseq/              # Archivos de notas o contenido auxiliar
+-- pages/               # Páginas de documentación del proyecto
+-- whiteboards/         # Datos de whiteboard del flujo de trabajo
+-- journals/            # Registros del proyecto
+-- venv/                # Entorno virtual local (ignorado por git)
+-- .gitignore           # Reglas para excluir artefactos locales
+-- voces.xlsx           # Archivo de referencia de voces
```

## Requisitos

- Python 3.8 o superior
- Internet para acceder al servicio de voces de Microsoft Edge
- Sistema operativo compatible con Python: Windows, macOS o Linux

## Instalación

1. Clona el repositorio o entra a la carpeta del proyecto.
2. Crea un entorno virtual.

```powershell
python -m venv venv
```

3. Activa el entorno virtual.

```powershell
.\venv\Scripts\Activate.ps1
```

4. Instala las dependencias.

```powershell
pip install -r requirements.txt
```

## Uso web

Inicia la aplicación:

```powershell
python app.py
```

Luego abre en tu navegador:

```text
http://localhost:8000
```

Desde la interfaz puedes:

- escribir o pegar texto;
- elegir una voz;
- ajustar velocidad y tono;
- escuchar una vista previa corta;
- generar y descargar el audio completo.

## Uso desde línea de comandos

Ejemplo básico:

```powershell
.\venv\Scripts\python.exe narrador.py --texto "¡Oferta especial de fin de año! Compra ahora y obtén 50% de descuento." --voz es-ES-AlvaroNeural --velocidad +15% --salida promocion.mp3
```

Parámetros principales:

- -t, --texto: texto directo para sintetizar.
- -f, --archivo: ruta a un archivo .txt.
- -v, --voz: identificador de la voz.
- -r, --velocidad: velocidad de lectura.
- -p, --tono: tono de la voz.
- -o, --salida: nombre del archivo de salida.
- --list-voces: lista voces recomendadas y disponibles.

## Voces recomendadas en español

| Voz | Región | Tipo | Uso recomendado |
| --- | --- | --- | --- |
| es-MX-JorgeNeural | México | Masculino | promociones y anuncios muy dinámicos |
| es-MX-DaliaNeural | México | Femenino | ventas y narración cálida |
| es-ES-AlvaroNeural | España | Masculino | tonos profesionales y corporativos |
| es-ES-ElviraNeural | España | Femenino | narración formal y clara |
| es-CO-GonzaloNeural | Colombia | Masculino | tutoriales y explicaciones |
| es-CO-SalomeNeural | Colombia | Femenino | contenido institucional y amable |

## Flujo de trabajo sugerido

1. Escribe el guion en el editor o en un archivo .txt.
2. Ajusta la voz, velocidad y tono.
3. Reproduce una vista previa.
4. Genera el audio final.
5. Guarda el archivo en la carpeta salidas.
6. Importa el audio al proyecto de video final en DaVinci Resolve o edición de video.

## Licencia

Este proyecto se distribuye con fines educativos y de desarrollo local. Puedes adaptarlo según tus necesidades personales o profesionales.

## Autor o nota

Proyecto orientado a la generación de voces profesionales para contenido audiovisual y narración de guiones de marketing, tutoriales, presentaciones y videos digitales.
