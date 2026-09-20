# Hackaton AI Builders GT

Documentación completa del hackatón: el dataset con el que se trabaja, el desafío, las
reglas, los criterios de evaluación y la entrega.

Secciones: Resumen · Contenido · Desafío · Evaluación · Entrega.

# Hackaton · AI Builders GT — Resumen

Vas a tomar los datos públicos de la educación en Guatemala —millones de filas que hoy solo
un especialista puede leer— y construir, con apoyo de IA, una herramienta que los vuelva
comprensibles para cualquier persona.

| Dato | Valor |
|---|---|
| Registros | ~4.3 millones |
| Departamentos | 22 |
| Ciclo escolar | 2024 |
| Integrantes por equipo | 1 a 5 |

## Con qué vas a trabajar

El dataset **Educación Formal 2024**, publicado como dato abierto por el Instituto Nacional de
Estadística en https://datos.ine.gob.gt/dataset/educacion-formal-2024. Son **microdatos**: cada
fila es una inscripción de un estudiante durante el ciclo 2024.

Cada registro describe dónde y cómo estudia una persona —departamento, establecimiento, nivel y
grado, sector, área urbana o rural, sexo, pueblo de pertenencia, jornada— y cómo cerró el año.
No hay nombres ni identificadores: no es una encuesta, es el censo administrativo completo del
sistema educativo.

## La problemática

Los datos están publicados y son gratuitos, pero en la práctica casi nadie los aprovecha. La
barrera no es el acceso: es la interpretación. Tres razones concretas:

1. **Todo está en clave.** Los valores son códigos numéricos. El sector de una escuela aparece
   como `1`, no como "Público"; el resultado del año como `5`, no como "No promovido". Sin el
   diccionario al lado, una fila no comunica nada.
2. **El volumen abruma.** Más de cuatro millones de filas repartidas en decenas de archivos. No
   se abren cómodamente en una hoja de cálculo ni se pueden volcar completas a un modelo de IA.
3. **Nada viene calculado.** No existe una columna que se pueda sumar. Cualquier indicador
   —aprobación, deserción, repitencia— hay que construirlo a partir del conteo de registros.

El costo de esto es real: una autoridad municipal, un periodista o un docente no pueden abrir esa
tabla y sacar conclusiones sobre la educación de su territorio.

## Qué buscamos resolver

Que estos datos dejen de ser una tabla opaca y se conviertan en información que una persona sin
formación técnica pueda entender en minutos. Concretamente, que tu herramienta logre tres cosas:

- **Traducir:** que los códigos se lean como palabras y las cifras tengan contexto.
- **Explicar:** que no solo muestre gráficas, sino que diga qué significan y qué se concluye de ellas.
- **Responder:** que quien tenga una duda pueda preguntarla en lenguaje natural y obtener una
  respuesta basada en los datos reales.

Flujo: datos codificados → tu solución con IA → información comprensible.

## Cómo: los tres componentes

1. **Ingesta de datos.** Lee los archivos y los decodifica con el diccionario de variables,
   dejándolos listos para consumirse. Si esta pieza interpreta mal, todo lo demás sale mal.
2. **Dashboard con gráficas y análisis.** Visualizaciones claras acompañadas de análisis escrito,
   dirigidas a alguien sin formación estadística. Las cifras que afirmes deben cuadrar con los datos.
3. **Agente en lenguaje natural.** Responde preguntas sobre los datos y sobre el análisis que generó
   tu dashboard, sin inventar cifras y admitiendo cuando algo no se puede saber.

## Cómo se evalúa

Sobre 100 puntos. Usar IA no resta —es parte del producto y una herramienta de desarrollo válida—;
lo que más pesa es que comprendas y puedas explicar lo que construiste.

| Peso | Criterio |
|---:|---|
| 30 | Comprensión de tu solución |
| 20 | Calidad de arquitectura |
| 20 | Calidad de código |
| 15 | Cumplir el reto |
| 10 | Buenas prácticas |
| 5 | Reproducibilidad |

La evaluación incluye un **pitch**: un representante del equipo expone durante 5 minutos qué hizo
y cómo lo hizo, seguido de 5 minutos de preguntas de los jueces.

## Qué entregas

1. **Código:** un repositorio público, reproducible localmente, con instrucciones de uso y
   documentación formal de la arquitectura y las decisiones técnicas.
2. **Audiovisual:** dos videos de máximo 3 minutos cada uno, uno explicando la arquitectura del
   proyecto y otro mostrando su funcionamiento.

## Lo esencial de las reglas

- Equipos de **1 a 5 personas**; puedes participar solo.
- El proyecto se construye durante el hackatón.
- Usar IA está permitido y se espera: documenta qué usaste y para qué.
- El dataset entregado es la base; datos externos deben ser públicos y citados.
- Presentarse al pitch es obligatorio para ser evaluado.


---

# Contenido — Dataset Educación Formal 2024

## Información

Vas a trabajar con el dataset **Educación Formal 2024**: el registro de todas las inscripciones
del sistema educativo guatemalteco durante ese ciclo escolar.

- Registros: ~4.3 millones
- Departamentos: 22
- Columnas: 15
- Ciclo escolar: 2024

### De dónde vienen

Los datos provienen de los **registros administrativos del sistema educativo**: cada año, los
establecimientos del país reportan al Ministerio de Educación quién se inscribió, en qué nivel y
grado, y cómo terminó el ciclo. Esa información se consolida y se publica como dato abierto.

Fuente oficial: portal de datos abiertos del **Instituto Nacional de Estadística (INE)**,
https://datos.ine.gob.gt/dataset/educacion-formal-2024

### Qué son exactamente

Son **microdatos**: en lugar de entregar totales ya calculados, se entrega el detalle fila por
fila. **Cada fila representa una inscripción**, es decir, un estudiante matriculado en un
establecimiento durante 2024.

Cada fila no dice quién es la persona —no hay nombres ni identificadores— sino **cómo y dónde
estudia**: el departamento, el establecimiento, el nivel educativo y grado, si la escuela es
pública o privada, si está en área urbana o rural, el sexo, el pueblo de pertenencia, la jornada,
el plan de estudios, y cómo cerró el año (aprobado, no aprobado o retirado), además de si repite
grado o se está graduando.

No es una encuesta ni una muestra estadística: es un **censo administrativo**, o sea la totalidad
de los registros del sistema. Por eso son más de cuatro millones de filas.

### Para qué se usan

- **Planificar y asignar recursos:** saber dónde hay más estudiantes, qué niveles están saturados
  y en qué municipios crece o cae la matrícula.
- **Medir resultados:** calcular qué porcentaje aprueba, no aprueba o abandona el año, y comparar
  entre departamentos, niveles o sectores.
- **Detectar brechas:** contrastar lo urbano contra lo rural, lo público contra lo privado, o cómo
  varían los resultados según sexo y pueblo de pertenencia.
- **Investigación y periodismo de datos:** sustentar reportajes, tesis y estudios con evidencia.

Preguntas como "¿en qué departamento se aprueba menos el nivel básico?" o "¿se abandona más la
escuela en el área rural?" se pueden responder con este dataset, pero solo después de procesarlo,
porque tal como viene no es legible.

### Qué no contienen

- Solo abarca el ciclo **2024**: no hay manera de comparar contra otros años.
- No hay identificador de estudiante, así que **no se puede seguir a una persona** en el tiempo ni
  reconstruir su trayectoria.
- No incluye calificaciones, edad, discapacidad, datos socioeconómicos, ni información sobre
  docentes o infraestructura de los establecimientos.

---

## Estructura

### Formato de entrega

- **23 archivos** en formato `.xlsx` (Excel): **22 de datos**, uno por departamento, más
  **1 diccionario de variables**.
- Cada archivo de datos tiene una **hoja con los registros**. La primera fila son los encabezados;
  de la segunda en adelante, los datos.
- **Grano:** una fila es una inscripción. Todos los archivos comparten exactamente el mismo esquema
  de 15 columnas, así que se pueden concatenar.
- **Sin celdas vacías:** cuando un dato no se registró, viene el código `9` (Ignorado), que es un
  valor real y no un faltante.

Casi todos los valores son **códigos numéricos**, no texto. El diccionario de variables es el que
traduce cada código a su etiqueta; sin él los datos no se interpretan.

### Las 15 columnas

| Columna | Tipo | Qué contiene |
|---|---|---|
| `Año` | Entero | Ciclo escolar. Siempre `2024`. |
| `CodEstablecimiento` | Texto | Código del establecimiento, formato `DD-MM-NNNN-SS`. |
| `Departamento_F` | Entero | Departamento, del `1` al `22`. |
| `Depto_mupio` | Entero | Campo de departamento y municipio. Ver notas. |
| `Sector` | Código | Quién administra el establecimiento. |
| `Área` | Código | Ubicación urbana o rural. |
| `Sexo` | Código | Sexo del estudiante. |
| `Grado` | Entero | Grado que cursa. Su significado depende de `Nivel`. |
| `Nivel` | Código | Nivel educativo. |
| `Pueblo_Per` | Código | Pueblo de pertenencia. |
| `Plan_Est` | Código | Plan de estudios (modalidad de asistencia). |
| `Jornada_Est` | Código | Jornada en que estudia. |
| `Resultado_F` | Código | Cómo cerró el ciclo escolar. |
| `Repitente` | Código | Si está repitiendo el grado. |
| `Graduando` | Código | Si se gradúa en ese ciclo. |

### Catálogo de códigos

- **Sector:** `1` Público · `2` Privado · `3` Municipal · `4` Cooperativa
- **Área:** `1` Urbana · `2` Rural · `9` Ignorado
- **Sexo:** `1` Hombre · `2` Mujer · `9` Ignorado
- **Nivel:** `1` Preprimaria · `2` Primaria · `3` Básico · `4` Diversificado ·
  `5` Primaria de adultos · `9` Ignorado
- **Pueblo de pertenencia:** `1` Maya · `2` Garífuna · `3` Xinka ·
  `4` Afrodescendiente/Creole/Afromestizo · `5` Ladino/Mestizo · `6` Extranjero · `9` Ignorado
- **Plan de estudios:** `1` Diario · `2` Fin de semana · `3` Virtual a distancia ·
  `4` Semipresencial · `5` Mixto
- **Jornada:** `1` Matutina · `2` Vespertina · `3` Nocturna · `4` Doble · `5` Intermedia ·
  `9` Ignorado
- **Resultado final:** `1` Promovido · `2` Vigente · `3` Retirado · `4` Retirado definitivo ·
  `5` No promovido · `9` Ignorado
- **Repitente:** `1` Sí · `2` No · `9` Ignorado
- **Graduando:** `1` Sí es graduando · `2` No es graduando · `9` Ignorado

### Catálogo de departamentos

`1` Guatemala · `2` El Progreso · `3` Sacatepéquez · `4` Chimaltenango · `5` Escuintla ·
`6` Santa Rosa · `7` Sololá · `8` Totonicapán · `9` Quetzaltenango · `10` Suchitepéquez ·
`11` Retalhuleu · `12` San Marcos · `13` Huehuetenango · `14` Quiché · `15` Baja Verapaz ·
`16` Alta Verapaz · `17` Petén · `18` Izabal · `19` Zacapa · `20` Chiquimula · `21` Jalapa ·
`22` Jutiapa

El diccionario incluye además el catálogo completo de **municipios**, con un código de cuatro
dígitos donde los dos primeros son el departamento (por ejemplo, `0101` es el municipio de
Guatemala).

### El código de establecimiento

`CodEstablecimiento` no es un identificador plano: codifica una jerarquía en cuatro segmentos
separados por guiones, como `19-01-0001-42`.

| Segmento | Ejemplo | Qué es |
|---|---|---|
| 1.º | `19` | Departamento |
| 2.º | `01` | Municipio dentro del departamento |
| 3.º | `0001` | Número del establecimiento |
| 4.º | `42` | Nivel educativo que ofrece |

Valores del cuarto segmento: `40`, `41` y `42` preprimaria · `43` primaria ·
`44` primaria de adultos · `45` básico · `46` diversificado.

Como el nivel va dentro del código, **un mismo establecimiento que atiende varios niveles aparece
con varios códigos distintos**. Contar códigos únicos no equivale a contar escuelas.

### Notas para interpretar correctamente

- **El municipio se deriva del código del establecimiento**, no de la columna `Depto_mupio`: esa
  columna trae un valor constante dentro de cada archivo y no sirve para desagregar.
- **`Grado` siempre se lee junto a `Nivel`.** Rangos: preprimaria `0`–`6`, primaria `1`–`6`,
  básico `1`–`3`, diversificado `4`–`7`, primaria de adultos `1`–`4`. Un `1` de primaria no es lo
  mismo que un `1` de básico.
- **El diccionario menciona una variable `Modalidad`** (bilingüe / monolingüe) que **no existe** en
  los archivos de datos. No la asumas.
- **El código `9` (Ignorado) es un dato real.** Decide si lo excluyes o lo reportas aparte, pero sé
  consistente y documenta la decisión.

### Inconsistencias conocidas

Particularidades reales de los archivos, verificadas sobre los datos. Si no las tomas en cuenta,
tus resultados van a salir mal.

| Qué pasa | Dónde | Cómo manejarlo |
|---|---|---|
| **Prefijo `00-` en el código.** Cerca del 36% de los registros del departamento de Guatemala usan `00-` como primer segmento en lugar de `01-`. Corresponden a establecimientos de la capital. | Solo en `guatemala.xlsx`. Ningún otro departamento lo presenta. | Normaliza el prefijo antes de derivar el municipio. Si no lo haces, a Guatemala le saldrán cerca de 39 municipios en lugar de los **17** reales, y unos 310 mil registros quedarán mal atribuidos. |
| **`Depto_mupio` no varía.** Su valor es constante dentro de cada archivo. | En los 22 archivos de datos. | Ignora esa columna para desagregar por municipio; usa el segundo segmento de `CodEstablecimiento`. |
| **`Modalidad` documentada pero ausente.** | Diccionario de variables. | No la asumas ni intentes derivarla. |
| **`Resultado_F = 4` casi no aparece.** El retiro se concentra en el código `3`. | En todos los archivos. | Decide cómo tratas el retiro y documéntalo. |
| **Hojas adicionales vacías.** | `solola.xlsx` | Lee la hoja que contiene los datos, no la primera por posición a ciegas. |
| **Conteo de municipios inflado.** | Efecto del caso `00-`. | El total nacional de municipios con datos debe quedar alrededor de **340**, no cerca de 384. |

Atajo de verificación: si tu proceso reporta **17 municipios para Guatemala** y un total cercano a
**4,298,887 registros**, vas bien. Si Guatemala te da 39, no normalizaste el prefijo `00-`.

### Cifras para validar tu lectura

| Indicador | Valor esperado |
|---|---|
| Total de registros | 4,298,887 |
| Sector: Público / Privado / Cooperativa / Municipal | 74.7% / 20.9% / 4.0% / 0.3% |
| Área: Rural / Urbana | 61.4% / 38.6% |
| Sexo: Hombre / Mujer | 50.7% / 49.3% |
| Nivel: Primaria / Básico / Preprimaria / Diversificado | 56.4% / 17.8% / 17.1% / 8.5% |
| Resultado: Promovido / No promovido / Retirado | 85.2% / 9.2% / 5.5% |
| Municipios en el departamento de Guatemala | 17 |

---

## Archivos

El dataset se entrega en 23 archivos `.xlsx`: uno por departamento más el diccionario de variables.

### Diccionario de variables

Empieza por aquí: es el archivo que traduce todos los códigos.

| Archivo | Tamaño | Descarga |
|---|---|---|
| `diccionario_de_variables.xlsx` | 25 KB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/diccionario_de_variables.xlsx |

### Datos por departamento

| Departamento | Archivo | Registros | Tamaño | Descarga |
|---|---|---:|---:|---|
| Alta Verapaz | `alta_verapaz.xlsx` | 391,085 | 20.3 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/alta_verapaz.xlsx |
| Baja Verapaz | `baja_verapaz.xlsx` | 81,736 | 4.2 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/baja_verapaz.xlsx |
| Chimaltenango | `chimaltenango.xlsx` | 166,965 | 8.6 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/chimaltenango.xlsx |
| Chiquimula | `chiquimula.xlsx` | 127,409 | 6.6 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/chiquimula.xlsx |
| El Progreso | `el_progreso.xlsx` | 49,803 | 2.5 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/el_progreso.xlsx |
| Escuintla | `escuintla.xlsx` | 207,618 | 10.7 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/escuintla.xlsx |
| Guatemala | `guatemala.xlsx` | 863,879 | 42.5 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/guatemala.xlsx |
| Huehuetenango | `huehuetenango.xlsx` | 316,771 | 16.5 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/huehuetenango.xlsx |
| Izabal | `izabal.xlsx` | 120,326 | 6.2 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/izabal.xlsx |
| Jalapa | `jalapa.xlsx` | 99,625 | 5.1 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/jalapa.xlsx |
| Jutiapa | `jutiapa.xlsx` | 134,571 | 6.9 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/jutiapa.xlsx |
| Petén | `peten.xlsx` | 169,629 | 8.8 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/peten.xlsx |
| Quetzaltenango | `quetzaltenango.xlsx` | 232,627 | 12.0 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/quetzaltenango.xlsx |
| Quiché | `quiche.xlsx` | 268,998 | 14.0 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/quiche.xlsx |
| Retalhuleu | `retalhuleu.xlsx` | 98,128 | 5.1 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/retalhuleu.xlsx |
| Sacatepéquez | `sacatepequez.xlsx` | 91,552 | 4.7 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/sacatepequez.xlsx |
| San Marcos | `san_marcos.xlsx` | 303,565 | 15.8 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/san_marcos.xlsx |
| Santa Rosa | `santa_rosa.xlsx` | 108,264 | 5.6 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/santa_rosa.xlsx |
| Sololá | `solola.xlsx` | 122,831 | 6.3 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/solola.xlsx |
| Suchitepéquez | `suchitepequez.xlsx` | 159,287 | 8.3 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/suchitepequez.xlsx |
| Totonicapán | `totonicapan.xlsx` | 113,139 | 5.8 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/totonicapan.xlsx |
| Zacapa | `zacapa.xlsx` | 71,079 | 3.7 MB | https://hackaton-aibuildersgt-datos.s3.us-east-1.amazonaws.com/zacapa.xlsx |

**Total:** 4,298,887 registros.


---

# Desafío

## Reto

Haz que el dataset de Educación Formal 2024 sea **entendible**. Hoy son millones de filas con
códigos numéricos que solo alguien del área puede interpretar; tu trabajo es convertirlos en
información que cualquier persona pueda leer y consultar.

Flujo: datos codificados → tu solución con IA → información comprensible.

### Los tres componentes

La solución se construye con tres piezas que se conectan entre sí. Cada una depende de la anterior.

**1. Ingesta de datos**

Un proceso que lee los archivos del dataset y los **decodifica con el diccionario de variables**,
de modo que los valores queden en palabras y no en números. Debe dejar los datos listos para que el
dashboard y el agente los consuman.

Aquí es donde se define si tu análisis va a ser correcto: si la ingesta interpreta mal los datos,
todo lo que se muestre después estará mal.

**2. Dashboard con gráficas y análisis**

Una interfaz que presente los datos mediante **gráficas claras** acompañadas de **análisis
escrito**: no basta con mostrar la visualización, hay que explicar qué significa y qué se concluye
de ella.

El público objetivo es alguien **sin formación técnica ni estadística**. Las etiquetas deben ser
legibles y las cifras que afirmes tienen que corresponder con los datos reales.

**3. Agente que explique en lenguaje natural**

Un agente conversacional al que se le pueda preguntar y que responda en **lenguaje natural**, tanto
sobre **los datos** ("cuántos estudiantes de primaria hay en Alta Verapaz") como sobre **el análisis
que generó tu dashboard** ("por qué señalas ese nivel como el más crítico").

Debe apoyarse en la información ya procesada y **no inventar cifras**. Si le preguntan algo que el
dataset no permite responder, lo correcto es que lo diga.

### Mínimo esperado

- La ingesta procesa el dataset y entrega los valores decodificados.
- El dashboard muestra al menos una vista general y una desagregación (por ejemplo, por departamento
  y por nivel), cada una con su análisis escrito.
- El agente responde consultas sobre los datos y al menos una pregunta sobre el análisis del
  dashboard.

Usar IA está permitido y se espera: es parte del producto y también una herramienta de desarrollo
válida. Lo que se evalúa es cuánto **comprendes y puedes explicar** lo que construiste.

---

## Reglas

- **Equipos de 1 a 5 personas.** Puedes participar solo si así lo prefieres.
- **El proyecto se construye durante el hackatón.** No se vale presentar algo que ya tenías hecho.
- **Usar IA está permitido y se espera.** Documenta qué usaste y para qué. Lo que se evalúa es que
  comprendas lo que entregas.
- **Puedes usar librerías, frameworks y servicios de terceros** libremente.
- **El dataset entregado es la base.** Si sumas datos externos, que sean públicos y citados.
- **No inventes datos** ni cifras en tus análisis.
- **Sin credenciales ni llaves** en el repositorio.
- **Presentarse al pitch es obligatorio** para ser evaluado.
- **Respeto entre participantes** y con el equipo organizador.
- **Las decisiones del jurado son finales.**

Si tienes duda sobre si algo está permitido, pregunta a los organizadores antes de asumir.

---

## Sugerencias: desarrollo asistido con IA

Vas a usar IA para construir esto, y está bien. La diferencia entre un proyecto que sostienes y uno
que se te va de las manos está en **cómo** la usas: como asistente que ejecuta y valida lo que tú
diseñaste, no como alguien a quien le delegas el proyecto completo.

### Quién hace qué

La regla práctica: **el criterio es tuyo, la ejecución puede ser compartida.**

**Tú decides**

- Entender el problema y qué se quiere lograr.
- El análisis: qué preguntas responderán los datos.
- El diseño: qué componentes hay y cómo se conectan.
- Las decisiones técnicas y por qué se tomaron.
- Qué código entra al proyecto y qué se descarta.

**La IA asiste**

- Implementar lo que ya definiste.
- Explicarte lo que no entiendes de un lenguaje o librería.
- Revisar tu diseño y señalar huecos o riesgos.
- Validar resultados y ayudarte a encontrar errores.
- Proponer alternativas para que tú elijas.

### Un ciclo de trabajo que funciona

1. **Piensa antes de pedir.** Antes de escribir un solo prompt, ten claro qué vas a construir y por
   qué. Si le pides a la IA que resuelva algo que tú no has entendido, no vas a poder juzgar si lo
   hizo bien.
2. **Diseña tú, y deja que la IA critique.** Plantea tu diseño y pídele que lo cuestione: qué se te
   escapó, qué se puede simplificar, qué va a fallar cuando crezca. Usarla como revisor es mucho más
   valioso que usarla como generadora de arquitecturas que no elegiste.
3. **Pide en pedazos pequeños.** Una función, un módulo, un paso. "Hazme todo el proyecto" produce
   código que nadie revisó y que nadie puede explicar.
4. **Lee y entiende antes de integrar.** Si te entrega algo que no comprendes, pídele que te lo
   explique antes de pegarlo. Si sigue sin quedar claro, pide una versión más simple. Código que no
   entiendes es deuda que vas a pagar en la ronda de preguntas.
5. **Verifica contra la realidad.** La IA puede producir cifras convincentes y equivocadas. Contrasta
   lo que salga con los datos: usa las cifras de referencia de la sección Contenido como control.
6. **Documenta mientras avanzas.** Anota por qué tomaste cada decisión, en tus palabras. Es lo que te
   va a permitir explicar el proyecto después.

### Señales de que perdiste el control

- Hay archivos en tu proyecto que no sabes qué hacen.
- No puedes explicar por qué el código está organizado así.
- Tienes dependencias instaladas que no recuerdas haber elegido.
- Cuando algo falla, tu única estrategia es volver a pedirle a la IA que lo arregle.
- El proyecto funciona, pero no sabrías por dónde empezar a modificarlo.

**Cómo recuperarlo:** deja de agregar cosas. Recorre lo que ya tienes y pídele a la IA que te
explique cada parte hasta que puedas explicarla tú. Borra lo que no aporta. Un proyecto más pequeño
que dominas vale más que uno grande que no.

### Cambia la forma de pedir

| En vez de | Pide |
|---|---|
| "Hazme el dashboard" | "Necesito una gráfica de X por Y. Propón dos formas y dime ventajas de cada una" |
| "Arréglalo" | "Explícame por qué falla antes de proponer el arreglo" |
| "Dame el código" | "Dame el código y explícame qué hace cada parte y por qué así" |
| "¿Está bien mi proyecto?" | "Este es mi diseño: ¿qué problemas le ves y qué estoy asumiendo sin querer?" |

Nada de esto es para que uses menos IA, sino para que llegues al final **con el dominio de tu
proyecto**. Es exactamente lo que se evalúa con mayor peso.


---

# Evaluación

## Criterios

El entregable se califica sobre **100 puntos**. El mayor peso no está en qué tan vistosa quedó la
herramienta, sino en **qué tanto comprendes y puedes explicar lo que construiste**.

Agrupado: 40 arquitectura y código · 30 comprensión de tu solución · 15 cumplir el reto ·
15 prácticas y reproducibilidad.

### Desglose

| Peso | Criterio | Qué se evalúa |
|---:|---|---|
| 30 | **Comprensión de tu solución** | Que puedas explicar tu arquitectura y tu código: por qué lo armaste así, qué hace cada parte y por qué elegiste esas herramientas. Es el criterio de mayor peso. Si no puedes explicarlo, se evidencia que solo se lo pediste a una IA. |
| 20 | **Calidad de arquitectura** | Que los tres componentes (ingesta, dashboard y agente) estén bien delimitados, con decisiones coherentes que puedas justificar, y que el flujo de datos sea rastreable. |
| 20 | **Calidad de código** | Legibilidad, modularidad, nombres claros, manejo de errores, y ausencia de duplicación y código muerto. |
| 15 | **La herramienta cumple el reto** | Que el dashboard muestre y explique la información, y que el agente responda. Aquí entra el tratamiento correcto de los datos: cifras que cuadren, etiquetas legibles y análisis que no engañe. |
| 10 | **Buenas prácticas** | README completo, repositorio ordenado, decisiones documentadas y sin secretos ni credenciales en la entrega. |
| 5 | **Reproducibilidad** | Que el proyecto arranque siguiendo tu propia documentación, ya sea en local o en la nube. |

### Cómo se aplica cada criterio

Dentro de su peso, cada criterio se ubica en uno de estos niveles:

- **Excelente:** cumple de forma sobresaliente, con decisiones justificadas.
- **Bueno:** sólido, con detalles menores por pulir.
- **Aceptable:** cumple lo mínimo, con vacíos notables.
- **Insuficiente:** no cumple o comete errores que invalidan el resultado.

El uso de IA **no resta puntos**. Lo que resta es no poder explicar ni justificar lo que entregaste.
Un equipo puede generar buena parte con IA y aun así obtener el puntaje completo si demuestra que lo
comprende y lo controla.

---

## Pitch

Un **representante del equipo** expone ante los jueces qué hizo y cómo lo hizo. Después viene una
ronda de preguntas. En total, **10 minutos** por equipo: 5 de exposición y 5 de preguntas.

### La exposición · 5 minutos

Un integrante del equipo presenta el proyecto. No es una demostración de ventas: los jueces quieren
entender **qué construyeron** y, sobre todo, **cómo lo construyeron**. Cubre estos dos frentes:

- **Qué hicieron:** qué resuelve la solución, qué muestra el dashboard y qué puede responder el agente.
- **Cómo lo hicieron:** cómo está armado el proyecto, cómo se conectan los componentes, qué decisiones
  técnicas tomaron y qué papel tuvo la IA en el proceso.

### La ronda de preguntas · 5 minutos

Los jueces harán preguntas breves para confirmar que el equipo **comprende y controla lo que
entregó**. Son preguntas sobre su propio proyecto y su proceso, no un examen sobre educación ni
estadística.

Responder con seguridad y honestidad cuenta a favor. Decir "esto no lo alcanzamos" o "esto lo
generamos con IA y así funciona" es válido; lo que resta es no saber explicar lo que se entregó.

El pitch es la principal oportunidad para demostrar el criterio de mayor peso: la comprensión de su
propia solución.

---

## Sugerencias para el pitch

Cinco minutos se pasan rápido. Estas recomendaciones son para que aproveches el tiempo y llegues
tranquilo a tu presentación.

### Cómo estructurar tus 5 minutos

- **Medio minuto — el problema.** Una o dos frases: qué dataset es y por qué no se entiende tal como
  viene.
- **Un minuto y medio — qué construyeron.** Muestra el dashboard y el agente funcionando. Que se vea
  antes de explicarlo.
- **Dos minutos — cómo lo construyeron.** Los componentes, cómo se conectan y las decisiones que
  tomaron. Esta es la parte que más pesa.
- **Un minuto — aprendizajes y pendientes.** Qué les costó, qué resolverían distinto y qué quedó
  fuera.

### Recomendaciones prácticas

- **Ensáyalo al menos una vez completo y con reloj.** Es la diferencia entre terminar holgado y
  quedarte a medias.
- **Ten la herramienta ya abierta y lista** antes de empezar. No gastes tu tiempo levantando el
  proyecto o buscando la pestaña.
- **Prepara de antemano una pregunta para hacerle al agente** en vivo, y verifica que responde bien.
- **Explica el "por qué", no solo el "qué".** "Separamos la ingesta del dashboard porque así podíamos
  reprocesar sin tocar la interfaz" dice mucho más que "tenemos tres carpetas".
- **Usa lenguaje sencillo.** Si tu solución se entiende explicada de forma simple, se nota que la
  comprendes de verdad.
- **Sé transparente con el uso de IA.** Di qué generaste con IA y qué escribiste tú. Está permitido y
  se espera; ocultarlo solo genera dudas.

### Para la ronda de preguntas

- **Escucha la pregunta completa** antes de responder, y ve al punto: son respuestas de alrededor de
  un minuto.
- **Si no sabes algo, dilo.** "No llegamos a eso" o "esa parte no la alcancé a revisar a fondo" es
  mejor respuesta que inventar.
- **Anticipa lo previsible:** por qué eligieron sus herramientas, qué fue lo más difícil, qué harían
  con más tiempo.
- **Aunque exponga un representante, el equipo puede apoyar** si le preguntan algo de su parte.
  Coordinen quién responde qué.

### Qué evitar

- Gastar tres minutos en la introducción y llegar apurado a lo técnico.
- Leer diapositivas de corrido sin mostrar el proyecto funcionando.
- Mostrar cifras en el dashboard que no puedas explicar de dónde salen.
- Describir el código línea por línea: interesa el diseño, no el recorrido completo.

Un proyecto modesto bien entendido y bien explicado vale más que uno ambicioso que nadie del equipo
puede sustentar.


---

# Entrega

## Código

Entregas un **repositorio público** que cualquiera pueda clonar, levantar localmente y entender sin
ayuda de tu equipo.

### 1. Repositorio público

El código vive en un repositorio de acceso público. Debe contener la solución completa: la ingesta de
datos, el dashboard y el agente.

### 2. Reproducible localmente

Un tercero debe poder clonar el repositorio y **ponerlo a funcionar en su propia máquina** siguiendo
tus pasos. Declara las versiones y dependencias que hacen falta, y no dejes supuestos del entorno sin
documentar.

Si algún componente requiere servicios en la nube, explica cómo configurarlos, sin incluir
credenciales en el repositorio.

### 3. Instrucciones de uso

Pasos concretos y ordenados para instalar, ejecutar y usar la solución: cómo se corre la ingesta,
cómo se abre el dashboard y cómo se interactúa con el agente.

### 4. Documentación formal

Más allá del "cómo se ejecuta", la documentación debe explicar **cómo está construida la solución**:
la arquitectura, qué hace cada componente, las decisiones técnicas que tomaron y por qué, cómo
trataron los datos, y las limitaciones conocidas.

Documenta también **qué herramientas de IA usaron y para qué**.

### Antes de entregar, verifica

- El repositorio es público y contiene los tres componentes.
- Clonaste en limpio y el proyecto arranca siguiendo tus propias instrucciones.
- La documentación explica la arquitectura y las decisiones, no solo los comandos.
- No hay credenciales, llaves ni tokens en el código ni en el historial de commits.
- No incluiste artefactos regenerables como dependencias instaladas o builds.

La reproducibilidad y la documentación se califican directamente. Si el proyecto no arranca siguiendo
tu propio README, ese punto se pierde.

---

## Audiovisual

Además del código, entregas **dos videos** de un máximo de 3 minutos cada uno. Son cortos a
propósito: obligan a explicar lo esencial con claridad.

### Video 1 · Arquitectura del proyecto (máx. 3 min)

Explica **cómo está construida** la solución: qué componentes tiene, cómo se conectan entre sí, por
dónde fluyen los datos desde el archivo original hasta llegar al dashboard y al agente, y qué
tecnologías eligieron.

Lo importante es que se note que **comprenden su propio diseño**: no describan solo lo que hace,
expliquen por qué lo armaron así.

### Video 2 · Funcionamiento del proyecto (máx. 3 min)

Muestra la solución **en funcionamiento**: recorran el dashboard, expliquen qué se ve en las gráficas
y en los análisis, y hagan preguntas reales al agente para que se vea cómo responde.

Es una demostración, no una presentación de diapositivas: que se vea la herramienta corriendo.

### Consideraciones

- **Máximo 3 minutos cada uno.** Lo que exceda ese tiempo puede no tomarse en cuenta.
- Audio claro y pantalla legible. Si graban la pantalla, que el texto se pueda leer.
- Pueden participar varios integrantes del equipo, pero cuiden que se entienda la explicación.
