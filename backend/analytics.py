import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any

from config import DATA_PROCESSED


def cargar_datos() -> pd.DataFrame:
    """Carga el dataset procesado."""
    ruta = DATA_PROCESSED / "educacion_2024.parquet"
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Ejecuta primero la ingesta (run_pipeline.py)"
        )
    return pd.read_parquet(ruta)


def calcular_indicadores_basicos(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula los indicadores principales a nivel nacional.
    Estos números deben cuadrar con las cifras de validación del hackatón.
    """
    total = len(df)

    # Tasas principales
    promovidos = (df["Resultado"] == "Promovido").sum()
    no_promovidos = (df["Resultado"] == "No promovido").sum()
    retirados = df["Resultado"].isin(["Retirado", "Retirado definitivo"]).sum()

    tasa_promocion = promovidos / total * 100
    tasa_no_promocion = no_promovidos / total * 100
    tasa_retiro = retirados / total * 100

    # Distribución por nivel
    por_nivel = df["Nivel"].value_counts(normalize=True).mul(100).round(1).to_dict()

    # Distribución por área
    por_area = df["Area"].value_counts(normalize=True).mul(100).round(1).to_dict()

    # Distribución por sector
    por_sector = df["Sector"].value_counts(normalize=True).mul(100).round(1).to_dict()

    # Distribución por sexo
    por_sexo = df["Sexo"].value_counts(normalize=True).mul(100).round(1).to_dict()

    return {
        "total_estudiantes": total,
        "tasa_promocion": round(tasa_promocion, 1),
        "tasa_no_promocion": round(tasa_no_promocion, 1),
        "tasa_retiro": round(tasa_retiro, 1),
        "por_nivel": por_nivel,
        "por_area": por_area,
        "por_sector": por_sector,
        "por_sexo": por_sexo,
    }


def calcular_por_departamento(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera una tabla resumen por departamento con los indicadores clave.
    """
    resumen = (
        df.groupby("Departamento")
        .agg(
            total=("Resultado", "count"),
            promovidos=("Resultado", lambda x: (x == "Promovido").sum()),
            no_promovidos=("Resultado", lambda x: (x == "No promovido").sum()),
            retirados=("Resultado", lambda x: x.isin(["Retirado", "Retirado definitivo"]).sum()),
        )
        .reset_index()
    )

    resumen["tasa_promocion"] = (resumen["promovidos"] / resumen["total"] * 100).round(1)
    resumen["tasa_no_promocion"] = (resumen["no_promovidos"] / resumen["total"] * 100).round(1)
    resumen["tasa_retiro"] = (resumen["retirados"] / resumen["total"] * 100).round(1)

    # Ordenar por tasa de retiro (de mayor a menor) para ver criticidad
    resumen = resumen.sort_values("tasa_retiro", ascending=False).reset_index(drop=True)

    return resumen


def calcular_brechas(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Calcula las principales brechas: Urbano/Rural, Público/Privado, por Pueblo y por Nivel.
    """
    def resumen_grupo(grupo_col: str) -> pd.DataFrame:
        g = (
            df.groupby(grupo_col)
            .agg(
                total=("Resultado", "count"),
                promovidos=("Resultado", lambda x: (x == "Promovido").sum()),
                retirados=("Resultado", lambda x: x.isin(["Retirado", "Retirado definitivo"]).sum()),
            )
            .reset_index()
        )
        g["tasa_promocion"] = (g["promovidos"] / g["total"] * 100).round(1)
        g["tasa_retiro"] = (g["retirados"] / g["total"] * 100).round(1)
        return g

    return {
        "area": resumen_grupo("Area"),
        "sector": resumen_grupo("Sector"),
        "pueblo": resumen_grupo("Pueblo"),
        "nivel": resumen_grupo("Nivel"),
    }


def generar_insights_nacionales(indicadores: Dict[str, Any], por_depto: pd.DataFrame) -> list[str]:
    """
    Genera textos de insights claros y accionables para la página de Inicio.
    Estos textos son los que el usuario lee (no solo números).
    """
    insights = []

    # Insight 1: Panorama general
    insights.append(
        f"En 2024 se registraron **{indicadores['total_estudiantes']:,}** inscripciones en el sistema educativo formal de Guatemala. "
        f"De ellas, el **{indicadores['tasa_promocion']}%** fue promovido, el **{indicadores['tasa_no_promocion']}%** no promovido "
        f"y el **{indicadores['tasa_retiro']}%** se retiró."
    )

    # Insight 2: Dónde está la mayor pérdida
    depto_mas_retiro = por_depto.iloc[0]
    insights.append(
        f"El departamento con mayor tasa de retiro es **{depto_mas_retiro['Departamento']}** "
        f"({depto_mas_retiro['tasa_retiro']}% ). Esto está por encima del promedio nacional."
    )

    # Insight 3: Nivel más crítico
    # (se puede mejorar cuando tengamos el desglose por nivel + resultado)
    insights.append(
        "La mayor cantidad de estudiantes se concentra en **Primaria**. "
        "Es en los niveles de Básico y Diversificado donde suele observarse mayor abandono relativo."
    )

    # Insight 4: Brecha rural
    insights.append(
        "Más de la mitad de los estudiantes estudia en área **rural**. "
        "Las brechas de resultados entre el área urbana y rural son uno de los puntos más importantes a monitorear."
    )

    return insights


def generar_insight_departamento(fila: pd.Series, promedio_nacional_retiro: float) -> str:
    """
    Genera un texto explicativo para un departamento específico.
    """
    diferencia = fila["tasa_retiro"] - promedio_nacional_retiro

    if diferencia > 1.5:
        comparacion = f"**{diferencia:.1f} puntos por encima** del promedio nacional"
        tono = "situación más crítica"
    elif diferencia < -1.5:
        comparacion = f"**{abs(diferencia):.1f} puntos por debajo** del promedio nacional"
        tono = "mejores resultados relativos"
    else:
        comparacion = "cerca del promedio nacional"
        tono = "situación similar al resto del país"

    return (
        f"En **{fila['Departamento']}** se registraron {fila['total']:,} estudiantes. "
        f"La tasa de retiro fue del **{fila['tasa_retiro']}%** ({comparacion}). "
        f"Esto indica una {tono}."
    )


def run_analytics(solo_prueba: bool = False) -> Dict[str, Any]:
    """
    Ejecuta todo el análisis y guarda los resultados listos para el frontend.
    """
    print("Cargando datos procesados...")
    df = cargar_datos()

    print("Calculando indicadores nacionales...")
    indicadores = calcular_indicadores_basicos(df)

    print("Calculando resumen por departamento...")
    por_depto = calcular_por_departamento(df)

    print("Calculando brechas...")
    brechas = calcular_brechas(df)

    print("Generando insights...")
    insights = generar_insights_nacionales(indicadores, por_depto)

    # Guardar resultados para que el frontend los consuma fácilmente
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    por_depto.to_parquet(DATA_PROCESSED / "resumen_departamentos.parquet", index=False)
    
    # Guardar brechas
    for nombre, tabla in brechas.items():
        tabla.to_parquet(DATA_PROCESSED / f"brecha_{nombre}.parquet", index=False)

    # Guardar indicadores e insights en un formato simple
    resultado = {
        "indicadores": indicadores,
        "insights": insights,
        "promedio_retiro_nacional": indicadores["tasa_retiro"],
    }

    # También guardamos un JSON legible
    import json
    with open(DATA_PROCESSED / "indicadores_nacionales.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("\n✅ Analytics terminado")
    print(f"Total estudiantes: {indicadores['total_estudiantes']:,}")
    print(f"Tasa de promoción: {indicadores['tasa_promocion']}%")
    print(f"Tasa de retiro: {indicadores['tasa_retiro']}%")

    return resultado


if __name__ == "__main__":
    run_analytics()