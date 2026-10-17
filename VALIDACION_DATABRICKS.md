# Validación real en Databricks

Fecha suministrada: 16 de octubre de 2026, America/Guatemala. **Procedencia:** resultados proporcionados por el usuario y observados por este en las salidas del notebook de Databricks. Se incorporan el JSON y las capturas recibidas; este cierre no abrió sesiones de Databricks, no reentrenó y no cambió permisos.

- [Notebook del workspace](https://dbc-5490c6a5-5215.cloud.databricks.com/editor/notebooks/2665096834519332?o=7474655525361249).
- Experimento: `/Users/fue22944@uvg.edu.gt/Champions_Resultado_Databricks`; ID `2665096834519373`.
- Datos: 151 filas crudas, 144 partidos válidos, 115 de entrenamiento y 29 de prueba.
- Configuración: SVC, 40 iteraciones, 5 folds, F1 macro, semilla 42, `MODELO_UC=None`.

| Formato | Run | MLflow Model |
|---|---|---|
| Notebook | `bfe4871fb7324ad8953efb6bb7fa33cb` | `models:/m-39d842fe62224cad9b83571b60c45968` |
| Python | `79e0d6ade66c4631b2cb47482a6b49f3` | `models:/m-fa7ce8e782ae498fb1a3f6bdecababdb` |

- [Run del notebook](https://dbc-5490c6a5-5215.cloud.databricks.com/ml/experiments/2665096834519373/runs/bfe4871fb7324ad8953efb6bb7fa33cb?o=7474655525361249).
- [Run del archivo Python](https://dbc-5490c6a5-5215.cloud.databricks.com/ml/experiments/2665096834519373/runs/79e0d6ade66c4631b2cb47482a6b49f3?o=7474655525361249).

El `.py` se ejecutó mediante `runpy` como `__main__` dentro del mismo notebook, **no como Job independiente**.

| Métrica | Notebook | Python |
|---|---:|---:|
| F1 macro CV | 0.6375702586700029 | 0.6375702586700029 |
| Desviación estándar CV | 0.05182572468993785 | 0.05182572468993785 |
| Exactitud prueba | 0.6551724137931034 | 0.6551724137931034 |
| F1 macro prueba | 0.6010101010101011 | 0.6010101010101011 |
| F1 macro referencia | 0.2170542635658915 | 0.2170542635658915 |
| Recarga verificada | Sí | Sí |

Hiperparámetros: `C=0.17535949529764422`, `class_weight="balanced"`, `kernel="linear"`, `gamma=0.04609877941534893`. Gamma no interviene con el kernel lineal.

## Alcance demostrado y procedencia

Se utilizaron Experiments, Tracking, Dataset Tracking y MLflow Models. El valor `version=null` de ambos resultados indica que no se registró una versión en Unity Catalog: **no hubo alias nuevo ni endpoint de Model Serving**. La recarga fue verificada en ambos formatos según los resultados suministrados.

El pipeline y dataset proceden del Taller 3, con créditos en [CREDITOS.md](CREDITOS.md). Sus métricas históricas se conservan como antecedentes y se distinguen por su procedencia de los dos runs de esta entrega, aunque coincidan al redondear. Las pruebas locales están en [VALIDACION_LOCAL.md](VALIDACION_LOCAL.md).

## Evidencia publicada

- [resultados_databricks.json](reporte/evidencias/resultados_databricks.json): archivo recibido íntegro, con parámetros, métricas, IDs y enlaces de ambos formatos.
- [Configuración](reporte/evidencias/configuracion_databricks.png) y [salida del notebook](reporte/evidencias/resultado_notebook.png): capturas del usuario, sin credenciales visibles. No se recibió una captura adicional del run Python; su resultado está documentado en el JSON y el reporte suministrados.
- [Cierre Markdown recibido](reporte/evidencias/CIERRE_NOTEBOOK.md), incorporado en la sección 5 del notebook.
- [Reporte final](reporte/MLflow_Databricks.pdf) y [fuente final](reporte/MLflow_Databricks.tex): adjuntos conservados íntegros, con las imágenes en las rutas relativas esperadas.

Al iniciar el cierre, el notebook local y el remoto coincidían y no contenían salidas de Databricks. No se recibió un notebook ejecutado exportado. Por eso el notebook publicado **documenta la ejecución con Markdown/JSON** y conserva vacíos `outputs` y `execution_count`; no se generaron resultados artificiales. Se mantuvieron las celdas de preparación y entrenamiento, se corrigieron las importaciones/configuración y se añadió la celda `runpy` que no existía en la versión disponible.
