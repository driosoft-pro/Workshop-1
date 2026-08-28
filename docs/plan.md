# Plan de Proyecto — Workshop 1: Dimensional Data Warehouse

**Proyecto:** Data Warehouse de Reclutamiento de Candidatos  
**Autor:** Deyton Riascos Ortiz  
**Fecha de Inicio:** 2026-08-28  
**Duración Estimada:** 2 Sprints (4 semanas)

---

## Visión General del Proyecto

Construir un Data Warehouse dimensional que permita a la empresa de reclutamiento tecnológico analizar patrones de contratación, rendimiento por tecnología, perfiles de candidatos y tendencias temporales para tomar decisiones informadas sobre sus procesos de reclutamiento.

---

## Sprint 1: Fundamentos y Modelo Dimensional

**Duración:** 2 semanas  
**Objetivo:** Comprender los requisitos del negocio, perfilar los datos y diseñar el modelo dimensional.

### Historias de Usuario

#### HU-01: Comprensión de Requisitos del Negocio
**Como** ingeniero de datos, **quiero** entender los 5 requisitos analíticos del negocio **para que** pueda diseñar un modelo dimensional que los satisfaga.

**Criterios de Aceptación:**
- [ ] Los 5 requisitos (R1-R5) están documentados y comprendidos
- [ ] Cada requisito tiene una pregunta de negocio clara
- [ ] Se identifican los datos necesarios para cada requisito
- [ ] Se definen los resultados analíticos esperados

**Tareas:**
1. Analizar el enunciado del workshop
2. Documentar los requisitos R1-R5 en la tabla de trazabilidad
3. Definir R4 y R5 (requerimientos adicionales propuestos)
4. Validar que los requisitos sean analíticos y no solo consultas simples

**Estimación:** 4 horas

---

#### HU-02: Perfilamiento Inicial de Datos
**Como** ingeniero de datos, **quiero** perfilar el dataset de candidatos **para que** pueda tomar decisiones informadas sobre transformaciones y modelado.

**Criterios de Aceptación:**
- [ ] Se cuenta el número de filas y columnas
- [ ] Se identifican tipos de datos por columna
- [ ] Se detectan valores faltantes y duplicados
- [ ] Se analizan rangos de fechas y scores
- [ ] Se documentan hallazgos principales

**Tareas:**
1. Crear notebook `data_profiling.ipynb`
2. Cargar el CSV y explorar estructura
3. Analizar valores faltantes por columna
4. Detectar registros duplicados
5. Calcular estadísticas descriptivas para scores
6. Analizar distribución de países, seniority y tecnologías
7. Documentar hallazgos en el notebook

**Estimación:** 6 horas

---

#### HU-03: Diseño del Modelo Dimensional (Star Schema)
**Como** ingeniero de datos, **quiero** diseñar un Star Schema que satisfaga los 5 requisitos **para que** el Data Warehouse sea funcional y escalable.

**Criterios de Aceptación:**
- [ ] Se identifica el proceso de negocio
- [ ] Se declara el grain de la tabla de hechos
- [ ] Se diseñan las dimensiones necesarias
- [ ] Se definen las medidas y hechos
- [ ] Se crea el diagrama del Star Schema
- [ ] Se valida que el modelo soporta todos los requisitos

**Tareas:**
1. **Paso 1:** Identificar el proceso de negocio (Reclutamiento de Candidatos)
2. **Paso 2:** Declarar el grain (una fila = una aplicación de candidato evaluada)
3. **Paso 3:** Diseñar dimensiones:
   - `dim_date` (temporal)
   - `dim_technology` (tecnología)
   - `dim_candidate` (candidato: nombre, país, experiencia, seniority)
   - `dim_assessment` (evaluación: scores)
4. **Paso 4:** Definir medidas:
   - `is_hired` (resultado de contratación)
   - `code_challenge_score`
   - `technical_interview_score`
   - `application_count`
5. **Paso 5:** Crear diagrama Star Schema
6. **Paso 6:** Validar contra los 5 requisitos

**Estimación:** 8 horas

---

#### HU-04: Configuración del Entorno
**Como** desarrollador, **quiero** configurar el entorno de desarrollo **para que** pueda implementar el ETL de forma reproducible.

**Criterios de Aceptación:**
- [ ] Se crea `requirements.txt` con dependencias
- [ ] Se crea `.gitignore` apropiado
- [ ] Se estructuran los directorios del proyecto
- [ ] Se configura la conexión a la base de datos

**Tareas:**
1. Crear estructura de directorios
2. Crear `requirements.txt`
3. Crear `.gitignore`
4. Configurar variables de conexión a PostgreSQL
5. Crear script `sql/create_tables.sql`

**Estimación:** 3 horas

---

### Entregables Sprint 1

- [ ] `notebooks/data_profiling.ipynb` — Perfilamiento de datos
- [ ] Documentación de requisitos (en README o documento separado)
- [ ] Diagrama `diagrams/star_schema.png`
- [ ] `sql/create_tables.sql` — Script de creación de tablas
- [ ] Estructura de directorios completa
- [ ] `requirements.txt` y `.gitignore`

---

## Sprint 2: ETL, Carga y Análisis

**Duración:** 2 semanas  
**Objetivo:** Implementar el pipeline ETL, cargar el Data Warehouse y generar análisis.

### Historias de Usuario

#### HU-05: Implementar Extracción de Datos
**Como** ingeniero de datos, **quiero** implementar la extracción del CSV **para que** pueda procesar los datos de forma programática.

**Criterios de Aceptación:**
- [ ] Se lee el CSV correctamente con Pandas
- [ ] Se preserva el archivo original
- [ ] Se carga en un DataFrame para procesamiento
- [ ] No se realizan transformaciones durante la extracción

**Tareas:**
1. Crear `src/extract.py`
2. Implementar función para leer CSV
3. Manejar encoding y delimitador
4. Validar estructura del DataFrame

**Estimación:** 3 horas

---

#### HU-06: Implementar Transformación de Datos
**Como** ingeniero de datos, **quiero** implementar las transformaciones necesarias **para que** los datos estén listos para el modelo dimensional.

**Criterios de Aceptación:**
- [ ] Se corrigen tipos de datos
- [ ] Se manejan valores faltantes
- [ ] Se implementa la regla de negocio `is_hired`
- [ ] Se crean atributos derivados para requisitos
- [ ] Se documentan decisiones de transformación

**Tareas:**
1. Crear `src/transform.py`
2. Convertir `Application Date` a datetime
3. Implementar regla: `is_hired = (code_score >= 7) AND (interview_score >= 7)`
4. Crear rangos de experiencia para R3
5. Manejar valores faltantes si existen
6. Validar tipos de datos

**Estimación:** 5 horas

---

#### HU-07: Implementar Modelo Dimensional
**Como** ingeniero de datos, **quiero** transformar los datos en estructuras dimensionales **para que** pueda cargar el Data Warehouse.

**Criterios de Aceptación:**
- [ ] Se crean los datasets de dimensiones
- [ ] Se eliminan duplicados en dimensiones
- [ ] Se generan surrogate keys
- [ ] Se mapean foreign keys a la tabla de hechos
- [ ] Se crea la tabla de hechos según el grain

**Tareas:**
1. Crear `src/dimensional_model.py`
2. Crear `dim_date` con surrogate keys
3. Crear `dim_technology` con surrogate keys
4. Crear `dim_candidate` con surrogate keys
5. Crear `dim_assessment` con surrogate keys
6. Mapear keys a tabla de hechos
7. Crear `fact_applications`

**Estimación:** 8 horas

---

#### HU-08: Cargar Data Warehouse
**Como** ingeniero de datos, **quiero** cargar las tablas en PostgreSQL **para que** el Data Warehouse esté disponible para análisis.

**Criterios de Aceptación:**
- [ ] Las dimensiones se cargan primero
- [ ] La tabla de hechos se carga después
- [ ] Se validan primary keys y foreign keys
- [ ] Se verifica integridad referencial
- [ ] Se confirma el número de registros cargados

**Tareas:**
1. Crear `src/load.py`
2. Implementar conexión a PostgreSQL
3. Cargar dimensiones en orden correcto
4. Cargar tabla de hechos
5. Ejecutar validaciones de integridad
6. Documentar resultados de carga

**Estimación:** 5 horas

---

#### HU-09: Implementar Consultas Analíticas
**Como** analista, **quiero** ejecutar consultas SQL que respondan los 5 requisitos **para que** pueda generar insights de negocio.

**Criterios de Aceptación:**
- [ ] Hay al menos una consulta por requisito (R1-R5)
- [ ] Las consultas se ejecutan contra el Data Warehouse
- [ ] Cada consulta tiene resultado e interpretación
- [ ] Los resultados son consistentes con el modelo

**Tareas:**
1. Crear `sql/analytical_queries.sql`
2. Implementar consulta R1 (Tendencias temporales)
3. Implementar consulta R2 (Análisis por tecnología)
4. Implementar consulta R3 (Perfil de candidato)
5. Implementar consulta R4 (Análisis geográfico)
6. Implementar consulta R5 (Correlación de evaluaciones)
7. Documentar resultados e interpretaciones

**Estimación:** 6 horas

---

#### HU-10: Visualización BI
**Como** analista, **quiero** crear visualizaciones en herramienta BI **para que** los hallazgos sean comunicados efectivamente.

**Criterios de Aceptación:**
- [ ] Al menos 3 visualizaciones creadas
- [ ] Incluye análisis temporal
- [ ] Incluye análisis comparativo
- [ ] Incluye análisis de R4 o R5
- [ ] Cada visualización identifica el requisito que soporta
- [ ] Los datos provienen del Data Warehouse

**Tareas:**
1. Conectar herramienta BI al Data Warehouse
2. Crear visualización temporal (R1)
3. Crear visualización comparativa (R2 o R3)
4. Crear visualización de R4 o R5
5. Documentar interpretaciones
6. Exportar resultados a `results/`

**Estimación:** 6 horas

---

#### HU-11: Validación Final y Documentación
**Como** desarrollador, **quiero** validar que el sistema cumple todos los requisitos **para que** el proyecto esté completo y documentado.

**Criterios de Aceptación:**
- [ ] Los 5 requisitos están implementados y validados
- [ ] El README está completo con toda la documentación
- [ ] El repositorio está organizado en GitHub
- [ ] Se puede reproducir el proyecto desde cero

**Tareas:**
1. Crear script `src/main.py` (orquestador)
2. Ejecutar pipeline completo end-to-end
3. Validar tabla de requisitos finales
4. Actualizar README si es necesario
5. Preparar repositorio para GitHub
6. Crear commit final

**Estimación:** 4 horas

---

### Entregables Sprint 2

- [ ] `src/extract.py` — Módulo de extracción
- [ ] `src/transform.py` — Módulo de transformación
- [ ] `src/dimensional_model.py` — Modelo dimensional
- [ ] `src/load.py` — Módulo de carga
- [ ] `src/main.py` — Orquestador del ETL
- [ ] `sql/analytical_queries.sql` — Consultas analíticas
- [ ] `results/` — Resultados y visualizaciones
- [ ] Data Warehouse poblado y validado
- [ ] Documentación completa en README

---

## Cronograma Resumen

| Sprint | Semana | Actividades Principales | Horas Est. |
|--------|--------|------------------------|------------|
| Sprint 1 | Semana 1 | Requisitos, Perfilamiento, Diseño | 10 |
| Sprint 1 | Semana 2 | Modelo Dimensional, Configuración | 11 |
| Sprint 2 | Semana 3 | Extracción, Transformación, Dimensional | 16 |
| Sprint 2 | Semana 4 | Carga, Análisis, BI, Validación | 21 |
| **Total** | **4 semanas** | | **58 horas** |

---

## Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Datos faltantes o corruptos | Media | Alto | Perfilamiento temprano, manejo de nulos |
| Modelo dimensional insuficiente | Baja | Alto | Validación contra requisitos antes de implementar |
| Problemas de conexión a BD | Media | Medio | Usar SQLite como fallback |
| Complejidad del ETL | Media | Medio | Mantener transformaciones simples y documentadas |

---

## Definición de Completado

Un requisito se considera **completado** cuando:
1. Está implementado en código
2. Tiene una consulta SQL asociada
3. Genera un resultado válido desde el Data Warehouse
4. Tiene una interpretación documentada
5. Soporta una decisión de negocio identificada

---

## Criterios de Aceptación del Proyecto

- [ ] Los 5 requisitos de negocio están implementados
- [ ] El modelo dimensional es un Star Schema válido
- [ ] El ETL es reproducible con `python src/main.py`
- [ ] El Data Warehouse está poblado y consultable
- [ ] Hay al menos 5 consultas analíticas funcionando
- [ ] Hay al menos 3 visualizaciones BI
- [ ] El README permite a otro persona reproducir el proyecto
- [ ] El repositorio está en GitHub con estructura correcta
