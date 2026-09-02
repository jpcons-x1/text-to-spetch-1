# Narrador Comercial AI - Conversor de Texto a Voz (Edge TTS)

Este proyecto implementa una solución local y profesional para convertir guiones y textos en narraciones de voz comercial de alta calidad en español. Utiliza la tecnología de síntesis de voz neuronal de Microsoft Edge a través de la librería `edge-tts`, lo que permite obtener locuciones humanas realistas con ajuste fino de velocidad y tono.

El proyecto está diseñado para funcionar de dos formas complementarias:
1.  **Terminal (CLI - `narrador.py`)**: Para procesamiento por lotes o conversiones rápidas de archivos de texto directamente desde la línea de comandos.
2.  **Interfaz Gráfica Local (Web Dashboard - `app.py` + `index.html`)**: Una aplicación web interactiva y moderna (diseño premium estilo modo oscuro con efecto *glassmorphism*) que permite escribir guiones, previsualizar locuciones cortas en tiempo real, ajustar velocidad y tono mediante sliders, y gestionar las descargas directamente desde el navegador.

---
- ## Estructura del Proyecto
  
  ```text
  ├── venv/                # Entorno virtual de Python (aislado)
  ├── salidas/             # Directorio de almacenamiento físico de audios (.mp3)
  ├── requirements.txt     # Archivo de dependencias (edge-tts)
  ├── narrador.py          # Script CLI interactivo
  ├── app.py               # Servidor web local de API y archivos
  ├── index.html           # Dashboard frontend premium
  ├── texto_ejemplo.txt    # Ejemplo de guión de ventas para pruebas
  └── README.md            # Documentación del proyecto (este archivo)
  ```
  
  ---
- ## Detalles de la Arquitectura
  
  ```mermaid
  graph TD
    User([Usuario]) -->|Usa CLI| CLI[narrador.py]
    User -->|Usa Navegador| Web[index.html]
    Web -->|API Requests| Server[app.py HTTP Server]
    CLI -->|asyncio| EdgeTTS[edge-tts Library]
    Server -->|asyncio| EdgeTTS
    EdgeTTS -->|WebSockets| MS[Microsoft Azure TTS Service]
    MS -->|Audio Stream| EdgeTTS
    EdgeTTS -->|Guarda .mp3| Folder[(salidas/)]
    Server -->|Sirve .mp3 y datos| Web
  ```
- ### Componentes:
  *   **Backend (Python Standard Library):** Implementado con `http.server.BaseHTTPRequestHandler` y `socketserver.ThreadingMixIn` para habilitar el procesamiento en hilos separados sin necesidad de dependencias robustas como Django o FastAPI.
  *   **Motor TTS (edge-tts):** Se conecta a los servicios de locución neuronal de Microsoft a través de WebSockets de manera asíncrona mediante `asyncio`.
  *   **Frontend (HTML5 + CSS + JavaScript Vanilla):** Diseñado con un sistema de cuadrícula responsivo, animaciones dinámicas, sliders fluidos y un reproductor de audio nativo personalizado. Utiliza [Lucide Icons](https://lucide.dev/) para la iconografía y fuentes de Google Fonts (Outfit & Inter).
  
  ---
- ## Especificaciones y Requisitos
  
  *   **Sistema Operativo:** Windows, macOS o Linux (probado en Windows con PowerShell y CMD).
  *   **Python:** Versión `3.7` o superior (probado con Python `3.13.11`).
  *   **Conexión a Internet:** Requerida durante la generación de audio (ya que la librería se comunica directamente con las APIs de voz de Microsoft Edge).
  *   **Espacio de Almacenamiento:** Mínimo (menos de 50 MB para la instalación; los audios MP3 ocupan ~1 MB por cada 10 minutos de locución).
  
  ---
- ## Instrucciones de Instalación y Configuración
  
  Sigue estos pasos en tu terminal para configurar el proyecto en un entorno virtual aislado:
- ### 1. Clonar o Ubicarse en el Proyecto
  Abre la consola en el directorio raíz del proyecto:
  `d:/11.DaVinci_Resolve_20_curso/TEXTTOSPETCH-VIDEOS`
- ### 2. Crear el Entorno Virtual
  Crea un entorno de Python llamado `venv` para no instalar dependencias globales:
  ```powershell
  python -m venv venv
  ```
- ### 3. Instalar Dependencias
  Instala los paquetes necesarios directamente en el entorno virtual:
  ```powershell
  # En Windows (PowerShell/CMD)
  .\venv\Scripts\pip.exe install -r requirements.txt
  ```
  
  ---
- ## Guía de Uso
- ### 1. Interfaz Web (Recomendado)
  
  La interfaz visual te permite ajustar de manera interactiva la velocidad de la voz, el tono y probar fragmentos antes de renderizar audios completos.
  
  1.  **Inicia el servidor local:**
    ```powershell
    .\venv\Scripts\python.exe app.py
    ```
  2.  **Abre el Dashboard en tu navegador:**
    Ve a [http://localhost:8000](http://localhost:8000).
  3.  **Dinámica de Uso:**
    *   Escribe tu texto en el editor principal.
    *   Selecciona tu voz y escribe un nombre para tu archivo.
    *   Usa los controles deslizantes para acelerar/ralentizar la voz u oscurecer/agudizar el tono.
    *   Haz clic en **Probar Fragmento** para escuchar los primeros 100 caracteres.
    *   Haz clic en **Generar Audio Completo** para guardarlo en la lista. Puedes descargarlo o eliminarlo usando los controles de la tarjeta.
  
  ---
- ### 2. Consola de Comandos (CLI)
  
  Puedes usar `narrador.py` para procesar textos de forma directa.
- #### Parámetros Disponibles:
  *   `-t`, `--texto`: Texto directo a sintetizar (entre comillas).
  *   `-f`, `--archivo`: Ruta de un archivo `.txt` que contiene el guión.
  *   `-v`, `--voz`: Identificador de la voz de Edge TTS (defecto: `es-MX-JorgeNeural`).
  *   `-r`, `--velocidad`: Velocidad de la voz en porcentaje (ej: `+10%`, `-5%`).
  *   `-p`, `--tono`: Tono de la voz en Hertz (ej: `+5Hz`, `-3Hz`).
  *   `-o`, `--salida`: Nombre del archivo de salida en `salidas/` (ej: `promo_ventas.mp3`).
  *   `--list-voces`: Lista en la consola las voces recomendadas en español.
- .\venv\Scripts\python.exe narrador.py --texto "¡Oferta especial de fin de año! Compra ahora y obtén 50% de descuento." --voz es-ES-AlvaroNeural --velocidad +15% --salida promocion.mp3
- ## Voces Neuronal Recomendadas en Español
  
  | Código de Voz | Región / Acento | Género | Tono de Voz y Uso Recomendado |
  | :--- | :--- | :--- | :--- |
  | **`es-MX-JorgeNeural`** | México | Masculino | **Muy enérgico, vendedor, persuasivo.** Ideal para anuncios y promociones de alto impacto. |
  | **`es-MX-DaliaNeural`** | México | Femenino | **Cálido, profesional y asertivo.** Excelente para videos explicativos y ventas suaves. |
  | **`es-ES-AlvaroNeural`** | España | Masculino | **Corporativo, formal, locutor maduro.** Recomendado para videos de negocios y documentales corporativos. |
  | **`es-ES-ElviraNeural`** | España | Femenino | **Limpio, pausado, institucional.** Excelente para narración corporativa y e-learning. |
  | **`es-CO-GonzaloNeural`** | Colombia | Masculino | **Neutro, expresivo, amigable.** Estilo tutoriales y videos explicativos en YouTube. |
  | **`es-CO-SalomeNeural`** | Colombia | Femenino | **Profesional, claro.** Perfecto para centralitas telefónicas y videos institucionales. |
  | **`es-US-AlonsoNeural`** | EE.UU. / Latino | Masculino | **Latino neutro, moderno y juvenil.** Recomendado para narrar redes sociales (TikTok/Reels). |
  | **`es-US-PalomaNeural`** | EE.UU. / Latino | Femenino | **Latino neutro, fluido.** Ideal para audiolibros y podcasts. |
  
  *(Nota: Para obtener un listado de todas las voces disponibles en la nube de Microsoft Edge, ejecuta `.\venv\Scripts\python.exe -m edge_tts --list-voices` en tu terminal).*