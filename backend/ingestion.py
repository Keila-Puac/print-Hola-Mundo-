import pandas as pd
from pathlib import Path
from typing import Optional
import warnings

from config import (
    DATA_RAW,
    DATA_PROCESSED,
    SECTOR, AREA, SEXO, NIVEL, PUEBLO,
    PLAN_ESTUDIOS, JORNADA, RESULTADO,
    REPITENTE, GRADUANDO, DEPARTAMENTOS,
    ARCHIVOS_DEPARTAMENTOS
)

warnings.filterwarnings("ignore")


def normalizar_codigo_establecimiento(codigo: str) -> str:
    """
    Corrige el problema conocido de Guatemala:
    ~36% de los códigos empiezan con '00-' en lugar de '01-'.
    """
    if pd.isna(codigo):
        return codigo
    codigo = str(codigo).strip()
    if codigo.startswith("00-"):
        return "01-" + codigo[3:]
    return codigo


def extraer_municipio(codigo: str) -> Optional[str]:
    """
    Extrae el código de municipio del CodEstablecimiento.
    Formato: DD-MM-NNNN-SS → los dos primeros segmentos.
    """
    if pd.isna(codigo):
        return None
    partes = str(codigo).split("-")
    if len(partes) >= 2:
        return f"{partes[0]}-{partes[1]}"
    return None


def decodificar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Traduce todos los códigos numéricos a etiquetas legibles.
    """
    df = df.copy()

    # Normalizar código de establecimiento (importante para Guatemala)
    if "CodEstablecimiento" in df.columns:
        df["CodEstablecimiento"] = df["CodEstablecimiento"].apply(normalizar_codigo_establecimiento)
        df["municipio_codigo"] = df["CodEstablecimiento"].apply(extraer_municipio)

    # Mapear columnas de códigos
    mapeos = {
        "Sector": SECTOR,
        "Área": AREA,
        "Sexo": SEXO,
        "Nivel": NIVEL,
        "Pueblo_Per": PUEBLO,
        "Plan_Est": PLAN_ESTUDIOS,
        "Jornada_Est": JORNADA,
        "Resultado_F": RESULTADO,
        "Repitente": REPITENTE,
        "Graduando": GRADUANDO,
        "Departamento_F": DEPARTAMENTOS,
    }

    for col, mapa in mapeos.items():
        if col in df.columns:
            # Guardamos también el código original por si se necesita
            df[f"{col}_codigo"] = df[col]
            df[col] = df[col].map(mapa).fillna("Desconocido")

    # Renombrar para que quede más legible
    df = df.rename(columns={
        "Área": "Area",
        "Pueblo_Per": "Pueblo",
        "Plan_Est": "Plan_estudios",
        "Jornada_Est": "Jornada",
        "Resultado_F": "Resultado",
        "Departamento_F": "Departamento",
    })

    return df


def procesar_archivo(ruta: Path, departamento_id: int) -> pd.DataFrame:
    """
    Lee un archivo de departamento, lo limpia y lo decodifica.
    """
    print(f"  → Procesando {ruta.name} ...")
    
    df = pd.read_excel(ruta, engine="openpyxl")
    
    # Asegurar que el departamento esté correcto
    df["Departamento_F"] = departamento_id
    
    df = decodificar_dataframe(df)
    
    print(f"     {len(df):,} registros procesados")
    return df


def run_ingestion(solo_prueba: bool = False) -> pd.DataFrame:
    """
    Ejecuta la ingesta completa.
    
    Args:
        solo_prueba: Si True, solo procesa 2-3 departamentos pequeños
                     (útil mientras desarrollas).
    """
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    if solo_prueba:
        # Departamentos pequeños para desarrollo rápido
        departamentos_a_procesar = {
            2: "el_progreso.xlsx",      # ~50k
            19: "zacapa.xlsx",          # ~71k
            15: "baja_verapaz.xlsx",    # ~82k
        }
        print("Modo PRUEBA: solo 3 departamentos pequeños")
    else:
        departamentos_a_procesar = ARCHIVOS_DEPARTAMENTOS
        print("Modo COMPLETO: los 22 departamentos")

    dfs = []

    for dep_id, nombre_archivo in departamentos_a_procesar.items():
        ruta = DATA_RAW / nombre_archivo
        if not ruta.exists():
            print(f"  ⚠️  No se encontró: {nombre_archivo}")
            continue

        df = procesar_archivo(ruta, dep_id)
        dfs.append(df)

    if not dfs:
        raise FileNotFoundError("No se encontró ningún archivo de datos en data/raw/")

    # Unir todo
    df_final = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal de registros: {len(df_final):,}")

    # Guardar versión completa (Parquet es mucho más rápido y liviano)
    ruta_parquet = DATA_PROCESSED / "educacion_2024.parquet"
    df_final.to_parquet(ruta_parquet, index=False)
    print(f"Guardado en: {ruta_parquet}")

    # También guardar una muestra en CSV por si quieren revisarlo fácil
    muestra = df_final.sample(n=min(5000, len(df_final)), random_state=42)
    muestra.to_csv(DATA_PROCESSED / "muestra_5000.csv", index=False)

    return df_final


if __name__ == "__main__":
    # Cambia a False cuando quieras procesar los 22 departamentos
    run_ingestion(solo_prueba=True)