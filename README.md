# Champions League: MLflow en Databricks

Laboratorio de Machine Learning Engineering, Universidad del Valle de Guatemala.
**Andy Fuentes, Diederich Solís, Diego Linares y Christian Echeverria.**

Repositorio de la entrega: [Andyfer004/Ejercicio5-MLOPS](https://github.com/Andyfer004/Ejercicio5-MLOPS).
Pipeline, dataset y notebook de referencia proceden del [Taller 3 original](https://github.com/DiegoLinares11/MLFlow), commit `bd619c3cea3eb2d00fb6732e2993530d87de3f39`. Véase [CREDITOS.md](CREDITOS.md).

Se reutiliza Champions League con SVC, regresión logística, HistGradientBoosting y Random Forest. El notebook y el script usan el mismo entrenamiento: preprocesamiento dentro de cada fold, `RandomizedSearchCV`, F1 macro y prueba estratificada reservada. No utiliza Iris. El dataset contiene estadísticas del partido; estos resultados **no validan un pronóstico previo al encuentro**.

| Entregable | Ubicación |
|---|---|
| Notebook de entrega | [notebooks/Champions_Databricks.ipynb](notebooks/Champions_Databricks.ipynb) |
| Script de entrega | [pipeline_champions_databricks.py](pipeline_champions_databricks.py) |
| Reporte final y fuente | [PDF](reporte/MLflow_Databricks.pdf), [LaTeX](reporte/MLflow_Databricks.tex) |
| Notebook histórico del Taller 3 | [notebooks/03_pipeline_sklearn_mlflow.ipynb](notebooks/03_pipeline_sklearn_mlflow.ipynb) |
| Paquete y dataset | [src/taller3_pipeline/](src/taller3_pipeline/), [CSV](src/taller3_pipeline/datasets/champions_league_matches.csv) |
| Adjuntos recibidos sin modificar y reporte original | [referencias/](referencias/) |
| Guía detallada de Databricks | [GUIA_EJECUCION.md](GUIA_EJECUCION.md) |

**Laboratorio ejecutado en ambos formatos en Databricks.** [Notebook real](https://dbc-5490c6a5-5215.cloud.databricks.com/editor/notebooks/2665096834519332?o=7474655525361249). Evidencia suministrada por el usuario y observada por este en Databricks: [validación y trazabilidad](VALIDACION_DATABRICKS.md), [JSON con precisión completa](reporte/evidencias/resultados_databricks.json) y [capturas](reporte/evidencias/).

El notebook ejecutado no se recibió como archivo exportado ni estaba incorporado en `origin/main` al iniciar el cierre. El notebook de GitHub documenta la ejecución mediante Markdown/JSON y conserva celdas sin salidas; no se fabricaron outputs, contadores ni logs. El notebook 03 conserva las salidas históricas del Taller 3.

## Instalación local

Desde esta misma carpeta, con Python 3.11 o 3.12 recomendado (paquete: Python >=3.10):

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

En Windows active con `.venv\Scripts\activate`. `requirements.txt` instala el proyecto editable y el extra de notebooks; las dependencias están centralizadas en `pyproject.toml`. Se fija MLflow 3.17.1 por la API `skops_trusted_types` del código original y se incluye `skops`. No hace falta levantar un servidor para entrenar con SQLite.

## Ejecutar el archivo Python localmente

```bash
python pipeline_champions_databricks.py \
  --uri sqlite:///mlflow.db \
  --experimento Champions_Local_Python \
  --familia svc --n-iter 2 --folds 3
```

La prueba corta valida la integración. Para la búsqueda completa use `--n-iter 40 --folds 5`. Las otras claves de familia son `regresion_logistica`, `hist_gradient_boosting` y `random_forest`. No seleccione hiperparámetros usando el conjunto de prueba. La recarga del modelo debe producir `recarga_verificada: true`.

Para ver los runs, desde la misma raíz:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 8080
```

Abra http://127.0.0.1:8080. La base y los artefactos locales están ignorados por Git.

## Ejecutar el Jupyter Notebook localmente

```bash
python -m ipykernel install --prefix .venv --name champions-local --display-name "Champions local"
jupyter lab notebooks/Champions_Databricks.ipynb
```

Seleccione el kernel del entorno virtual. Antes de ejecutar el entrenamiento, cambie explícitamente la configuración a modo local:

```python
URI = "sqlite:///" + str(RAIZ / "mlflow.db")
EXPERIMENTO = "Champions_Local_Notebook"
# Opcional para una prueba corta local:
N_ITER = 2
FOLDS = 3
```

El valor publicado por defecto es `URI = "databricks"`, con 40 iteraciones y 5 folds. Una repetición local crea runs distintos de la evidencia suministrada. El notebook añade la raíz y `raíz/src` a `sys.path` e importa `ejecutar` del script, sin duplicar el entrenamiento. El CSV se distribuye dentro del paquete.

## Ejecución documentada en Databricks

El usuario completó ambos formatos en el mismo entorno de Databricks. El archivo `.py` se ejecutó mediante `runpy.run_path(..., run_name="__main__")` desde el notebook: **no fue un Job independiente**. Este cierre incorpora la evidencia, sin volver a entrenar en Databricks ni modificar permisos.

Configuración utilizada y conservada en el notebook:

```python
URI = "databricks"
EXPERIMENTO = "/Users/fue22944@uvg.edu.gt/Champions_Resultado_Databricks"
FAMILIA = "svc"
N_ITER = 40
FOLDS = 5
MODELO_UC = None
```

Para reproducirlo posteriormente de forma deliberada:

1. Abra el Git folder de este mismo repositorio y `notebooks/Champions_Databricks.ipynb` en un compute Python. Instale sus dependencias según `pyproject.toml`; `%pip install -e "/ruta/real/Ejercicio5-MLOPS"` es una opción si el entorno la admite. Si reinicia Python, ejecute de nuevo la celda de rutas antes de las importaciones.
2. La celda de rutas busca la raíz desde la ubicación conocida del notebook (incluido el contexto del workspace si está disponible) y desde el directorio actual. Añade tanto la raíz como `src/`, sin depender de la instalación editable. Si serverless usa otro directorio, establezca `RUTA_WORKSPACE` con la ruta absoluta real del repositorio; una ruta explícita inválida produce un error claro. La ruta del Git folder es distinta de la del experimento.
3. Conserve la configuración anterior. Ejecutar la celda de entrenamiento o la celda `runpy` crea nuevas ejecuciones; los IDs registrados en la evidencia no se sustituyen por esos resultados posteriores.
4. La celda del script preserva `sys.argv`, configura los argumentos y ejecuta el archivo raíz como `__main__`. El propio script también añade su `src/` para resolver el paquete tras un reinicio.
5. En Experiments consulte los [runs suministrados](VALIDACION_DATABRICKS.md): parámetros, métricas, datasets, modelo y `evaluacion/verificacion_recarga.json`. Los dos modelos están guardados como MLflow Models con `version=null`: **sin versión registrada en Unity Catalog, sin alias nuevo y sin endpoint**.

[Notebook en Databricks](https://dbc-5490c6a5-5215.cloud.databricks.com/editor/notebooks/2665096834519332?o=7474655525361249). El acceso depende de los permisos existentes del workspace, que no se modificaron.

## MLflow y CRISP-DM

Experiments agrupa ejecuciones; Tracking registra parámetros, métricas, datasets y artefactos; Models conserva el pipeline reutilizable. Model Registry añade versiones y alias, y Unity Catalog su gobierno en Databricks. La comprensión del negocio y de los datos se documenta en notas y artefactos; la preparación se encapsula en el pipeline; modelado y evaluación se rastrean directamente. El despliegue requiere configurar servicios adicionales. El desarrollo y las referencias están en el [reporte](reporte/MLflow_Databricks.pdf).

## Resultados y validación

Los dos runs de Databricks suministrados por el usuario tienen F1 macro CV **0.6375702586700029**, desviación estándar **0.05182572468993785**, exactitud de prueba **0.6551724137931034**, F1 macro de prueba **0.6010101010101011** y referencia **0.2170542635658915**, con recarga verificada. Sus IDs y modelos están en [VALIDACION_DATABRICKS.md](VALIDACION_DATABRICKS.md) y el [JSON original recibido](reporte/evidencias/resultados_databricks.json).

Las cifras históricas redondeadas del Taller 3 (SVC: 0.638 / 0.655 / 0.601) se conservan como antecedentes en el notebook 03 y el reporte original. La coincidencia numérica no cambia su procedencia: las ejecuciones de esta entrega se identifican por sus propios runs. No se presentan las otras familias históricas como nuevas ejecuciones en Databricks.

[VALIDACION_LOCAL.md](VALIDACION_LOCAL.md) separa las pruebas locales iniciales y las comprobaciones de este cierre de la evidencia real en Databricks. El PDF final recibido contiene los resultados completos y sus enlaces; las pruebas locales cortas no los sustituyen.

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m build
```

El PDF se regenera desde la raíz con `cd reporte && tectonic MLflow_Databricks.tex` (requiere Tectonic; la primera compilación puede descargar paquetes TeX).

Fuentes oficiales: [MLflow en Databricks](https://docs.databricks.com/aws/en/mlflow/), [Tracking](https://docs.databricks.com/aws/en/mlflow/tracking), [Models en Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/) y [API scikit-learn de MLflow](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.sklearn.html).
