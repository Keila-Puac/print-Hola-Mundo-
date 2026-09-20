import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "backend"))
from config import DATA_PROCESSED


@st.cache_data
def cargar_brecha(nombre: str) -> pd.DataFrame:
    return pd.read_parquet(DATA_PROCESSED / f"brecha_{nombre}.parquet")


def crear_grafica_comparacion(df: pd.DataFrame, categoria: str, titulo: str):
    """Crea una gráfica de barras comparando promoción y retiro."""
    df_plot = df.melt(
        id_vars=[categoria],
        value_vars=["tasa_promocion", "tasa_retiro"],
        var_name="Indicador",
        value_name="Porcentaje"
    )
    df_plot["Indicador"] = df_plot["Indicador"].map({
        "tasa_promocion": "% Promoción",
        "tasa_retiro": "% Retiro"
    })

    fig = px.bar(
        df_plot,
        x=categoria,
        y="Porcentaje",
        color="Indicador",
        barmode="group",
        text="Porcentaje",
        color_discrete_map={
            "% Promoción": "#27ae60",
            "% Retiro": "#c0392b"
        },
        title=titulo,
        labels={categoria: "", "Porcentaje": "Porcentaje (%)"}
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=40),
        legend_title_text="",
        yaxis_range=[0, max(df_plot["Porcentaje"]) * 1.2]
    )
    return fig


def mostrar_brechas():
    st.title("Brechas y Desigualdades")
    st.markdown(
        "Aquí puedes ver las diferencias más importantes en los resultados educativos "
        "según el área (urbana/rural), el sector, el pueblo de pertenencia y el nivel educativo."
    )
    st.markdown("---")

    # ============================================================
    # 1. BRECHA URBANO vs RURAL
    # ============================================================
    st.subheader("1. Área Urbana vs Rural")

    try:
        df_area = cargar_brecha("area")
    except Exception:
        st.error("No se encontraron los datos de brechas. Ejecuta el pipeline primero.")
        st.stop()

    col1, col2 = st.columns([1.4, 1])

    with col1:
        fig_area = crear_grafica_comparacion(df_area, "Area", "Resultados por Área")
        st.plotly_chart(fig_area, use_container_width=True)

    with col2:
        st.markdown("##### ¿Qué significa?")
        rural = df_area[df_area["Area"] == "Rural"]
        urbana = df_area[df_area["Area"] == "Urbana"]

        if not rural.empty and not urbana.empty:
            diff_retiro = rural["tasa_retiro"].values[0] - urbana["tasa_retiro"].values[0]
            st.markdown(f"""
            - En el **área rural** la tasa de retiro es de **{rural['tasa_retiro'].values[0]}%**.
            - En el **área urbana** es de **{urbana['tasa_retiro'].values[0]}%**.
            - Diferencia: **{diff_retiro:+.1f} puntos porcentuales**.
            
            Esta es una de las brechas más relevantes del sistema educativo guatemalteco.
            """)

    st.markdown("---")

    # ============================================================
    # 2. BRECHA POR SECTOR
    # ============================================================
    st.subheader("2. Sector (Público, Privado, etc.)")

    df_sector = cargar_brecha("sector")

    col1, col2 = st.columns([1.4, 1])

    with col1:
        fig_sector = crear_grafica_comparacion(df_sector, "Sector", "Resultados por Sector")
        st.plotly_chart(fig_sector, use_container_width=True)

    with col2:
        st.markdown("##### ¿Qué significa?")
        st.markdown("""
        - El sector **público** concentra la gran mayoría de estudiantes.
        - Suele presentar tasas de retiro y no promoción más altas que el sector privado.
        - Esta diferencia refleja desigualdades de recursos y condiciones de aprendizaje.
        """)

    st.markdown("---")

    # ============================================================
    # 3. BRECHA POR PUEBLO DE PERTENENCIA
    # ============================================================
    st.subheader("3. Pueblo de pertenencia")

    df_pueblo = cargar_brecha("pueblo")

    # Filtramos "Ignorado" y "Desconocido" para que la gráfica sea más clara
    df_pueblo_limpio = df_pueblo[~df_pueblo["Pueblo"].isin(["Ignorado", "Desconocido"])]

    fig_pueblo = px.bar(
        df_pueblo_limpio.sort_values("tasa_retiro", ascending=False),
        x="Pueblo",
        y="tasa_retiro",
        color="tasa_retiro",
        color_continuous_scale="Reds",
        text="tasa_retiro",
        labels={"tasa_retiro": "Tasa de retiro (%)", "Pueblo": ""},
        title="Tasa de retiro por pueblo de pertenencia"
    )
    fig_pueblo.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_pueblo.update_layout(
        height=420,
        coloraxis_showscale=False,
        xaxis_tickangle=-30,
        margin=dict(t=50, b=80)
    )
    st.plotly_chart(fig_pueblo, use_container_width=True)

    st.info(
        "Las diferencias por pueblo de pertenencia son un indicador importante de inequidad. "
        "Observa especialmente los grupos con mayor tasa de retiro."
    )

    st.markdown("---")

    # ============================================================
    # 4. BRECHA POR NIVEL EDUCATIVO
    # ============================================================
    st.subheader("4. Nivel educativo")

    df_nivel = cargar_brecha("nivel")

    col1, col2 = st.columns([1.4, 1])

    with col1:
        fig_nivel = crear_grafica_comparacion(df_nivel, "Nivel", "Resultados por Nivel Educativo")
        st.plotly_chart(fig_nivel, use_container_width=True)

    with col2:
        st.markdown("##### ¿Qué significa?")
        st.markdown("""
        - En **Primaria** suele haber mayor cantidad de estudiantes y mejores tasas de promoción.
        - En **Básico** y **Diversificado** aumenta el retiro y la no promoción.
        - Esta es la etapa donde más jóvenes abandonan el sistema educativo.
        """)

    st.markdown("---")

    # ============================================================
    # RESUMEN FINAL
    # ============================================================
    st.subheader("Resumen de las principales brechas")

    st.success("""
    **Puntos clave para docentes, supervisores y organizaciones:**

    1. La brecha **rural-urbana** sigue siendo una de las más marcadas.
    2. El sector **público** concentra tanto la mayor cantidad de estudiantes como los mayores desafíos.
    3. Existen diferencias importantes según el **pueblo de pertenencia**.
    4. El paso de Primaria a Básico es un momento crítico de abandono.
    """)

    st.caption("Fuente: Microdatos de Educación Formal 2024 · Instituto Nacional de Estadística (INE)")


# Para probar de forma independiente
if __name__ == "__main__":
    st.set_page_config(page_title="Brechas y Desigualdades", layout="wide")
    mostrar_brechas()