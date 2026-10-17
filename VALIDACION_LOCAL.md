# Validación local de la adaptación

Fecha: 16 de octubre de 2026. Todas las ejecuciones descritas se realizaron localmente; no se estableció conexión con Databricks.

## Comprobaciones de la integración inicial (commit 874fe00)

- Repositorio inicialmente vacío y sin commits; origin conservado: `git@github.com:Andyfer004/Ejercicio5-MLOPS.git`.
- Instalación editable del proyecto con extras `dev,notebook`; `pip check` sin dependencias incompatibles.
- `python -m pytest -q`: **5 pruebas aprobadas**. Una comprueba limpieza, clases y separación; las otras entrenan y recargan las cuatro familias reales con 1 iteración y 2 folds. Se verifican runs terminados, parámetros, métricas, datasets, firma del modelo y artefactos de evaluación/búsqueda.
- Script raíz ejecutado por su CLI con SQLite, SVC, 2 iteraciones y 3 folds.
- Notebook de entrega ejecutado completo con nbclient y un kernel del entorno virtual, desde `notebooks/`, con SQLite, SVC, 2 iteraciones y 3 folds. Sin celdas con error. Se validó también el esquema de ambos notebooks.
- `python -m build`: sdist y wheel construidas. Se instaló la wheel en una carpeta aislada y se importó desde fuera del repositorio; el CSV incluido coincide con el original y la carga devuelve 115 filas de entrenamiento y 29 de prueba.
- Paquete `src/taller3_pipeline/` y dataset idénticos byte a byte al commit original. Adjuntos ZIP y PDF conservados íntegros.
- PDF final recompilado con Tectonic, sin avisos de desbordamiento de texto; cinco páginas renderizadas y revisadas visualmente. Se verificaron las anotaciones de los enlaces de GitHub y la atribución de las métricas históricas a la página 10 del Taller 3.
- `.gitignore` comprobado para entorno virtual, temporales, SQLite, artefactos MLflow y archivos de configuración privados.

## Prueba corta de ambos formatos

| Formato | F1 macro CV | Accuracy prueba | F1 macro prueba | Recarga |
|---|---:|---:|---:|---|
| Notebook local | 0.592917 | 0.758621 | 0.646825 | Verificada |
| Python local | 0.592917 | 0.758621 | 0.646825 | Verificada |

Semilla 42; 151 filas crudas, 144 partidos, 115 filas de entrenamiento y 29 de prueba. Las clases contienen 71 Home Win, 48 Away Win y 25 Draw. Se registraron datasets de entrenamiento/prueba, métricas, modelo y verificación de recarga para ambos formatos.

**Estas cifras son de una prueba local corta de esta adaptación.** No reproducen la búsqueda completa del taller ni constituyen resultados de Databricks. El reporte inicial conservaba las cifras históricas del Taller 3. El reporte final recibido para el cierre documenta ahora los runs reales de Databricks por separado. El notebook de entrega documenta la ejecución mediante Markdown/JSON, sin salidas inventadas; el notebook 03 conserva las salidas históricas del taller.

## Entorno comprobado

| Componente | Versión |
|---|---|
| python | 3.11.14 |
| mlflow | 3.17.1 |
| scikit-learn | 1.8.0 |
| pandas | 3.0.6 |
| numpy | 2.4.6 |
| scipy | 1.17.1 |
| skops | 0.16.0 |

Las dependencias emitieron avisos de deprecación de SQLAlchemy/pandas y de detección de núcleos de joblib; no causaron fallos. El código usa un proceso para la búsqueda. No se ocultaron esos avisos en las pruebas.

## Cierre con evidencia de Databricks

El usuario ya ejecutó ambos formatos con 40 iteraciones y 5 folds. Los IDs, métricas completas, recarga y alcance real están en [VALIDACION_DATABRICKS.md](VALIDACION_DATABRICKS.md). El script se ejecutó con runpy como `__main__` dentro del notebook, no como Job. No se registraron versiones ni alias nuevos en Unity Catalog ni un endpoint.

Las verificaciones locales del cierre se documentan a continuación; no se ejecutó el notebook completo con su configuración Databricks ni se creó una ejecución remota nueva.

## Verificaciones realizadas durante el cierre

- `python -m pytest -q`: **9 pruebas aprobadas** (50.32 s). Incluye las cinco pruebas locales previas y cuatro pruebas de regresión: importaciones sin el atajo de instalación editable desde `notebooks/`, desde la ubicación conocida del notebook y con ruta explícita de workspace; además, argumentos de `runpy`, `run_name="__main__"` y restauración de `sys.argv` mediante una llamada simulada. Esta última prueba no ejecuta el script ni contacta Databricks.
- Las pruebas de entrenamiento de las cuatro familias usan SQLite local, una iteración y dos folds. No se presentan como nuevos resultados remotos. Se mantuvieron los avisos conocidos de dependencias, sin fallos.
- `pip check`: sin dependencias incompatibles.
- Esquemas de ambos notebooks y sintaxis de todas las celdas de código válidos. Configuración Databricks comprobada; celdas de datos y entrenamiento previas conservadas. Todos los `outputs` y `execution_count` del notebook de entrega siguen vacíos, como en el archivo disponible antes de editar.
- JSON comprobado contra los IDs, modelos, parámetros y métricas exactas solicitados. Su contenido, las imágenes, el cierre Markdown, el PDF y el LaTeX coinciden byte a byte con los adjuntos finales.
- PDF final recibido: nueve páginas renderizadas y revisadas visualmente, cuatro integrantes y enlaces reales de GitHub y Databricks presentes en las anotaciones. Sin sección de Canva ni notas de pendientes. Se validaron las rutas relativas de las imágenes de su fuente.
- Enlaces internos de la documentación y origin comprobados. Diff revisado y `git diff --check` sin errores de espacios.

No se ejecutó el notebook completo con `URI="databricks"` ni se alteraron los permisos del workspace. La evidencia remota es la proporcionada por el usuario, separada de las comprobaciones locales anteriores.
