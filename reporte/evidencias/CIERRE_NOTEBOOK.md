## 5. Resultados y conclusiones

Se ejecutó el pipeline de Champions League en **Databricks** en dos formatos: Jupyter Notebook y archivo Python. Ambos utilizaron SVC con `RandomizedSearchCV`, 40 iteraciones y validación cruzada estratificada de cinco particiones, optimizando F1 macro.

| Métrica | Notebook | Archivo Python |
|---|---:|---:|
| F1 macro de validación cruzada | 0.637570 | 0.637570 |
| Desviación estándar del F1 de validación | 0.051826 | 0.051826 |
| Exactitud en prueba | 0.655172 | 0.655172 |
| F1 macro en prueba | 0.601010 | 0.601010 |
| F1 macro de referencia | 0.217054 | 0.217054 |
| Recarga del modelo verificada | Sí | Sí |

El conjunto contiene 144 partidos válidos: 115 para entrenamiento y 29 para prueba. Los hiperparámetros seleccionados fueron `C=0.17535949529764422`, `class_weight="balanced"`, `kernel="linear"` y `gamma=0.04609877941534893`. Con el kernel lineal, `gamma` no interviene en la decisión del clasificador.

**Trazabilidad de las ejecuciones**

- Notebook: `bfe4871fb7324ad8953efb6bb7fa33cb`.
- Modelo del notebook: `models:/m-39d842fe62224cad9b83571b60c45968`.
- Archivo Python: `79e0d6ade66c4631b2cb47482a6b49f3`.
- Modelo del archivo Python: `models:/m-fa7ce8e782ae498fb1a3f6bdecababdb`.

La igualdad de métricas confirma consistencia entre ambos formatos bajo la misma configuración y partición. El F1 macro de prueba supera la referencia de clase mayoritaria. La selección se basa en validación cruzada; los datos de prueba se utilizan para la evaluación final. El conjunto es pequeño y emplea estadísticas del encuentro, por lo que estos resultados no demuestran pronóstico previo al partido.

Se utilizaron **Experiments, Tracking, Dataset Tracking y MLflow Models**. Cada ejecución guardó parámetros, métricas, datasets, artefactos y el pipeline completo; la recarga reprodujo su F1 macro de prueba. `version=null` indica que no se registró una versión en Model Registry: el modelo sí está guardado en MLflow. Esta ejecución no incluye Feature Store, registro en Unity Catalog ni un endpoint de Model Serving.

### Enlaces de la entrega

- [Repositorio de GitHub](https://github.com/Andyfer004/Ejercicio5-MLOPS)
- [Notebook en el workspace de Databricks](https://dbc-5490c6a5-5215.cloud.databricks.com/editor/notebooks/2665096834519332?o=7474655525361249)
- [Run del notebook](https://dbc-5490c6a5-5215.cloud.databricks.com/ml/experiments/2665096834519373/runs/bfe4871fb7324ad8953efb6bb7fa33cb?o=7474655525361249)
- [Run del archivo Python](https://dbc-5490c6a5-5215.cloud.databricks.com/ml/experiments/2665096834519373/runs/79e0d6ade66c4631b2cb47482a6b49f3?o=7474655525361249)

El acceso a los recursos de Databricks depende de los permisos del workspace.
