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

**Notebook en Databricks:** pendiente de ejecución y de obtener su URL real. No se ha conectado a Databricks ni se presentan resultados de ese servicio. Después de ejecutar, agregue aquí el enlace compartido y actualice la sección 5 del fuente del reporte, recompilando el PDF. El contenido de Canva ya está elaborado y no se modifica.

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

Seleccione el kernel del entorno virtual y ejecute todas las celdas. La configuración inicial utiliza SQLite local con ruta absoluta y un experimento distinto al script. El notebook localiza la raíz desde `notebooks/` e importa `ejecutar` del script, sin duplicar el entrenamiento. El CSV se distribuye dentro del paquete.

## Ejecutar ambos formatos en Databricks

1. En Workspace, cree un **Git folder** de `https://github.com/Andyfer004/Ejercicio5-MLOPS.git`, rama `main`. Esto se realiza posteriormente dentro de Databricks; no requiere otro clon local. Use la integración GitHub de su cuenta para guardar cambios.
2. Abra `notebooks/Champions_Databricks.ipynb` y seleccione un compute Python con instalación de paquetes habilitada. Copie la ruta real de la raíz del Git folder.
3. En una celda separada instale el proyecto con `%pip install -e "/Workspace/Users/SU_USUARIO/Ejercicio5-MLOPS"`, sustituyendo la ruta. Si el entorno lo solicita, ejecute `dbutils.library.restartPython()` en otra celda, antes de las importaciones. En serverless gestione dependencias en el panel Environment cuando `%pip` o instalaciones editables estén restringidas; puede instalar una wheel construida con `python -m build`. Use compute compatible con las dependencias; no un SQL warehouse.
4. En la configuración del notebook cambie `URI = "databricks"` y `EXPERIMENTO = "/Users/SU_CORREO/Champions_Resultado_Databricks"`. Sustituya el correo por el usuario real y use una carpeta sobre la que tenga permisos. Deje `MODELO_UC = None` para la primera ejecución.
5. Ejecute todas las celdas con `N_ITER = 2`, `FOLDS = 3`. Compruebe recarga y artefactos. Luego use `N_ITER = 40`, `FOLDS = 5` y vuelva a ejecutar la celda de entrenamiento para la búsqueda completa.
6. Ejecute el punto de entrada del archivo Python desde una celda del mismo notebook, con el mismo entorno:

```python
import runpy
import sys

argumentos_previos = sys.argv[:]
try:
    sys.argv = [
        "pipeline_champions_databricks.py",
        "--uri", "databricks",
        "--experimento", EXPERIMENTO,
        "--familia", "svc", "--n-iter", "40", "--folds", "5",
    ]
    runpy.run_path(str(RAIZ / "pipeline_champions_databricks.py"), run_name="__main__")
finally:
    sys.argv = argumentos_previos
```

7. En **Experiments** abra el experimento: habrá runs con etiquetas `formato=notebook` y `formato=python`. Revise parámetros, `cv_f1_macro`, `test_accuracy`, `test_f1_macro`, baseline, datasets training/testing, matriz de confusión, `busqueda/cv_results.csv`, modelo y `evaluacion/verificacion_recarga.json`.
8. **Models**: `mlflow.sklearn.log_model` ya guarda un MLflow Model con firma, ejemplo de entrada y código de los transformadores. Opcionalmente configure un nombre real `catalogo.esquema.modelo` en `MODELO_UC`, o pase `--modelo-uc` al script. Se usa `databricks-uc`, se crea una versión y se asigna el alias `campeon`; debe hacerlo solo con el modelo que haya seleccionado por validación. Requiere Unity Catalog habilitado, compute compatible, `USE CATALOG`, `USE SCHEMA`, permisos para crear modelo/versiones y para cambiar su alias. No se configura Model Serving.
9. Comparta el notebook con el docente mediante Share y copie su URL real. Guarde evidencia de ambos formatos, actualice README y reporte con ese enlace y suba el notebook ejecutado a GitHub. Confirme que el docente tenga acceso: conocer una URL no concede permisos.

Para automatización, cree después un Job con tarea Python script y los mismos argumentos. Instale el paquete y dependencias en el entorno del Job; las bibliotecas del notebook no se heredan automáticamente.

## MLflow y CRISP-DM

Experiments agrupa ejecuciones; Tracking registra parámetros, métricas, datasets y artefactos; Models conserva el pipeline reutilizable. Model Registry añade versiones y alias, y Unity Catalog su gobierno en Databricks. La comprensión del negocio y de los datos se documenta en notas y artefactos; la preparación se encapsula en el pipeline; modelado y evaluación se rastrean directamente. El despliegue requiere configurar servicios adicionales. El desarrollo y las referencias están en el [reporte](reporte/MLflow_Databricks.pdf).

## Resultados y validación

Las cifras SVC 0.638 (F1 macro CV), 0.655 (accuracy prueba) y 0.601 (F1 macro prueba), junto con las de otras familias del reporte, **proceden del Taller 3 original, página 10**. No corresponden a una ejecución nueva ni a Databricks. El notebook histórico conserva sus salidas originales identificadas como referencia.

Véase [VALIDACION_LOCAL.md](VALIDACION_LOCAL.md) para lo ejecutado en esta adaptación. Las pruebas cortas no reproducen la comparación completa del taller.

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m build
```

El PDF se regenera desde la raíz con `tectonic -o reporte reporte/MLflow_Databricks.tex` (requiere Tectonic; la primera compilación puede descargar paquetes TeX).

Fuentes oficiales: [MLflow en Databricks](https://docs.databricks.com/aws/en/mlflow/), [Tracking](https://docs.databricks.com/aws/en/mlflow/tracking), [Models en Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/) y [API scikit-learn de MLflow](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.sklearn.html).
