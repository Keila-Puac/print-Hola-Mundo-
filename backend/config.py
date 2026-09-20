from pathlib import Path

# ============================================================
# RUTAS
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

DICCIONARIO_PATH = DATA_RAW / "diccionario_de_variables.xlsx"

# ============================================================
# MAPEOS DE CÓDIGOS (según documentación del hackatón)
# ============================================================

SECTOR = {
    1: "Público",
    2: "Privado",
    3: "Municipal",
    4: "Cooperativa",
}

AREA = {
    1: "Urbana",
    2: "Rural",
    9: "Ignorado",
}

SEXO = {
    1: "Hombre",
    2: "Mujer",
    9: "Ignorado",
}

NIVEL = {
    1: "Preprimaria",
    2: "Primaria",
    3: "Básico",
    4: "Diversificado",
    5: "Primaria de adultos",
    9: "Ignorado",
}

PUEBLO = {
    1: "Maya",
    2: "Garífuna",
    3: "Xinka",
    4: "Afrodescendiente/Creole/Afromestizo",
    5: "Ladino/Mestizo",
    6: "Extranjero",
    9: "Ignorado",
}

PLAN_ESTUDIOS = {
    1: "Diario",
    2: "Fin de semana",
    3: "Virtual a distancia",
    4: "Semipresencial",
    5: "Mixto",
}

JORNADA = {
    1: "Matutina",
    2: "Vespertina",
    3: "Nocturna",
    4: "Doble",
    5: "Intermedia",
    9: "Ignorado",
}

RESULTADO = {
    1: "Promovido",
    2: "Vigente",
    3: "Retirado",
    4: "Retirado definitivo",
    5: "No promovido",
    9: "Ignorado",
}

REPITENTE = {
    1: "Sí",
    2: "No",
    9: "Ignorado",
}

GRADUANDO = {
    1: "Sí",
    2: "No",
    9: "Ignorado",
}

# Catálogo de departamentos
DEPARTAMENTOS = {
    1: "Guatemala",
    2: "El Progreso",
    3: "Sacatepéquez",
    4: "Chimaltenango",
    5: "Escuintla",
    6: "Santa Rosa",
    7: "Sololá",
    8: "Totonicapán",
    9: "Quetzaltenango",
    10: "Suchitepéquez",
    11: "Retalhuleu",
    12: "San Marcos",
    13: "Huehuetenango",
    14: "Quiché",
    15: "Baja Verapaz",
    16: "Alta Verapaz",
    17: "Petén",
    18: "Izabal",
    19: "Zacapa",
    20: "Chiquimula",
    21: "Jalapa",
    22: "Jutiapa",
}

# Nombres de archivos esperados
ARCHIVOS_DEPARTAMENTOS = {
    1: "guatemala.xlsx",
    2: "el_progreso.xlsx",
    3: "sacatepequez.xlsx",
    4: "chimaltenango.xlsx",
    5: "escuintla.xlsx",
    6: "santa_rosa.xlsx",
    7: "solola.xlsx",
    8: "totonicapan.xlsx",
    9: "quetzaltenango.xlsx",
    10: "suchitepequez.xlsx",
    11: "retalhuleu.xlsx",
    12: "san_marcos.xlsx",
    13: "huehuetenango.xlsx",
    14: "quiche.xlsx",
    15: "baja_verapaz.xlsx",
    16: "alta_verapaz.xlsx",
    17: "peten.xlsx",
    18: "izabal.xlsx",
    19: "zacapa.xlsx",
    20: "chiquimula.xlsx",
    21: "jalapa.xlsx",
    22: "jutiapa.xlsx",
}