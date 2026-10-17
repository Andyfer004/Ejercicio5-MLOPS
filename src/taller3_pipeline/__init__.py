"""taller3_pipeline

Paquete del Taller 3 (MLflow): el pipeline de scikit-learn de la Actividad 9
(dataset de la UEFA Champions League del Ejercicio 1) con seguimiento en MLflow,
más el generador de datos sintéticos del tutorial de MLflow y su versión
corregida.

- ``seguimiento``: registro manual de cada búsqueda de hiperparámetros en
  MLflow (parámetros, métricas, datasets, archivos y el modelo), y registro del
  mejor modelo en el Model Registry con el alias ``@campeon``.
- ``manzanas``: generador del tutorial "Your First MLflow Model" y nuestra
  versión con los problemas corregidos.
- ``cli``: comandos ``taller3-entrenar`` y ``taller3-demo``.
"""

from .data import (
    CATEGORICAL_FEATURES,
    FEATURES,
    LEAKAGE_COLUMNS,
    NUMERIC_FEATURES,
    PERCENT_FEATURES,
    RATIO_FEATURES,
    TARGET,
    cargar_datos,
    extraer_datos,
    filtrar_datos,
    separar_datos,
)
from .manzanas import efecto_cosecha, generar_datos_mejorado, generar_datos_tutorial
from .modelos import FAMILIAS, espacio_del_pipeline
from .pipeline import SEED, construir_pipeline, construir_preprocesamiento
from .seguimiento import (
    ALIAS,
    EXPERIMENTO,
    MODELO_REGISTRADO,
    asignar_alias,
    configurar_mlflow,
    dataset_mlflow,
    entrenar_familia,
    servidor_disponible,
)
from .transformers import PorcentajeATexto, RatioATexto

__all__ = [
    "NUMERIC_FEATURES", "PERCENT_FEATURES", "RATIO_FEATURES", "CATEGORICAL_FEATURES",
    "LEAKAGE_COLUMNS", "FEATURES", "TARGET",
    "extraer_datos", "filtrar_datos", "separar_datos", "cargar_datos",
    "SEED", "construir_pipeline", "construir_preprocesamiento", "PorcentajeATexto", "RatioATexto",
    "FAMILIAS", "espacio_del_pipeline",
    "generar_datos_tutorial", "generar_datos_mejorado", "efecto_cosecha",
    "EXPERIMENTO", "MODELO_REGISTRADO", "ALIAS",
    "configurar_mlflow", "servidor_disponible", "dataset_mlflow", "entrenar_familia", "asignar_alias",
]

__version__ = "0.1.0"
