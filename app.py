#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import urllib.parse
import asyncio
import edge_tts
from datetime import datetime
import sys

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "salidas")

# Crear carpeta de salidas si no existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Voces predefinidas recomendadas en español para respuesta rápida
VOCES_PREDEFINIDAS = [
    {"ShortName": "es-MX-JorgeNeural", "Locale": "es-MX", "Gender": "Male", "FriendlyName": "México (Jorge) - Enérgico/Comercial"},
    {"ShortName": "es-MX-DaliaNeural", "Locale": "es-MX", "Gender": "Female", "FriendlyName": "México (Dalia) - Cálida/Persuasiva"},
    {"ShortName": "es-ES-AlvaroNeural", "Locale": "es-ES", "Gender": "Male", "FriendlyName": "España (Álvaro) - Profesional/Claro"},
    {"ShortName": "es-ES-ElviraNeural", "Locale": "es-ES", "Gender": "Female", "FriendlyName": "España (Elvira) - Corporativo/Formal"},
    {"ShortName": "es-CO-GonzaloNeural", "Locale": "es-CO", "Gender": "Male", "FriendlyName": "Colombia (Gonzalo) - Expresivo/Neutro"},
    {"ShortName": "es-CO-SalomeNeural", "Locale": "es-CO", "Gender": "Female", "FriendlyName": "Colombia (Salomé) - Claro/Corporativo"},
    {"ShortName": "es-AR-TomasNeural", "Locale": "es-AR", "Gender": "Male", "FriendlyName": "Argentina (Tomás) - Expresivo/Natural"},
    {"ShortName": "es-AR-ElenaNeural", "Locale": "es-AR", "Gender": "Female", "FriendlyName": "Argentina (Elena) - Dulce/Narrativa"},
    {"ShortName": "es-US-AlonsoNeural", "Locale": "es-US", "Gender": "Male", "FriendlyName": "EE.UU. (Alonso) - Latino Neutro"},
    {"ShortName": "es-US-PalomaNeural", "Locale": "es-US", "Gender": "Female", "FriendlyName": "EE.UU. (Paloma) - Latino Neutro/Fluido"}
]

async def list_all_voices():
    """Obtiene la lista completa de voces en español desde edge_tts."""
    try:
        all_voices = await edge_tts.list_voices()
        # Filtrar solo voces en español
        spanish_voices = [
            {
                "ShortName": v["Name"],
                "Locale": v["Locale"],
                "Gender": v["Gender"],
                "FriendlyName": f"{v['Locale']} - {v['Name'].split('-')[-1].replace('Neural', '')} ({'Hombre' if v['Gender']=='Male' else 'Mujer'})"
            }
            for v in all_voices if v["Locale"].startswith("es-")
        ]
        return spanish_voices
    except Exception as e:
        print(f"[!] Error al listar voces online, usando lista local: {e}")
        return VOCES_PREDEFINIDAS

class RequestHandler(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Desactivar logs estándar en consola para no saturar, podemos imprimir los relevantes manual
        pass

    def send_json(self, data, status=200):
        try:
            response_bytes = json.dumps(data).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(response_bytes))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response_bytes)
        except Exception as e:
            print(f"[ERROR] Error enviando JSON: {e}")

    def serve_file(self, file_path, content_type):
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_error(404, "File not found")
            return

        try:
            file_size = os.path.getsize(file_path)
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', file_size)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open(file_path, 'rb') as f:
                # Escribir en bloques para no saturar memoria con archivos grandes
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except Exception as e:
            print(f"[ERROR] Error sirviendo archivo {file_path}: {e}")

    def do_OPTIONS(self):
        # Manejo de peticiones CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # 1. Página Principal (index.html)
        if path == "/" or path == "/index.html":
            self.serve_file(os.path.join(BASE_DIR, "index.html"), "text/html; charset=utf-8")
            return

        # 2. Servir audios generados
        elif path.startswith("/salidas/"):
            # Decodificar URL para soportar espacios en nombres de archivo
            filename = urllib.parse.unquote(path[len("/salidas/"):])
            # Prevenir ataques de path traversal
            filename = os.path.basename(filename)
            file_path = os.path.join(OUTPUT_DIR, filename)
            self.serve_file(file_path, "audio/mpeg")
            return

        # 3. API: Obtener voces en español
        elif path == "/api/voices":
            print("[+] API: Solicitando voces...")
            try:
                voices = asyncio.run(list_all_voices())
                self.send_json(voices)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # 4. API: Obtener lista de audios generados
        elif path == "/api/audios":
            try:
                audios = []
                for file in os.listdir(OUTPUT_DIR):
                    if file.lower().endswith(".mp3"):
                        path_file = os.path.join(OUTPUT_DIR, file)
                        stats = os.stat(path_file)
                        created_time = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        audios.append({
                            "name": file,
                            "size_bytes": stats.st_size,
                            "size_formatted": f"{stats.st_size / (1024*1024):.2f} MB",
                            "created": created_time,
                            "url": f"/salidas/{urllib.parse.quote(file)}"
                        })
                # Ordenar por fecha de modificación, más nuevos primero
                audios.sort(key=lambda x: x["created"], reverse=True)
                self.send_json(audios)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # Ruta por defecto
        self.send_error(404, "Not found")

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # 1. API: Generar audio a partir de texto
        if path == "/api/generate":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                params = json.loads(post_data)
                texto = params.get("text", "").strip()
                voz = params.get("voice", "es-MX-JorgeNeural")
                velocidad = params.get("rate", "+0%")
                tono = params.get("pitch", "+0Hz")
                nombre_archivo = params.get("filename", "").strip()

                if not texto:
                    self.send_json({"error": "El texto no puede estar vacío"}, 400)
                    return

                # Normalizar nombre del archivo
                if not nombre_archivo:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nombre_archivo = f"audio_{timestamp}.mp3"
                else:
                    # Sanitizar nombre
                    nombre_archivo = "".join([c for c in nombre_archivo if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).strip()
                    if not nombre_archivo:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        nombre_archivo = f"audio_{timestamp}.mp3"
                    else:
                        nombre_archivo += ".mp3"

                file_path = os.path.join(OUTPUT_DIR, nombre_archivo)

                print(f"[+] API: Generando audio en venv...")
                print(f"    - Archivo: {nombre_archivo}")
                print(f"    - Longitud texto: {len(texto)} caracteres")
                print(f"    - Voz: {voz} | Velocidad: {velocidad} | Tono: {tono}")

                # Ejecutar edge-tts asíncronamente
                async def run_tts():
                    communicate = edge_tts.Communicate(texto, voz, rate=velocidad, pitch=tono)
                    await communicate.save(file_path)

                asyncio.run(run_tts())

                print(f"[OK] Audio guardado: {nombre_archivo}")
                self.send_json({
                    "success": True,
                    "filename": nombre_archivo,
                    "url": f"/salidas/{urllib.parse.quote(nombre_archivo)}"
                })

            except json.JSONDecodeError:
                self.send_json({"error": "JSON Inválido"}, 400)
            except Exception as e:
                print(f"[ERROR] Error en generación de audio: {e}")
                self.send_json({"error": str(e)}, 500)
            return

        self.send_error(404, "Not found")

    def do_DELETE(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # 1. API: Eliminar un audio
        if path == "/api/audios":
            query = urllib.parse.parse_qs(parsed_url.query)
            filename = query.get("name", [None])[0]

            if not filename:
                self.send_json({"error": "Se requiere especificar el parámetro 'name'"}, 400)
                return

            # Sanitizar nombre
            filename = os.path.basename(filename)
            file_path = os.path.join(OUTPUT_DIR, filename)

            if not os.path.exists(file_path):
                self.send_json({"error": "El archivo no existe"}, 404)
                return

            try:
                os.remove(file_path)
                print(f"[i] Archivo eliminado: {filename}")
                self.send_json({"success": True, "message": f"Archivo {filename} eliminado"})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        self.send_error(404, "Not found")

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    # Permite al servidor web manejar peticiones en hilos separados sin bloquearse
    daemon_threads = True

def run():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    print(f"\n========================================================")
    print(f"[OK] Servidor de Narracion Comercial AI Iniciado")
    print(f"     Abre en tu navegador: http://localhost:{PORT}")
    print(f"     Carpeta de audios fisicos: {OUTPUT_DIR}")
    print(f"     Presiona Ctrl+C para detener el servidor")
    print(f"========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[i] Deteniendo servidor...")
        httpd.server_close()
        sys.exit(0)

if __name__ == '__main__':
    run()
