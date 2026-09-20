"""
Agente - Persona C
Usa Grok de forma gratuita a través de la librería 'grook'
+ datos reales generados por analytics.py
"""

import json
from pathlib import Path
import pandas as pd

try:
    from grook import Grook
except ImportError:
    raise ImportError("Primero instala: pip install grook")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# ============================================================
# CARGAR DATOS REALES
# ============================================================

def cargar_contexto() -> str:
    """
    Carga solo los datos agregados que generó Persona B.
    """
    contexto = {}

    # Indicadores + insights
    ruta_json = DATA_PROCESSED / "indicadores_nacionales.json"
    if ruta_json.exists():
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            contexto["indicadores"] = data.get("indicadores", {})
            contexto["insights"] = data.get("insights", [])
            contexto["promedio_retiro"] = data.get("promedio_retiro_nacional")

    # Por departamento
    ruta_depto = DATA_PROCESSED / "resumen_departamentos.parquet"
    if ruta_depto.exists():
        df = pd.read_parquet(ruta_depto)
        # Solo enviamos las columnas importantes para no saturar
        contexto["por_departamento"] = df[["Departamento", "total", "tasa_promocion", "tasa_retiro"]].to_dict(orient="records")

    # Brechas principales
    for nombre in ["area", "sector", "nivel"]:
        ruta = DATA_PROCESSED / f"brecha_{nombre}.parquet"
        if ruta.exists():
            df = pd.read_parquet(ruta)
            contexto[f"brecha_{nombre}"] = df.to_dict(orient="records")

    return json.dumps(contexto, ensure_ascii=False, indent=2)


# ============================================================
# SYSTEM PROMPT ESTRICTO
# ============================================================

SYSTEM_PROMPT = """
Eres un asistente experto en los datos de Educación Formal 2024 de Guatemala.

REGLAS OBLIGATORIAS:
1. Solo puedes usar la información que te doy en el contexto.
2. Nunca inventes cifras ni porcentajes.
3. Si no tienes el dato, di exactamente: "No tengo esa información en los datos disponibles".
4. Responde siempre en español, claro y sencillo.
5. Cuando des un número, menciona de dónde sale.

Contexto de datos reales:
{contexto}
"""

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def preguntar_al_agente(pregunta: str, historial: list | None = None) -> str:
    """
    Función principal que usa el frontend.
    """
    contexto = cargar_contexto()

    # Creamos el mensaje completo
    mensaje = SYSTEM_PROMPT.format(contexto=contexto) + f"\n\nPregunta del usuario: {pregunta}"

    try:
        # Usamos Grok de forma gratuita
        grok = Grook(model="grok-3-auto")   # o "grok-4" si quieres
        respuesta = grok.ask(mensaje)
        return respuesta
    except Exception as e:
        return f"Error al consultar Grok: {str(e)}\n\nIntenta de nuevo o revisa que los datos procesados existan."


# ============================================================
# PRUEBA RÁPIDA
# ============================================================

if __name__ == "__main__":
    print("Probando agente con Grok (gratuito)...\n")
    
    preguntas = [
        "¿Cuántos estudiantes hay en total?",
        "¿Qué departamento tiene la mayor tasa de retiro?",
        "Dame el panorama general de la educación en 2024"
    ]
    
    for p in preguntas:
        print(f"Pregunta: {p}")
        print(f"Respuesta: {preguntar_al_agente(p)}")
        print("-" * 60)