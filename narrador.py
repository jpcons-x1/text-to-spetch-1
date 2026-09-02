#!/usr/bin/env python3
import asyncio
import os
import sys
import argparse
from datetime import datetime
import edge_tts

# Directorio por defecto para las salidas
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salidas")

# Voces en español recomendadas
VOCES_RECOMENDADAS = {
    "es-MX-JorgeNeural": "México (Hombre) - Comercial y enérgico",
    "es-MX-DaliaNeural": "México (Mujer) - Cálida y persuasiva",
    "es-ES-AlvaroNeural": "España (Hombre) - Profesional y claro",
    "es-ES-ElviraNeural": "España (Mujer) - Corporativa y formal",
    "es-CO-GonzaloNeural": "Colombia (Hombre) - Expresivo y pausado",
    "es-CO-SalomeNeural": "Colombia (Mujer) - Limpia y neutra",
    "es-US-AlonsoNeural": "EE. UU. (Hombre) - Latino neutro, moderno",
    "es-US-PalomaNeural": "EE. UU. (Mujer) - Latino neutro, profesional"
}

async def generar_audio(texto, voz, velocidad, tono, ruta_salida):
    """
    Genera el audio usando edge_tts.Communicate.
    """
    # edge-tts requiere el formato de velocidad como '+10%' o '-5%' y tono como '+0Hz'
    rate_str = velocidad if (velocidad.startswith('+') or velocidad.startswith('-')) else f"+{velocidad}"
    if not rate_str.endswith('%'):
        rate_str += '%'
        
    pitch_str = tono if (tono.startswith('+') or tono.startswith('-')) else f"+{tono}"
    if not pitch_str.endswith('Hz'):
        pitch_str += 'Hz'

    print(f"\n[+] Generando audio...")
    print(f"    - Voz: {voz}")
    print(f"    - Velocidad (Rate): {rate_str}")
    print(f"    - Tono (Pitch): {pitch_str}")
    print(f"    - Destino: {ruta_salida}\n")

    try:
        communicate = edge_tts.Communicate(texto, voz, rate=rate_str, pitch=pitch_str)
        await communicate.save(ruta_salida)
        print(f"[OK] Audio generado exitosamente en: {ruta_salida}")
    except Exception as e:
        print(f"[ERROR] Error al generar el audio: {e}", file=sys.stderr)
        sys.exit(1)

def mostrar_voces():
    print("\n--- VOCES RECOMENDADAS EN ESPAÑOL ---")
    for key, desc in VOCES_RECOMENDADAS.items():
        print(f" * {key:<20} | {desc}")
    print("\nPara ver la lista completa de todas las voces disponibles ejecute: python -m edge_tts --list-voices\n")

def main():
    parser = argparse.ArgumentParser(
        description="Convertidor de Texto a Voz Comercial en Español con Edge TTS"
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--texto", type=str, help="Texto a convertir a voz")
    group.add_argument("-f", "--archivo", type=str, help="Archivo de texto (.txt) a leer")
    
    parser.add_argument("-v", "--voz", type=str, default="es-MX-JorgeNeural",
                        help="Voz de Edge TTS (defecto: es-MX-JorgeNeural)")
    parser.add_argument("-r", "--velocidad", type=str, default="+0%",
                        help="Ajuste de velocidad, ej: +10%% o -5%% (defecto: +0%%)")
    parser.add_argument("-p", "--tono", type=str, default="+0Hz",
                        help="Ajuste de tono, ej: +5Hz o -3Hz (defecto: +0Hz)")
    parser.add_argument("-o", "--salida", type=str,
                        help="Nombre del archivo MP3 de salida (guardado en carpeta 'salidas')")
    parser.add_argument("--list-voces", action="store_true", help="Muestra la lista de voces en español recomendadas")

    args = parser.parse_args()

    if args.list_voces:
        mostrar_voces()
        sys.exit(0)

    # Crear carpeta de salidas si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[i] Carpeta de salidas creada en: {OUTPUT_DIR}")

    texto_final = ""
    if args.texto:
        texto_final = args.texto
    elif args.archivo:
        if not os.path.exists(args.archivo):
            print(f"[ERROR] El archivo '{args.archivo}' no existe.", file=sys.stderr)
            sys.exit(1)
        try:
            with open(args.archivo, 'r', encoding='utf-8') as f:
                texto_final = f.read()
        except Exception as e:
            print(f"[ERROR] Error al leer el archivo: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Modo interactivo por defecto si no se pasa texto
        print("=== CONVERTIDOR DE TEXTO A VOZ COMERCIAL ===")
        print("Escribe o pega el texto que deseas convertir (presiona Ctrl+D en Unix o Ctrl+Z + Enter en Windows para finalizar):\n")
        try:
            texto_final = sys.stdin.read()
        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario.")
            sys.exit(0)

    texto_final = texto_final.strip()
    if not texto_final:
        print("[ERROR] Error: El texto a convertir no puede estar vacío.", file=sys.stderr)
        sys.exit(1)

    # Nombre de salida
    if args.salida:
        # Asegurarse de que termine en .mp3
        nombre_archivo = args.salida
        if not nombre_archivo.lower().endswith(".mp3"):
            nombre_archivo += ".mp3"
        ruta_salida = os.path.join(OUTPUT_DIR, nombre_archivo)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_salida = os.path.join(OUTPUT_DIR, f"audio_{timestamp}.mp3")

    asyncio.run(generar_audio(texto_final, args.voz, args.velocidad, args.tono, ruta_salida))

if __name__ == "__main__":
    main()
