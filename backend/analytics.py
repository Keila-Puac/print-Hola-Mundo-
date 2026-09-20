import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
import json

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
    """
    total = len(df)

    promovidos = (df["Resultado"] == "Promovido").sum()
    no_promovidos = (df["Resultado"] == "No promovido").sum()
    retirados = df["Resultado"].isin(["Retirado", "Retirado definitivo"]).sum()

    tasa_promocion = promovidos / total * 100
    tasa_no_promocion = no_promovidos / total * 100
    tasa_retiro = retirados / total * 100

    por_nivel = df["Nivel"].value_counts(normalize=True).mul(100).round(1).to_dict()
    por_area = df["Area"].value_counts(normalize=True).mul(100).round(1).to_dict()
    por_sector = df["Sector"].value_counts(normalize=True).mul(100).round(1).to_dict()
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

    # Ordenar por tasa de retiro (de mayor a menor)
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


def generar_insights_nacionales(indicadores: dict, por_depto: pd.DataFrame, brechas: dict) -> list[str]:
    """
    Genera insights accionables para la página de Inicio.
    Cada insight tiene: Dato + Contexto + Implicación.
    """
    insights = []

    total = indicadores["total_estudiantes"]
    tasa_retiro = indicadores["tasa_retiro"]
    tasa_promocion = indicadores["tasa_promocion"]

    # 1. Panorama general
    insights.append(
        f"**Panorama general:** En 2024 se registraron **{total:,}** estudiantes. "
        f"El **{tasa_promocion}%** fue promovido y el **{tasa_retiro}%** se retiró. "
        f"Esto significa que aproximadamente **{int(total * tasa_retiro / 100):,}** estudiantes abandonaron el ciclo escolar."
    )

    # 2. Departamento más crítico
    mas_critico = por_depto.iloc[0]
    diferencia = mas_critico["tasa_retiro"] - tasa_retiro
    insights.append(
        f"**Zona más crítica:** **{mas_critico['Departamento']}** tiene la tasa de retiro más alta "
        f"({mas_critico['tasa_retiro']}% ), **{diferencia:.1f} puntos por encima** del promedio nacional. "
        f"Allí se registraron {mas_critico['total']:,} estudiantes. Es prioritario reforzar el acompañamiento en este departamento."
    )

    # 3. Brecha rural-urbana
    if "area" in brechas:
        df_area = brechas["area"]
        rural = df_area[df_area["Area"] == "Rural"]
        urbana = df_area[df_area["Area"] == "Urbana"]
        if not rural.empty and not urbana.empty:
            diff = rural["tasa_retiro"].values[0] - urbana["tasa_retiro"].values[0]
            insights.append(
                f"**Brecha rural-urbana:** El retiro en el área rural es **{diff:.1f} puntos más alto** que en el área urbana. "
                f"Esta es una de las desigualdades más persistentes del sistema educativo y requiere estrategias diferenciadas."
            )

    # 4. Nivel más afectado
    if "nivel" in brechas:
        df_nivel = brechas["nivel"]
        df_nivel_limpio = df_nivel[~df_nivel["Nivel"].isin(["Ignorado", "Desconocido"])]
        if not df_nivel_limpio.empty:
            nivel_critico = df_nivel_limpio.sort_values("tasa_retiro", ascending=False).iloc[0]
            insights.append(
                f"**Nivel más afectado:** El nivel **{nivel_critico['Nivel']}** presenta la mayor tasa de retiro "
                f"({nivel_critico['tasa_retiro']}% ). Es el momento donde más estudiantes abandonan el sistema. "
                f"Intervenir aquí tiene un alto potencial de impacto."
            )

    return insights


def generar_insight_departamento(fila: pd.Series, promedio_nacional_retiro: float) -> str:
    """
    Genera un insight accionable para un departamento específico.
    """
    diferencia = fila["tasa_retiro"] - promedio_nacional_retiro
    estudiantes_retirados = int(fila["total"] * fila["tasa_retiro"] / 100)

    if diferencia >= 2:
        evaluacion = "se encuentra en una **situación crítica**"
        recomendacion = "Se recomienda priorizar acciones de retención escolar, especialmente en los niveles de mayor abandono."
    elif diferencia >= 0.5:
        evaluacion = "está **por encima del promedio nacional**"
        recomendacion = "Conviene reforzar el seguimiento a estudiantes en riesgo de retiro."
    elif diferencia <= -2:
        evaluacion = "muestra **mejores resultados** que el promedio nacional"
        recomendacion = "Puede servir como referencia de buenas prácticas para otros departamentos."
    else:
        evaluacion = "se encuentra **cerca del promedio nacional**"
        recomendacion = "Mantener el monitoreo y fortalecer las estrategias preventivas."

    return (
        f"En **{fila['Departamento']}** se registraron **{fila['total']:,}** estudiantes. "
        f"La tasa de retiro fue del **{fila['tasa_retiro']}%** "
        f"({diferencia:+.1f} puntos vs el promedio nacional de {promedio_nacional_retiro}%). "
        f"Esto equivale a aproximadamente **{estudiantes_retirados:,}** estudiantes que abandonaron el ciclo. "
        f"El departamento {evaluacion}. {recomendacion}"
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
    insights = generar_insights_nacionales(indicadores, por_depto, brechas)

    # Guardar resultados
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    por_depto.to_parquet(DATA_PROCESSED / "resumen_departamentos.parquet", index=False)

    for nombre, tabla in brechas.items():
        tabla.to_parquet(DATA_PROCESSED / f"brecha_{nombre}.parquet", index=False)

    resultado = {
        "indicadores": indicadores,
        "insights": insights,
        "promedio_retiro_nacional": indicadores["tasa_retiro"],
    }

    with open(DATA_PROCESSED / "indicadores_nacionales.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("\n✅ Analytics terminado")
    print(f"Total estudiantes: {indicadores['total_estudiantes']:,}")
    print(f"Tasa de promoción: {indicadores['tasa_promocion']}%")
    print(f"Tasa de retiro: {indicadores['tasa_retiro']}%")

    return resultado


if __name__ == "__main__":
    run_analytics()