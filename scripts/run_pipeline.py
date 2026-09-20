import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from ingestion import run_ingestion
from analytics import run_analytics

if __name__ == "__main__":
    print("=" * 60)
    print(" PIPELINE COMPLETO - Educación Formal 2024")
    print("=" * 60)

    # 1. Ingesta
    print("\n[1/2] Ejecutando ingesta...")
    run_ingestion(solo_prueba=True)   # Cambia a False cuando tengas todos los archivos

    # 2. Analytics
    print("\n[2/2] Ejecutando analytics...")
    run_analytics()

    print("\n" + "=" * 60)
    print("✅ Pipeline terminado correctamente")
    print("=" * 60)