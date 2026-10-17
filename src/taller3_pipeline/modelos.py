"""Familias de modelos que se comparan en el taller.

Son las mismas cuatro de la Actividad 9, con los mismos espacios de búsqueda.
Allá cada familia era un *plugin* (entry point); aquí basta un diccionario,
porque lo que interesa es cómo MLflow registra cada búsqueda.

Cada familia devuelve:

``estimador``
    Un clasificador de scikit-learn sin entrenar.
``espacio``
    Hiperparámetros para ``RandomizedSearchCV``, con los nombres propios del
    estimador. ``espacio_del_pipeline`` les agrega el prefijo ``modelo__``
    para ubicarlos dentro del pipeline.
"""

from __future__ import annotations

from scipy.stats import loguniform, randint, uniform
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from .pipeline import SEED


def random_forest() -> dict:
    """Bosque aleatorio: ``max_depth`` y ``min_samples_leaf`` frenan el sobreajuste."""
    return {
        "estimador": RandomForestClassifier(random_state=SEED),
        "espacio": {
            "n_estimators": randint(100, 600),
            "max_depth": [None, 4, 6, 10, 16],
            "min_samples_leaf": randint(1, 6),
            "max_features": ["sqrt", "log2", None],
            "class_weight": [None, "balanced"],
        },
    }


def regresion_logistica() -> dict:
    """Regresión logística: ``C`` se busca en escala logarítmica."""
    return {
        "estimador": LogisticRegression(max_iter=5000, random_state=SEED),
        "espacio": {
            "C": loguniform(1e-3, 1e2),
            "class_weight": [None, "balanced"],
        },
    }


def svc() -> dict:
    """Máquina de vectores de soporte: ``C`` y ``gamma`` se compensan entre sí."""
    return {
        "estimador": SVC(random_state=SEED),
        "espacio": {
            "C": loguniform(1e-2, 1e2),
            "gamma": loguniform(1e-4, 1e0),
            "kernel": ["rbf", "linear"],
            "class_weight": [None, "balanced"],
        },
    }


def hist_gradient_boosting() -> dict:
    """Gradient boosting por histogramas: ``learning_rate`` y ``max_iter`` van juntos."""
    return {
        "estimador": HistGradientBoostingClassifier(random_state=SEED),
        "espacio": {
            "learning_rate": uniform(0.02, 0.28),
            "max_iter": randint(80, 400),
            "max_leaf_nodes": [7, 15, 31],
            "min_samples_leaf": randint(5, 25),
        },
    }


FAMILIAS = {
    "random_forest": random_forest,
    "regresion_logistica": regresion_logistica,
    "svc": svc,
    "hist_gradient_boosting": hist_gradient_boosting,
}


def espacio_del_pipeline(espacio: dict) -> dict:
    """Agrega el prefijo ``modelo__`` para que la búsqueda ajuste el paso ``modelo``."""
    return {f"modelo__{nombre}": valores for nombre, valores in espacio.items()}
