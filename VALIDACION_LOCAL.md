# Validación local de la adaptación

Fecha: 16 de octubre de 2026. Todas las ejecuciones descritas se realizaron localmente; no se estableció conexión con Databricks.

## Comprobaciones realizadas

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

**Estas cifras son de una prueba local corta de esta adaptación.** No reproducen la búsqueda completa del taller ni constituyen resultados de Databricks. El reporte conserva exclusivamente las cifras históricas del Taller 3. El notebook de entrega se publica sin salidas para su ejecución posterior; las salidas del notebook 03 se conservan como referencia histórica.

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

## Pendiente en Databricks

Ejecutar ambos formatos con el tracking administrado, verificar artefactos y permisos reales, ejecutar la búsqueda completa si se requiere y compartir el enlace real del notebook. Unity Catalog, su alias y Model Serving no se validaron localmente ni se configuraron remotamente. Los pasos están en el README y la guía de ejecución.
