"""Champions League con MLflow local o Databricks.

Adaptado del ZIP proporcionado y del Taller 3 de Diego Linares, Andy Fuentes,
Diederich Solís y Christian Echeverria: https://github.com/DiegoLinares11/MLFlow.
Instalar este proyecto antes de ejecutar: python -m pip install -e .
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


# Permite importar el paquete fuente tras reiniciar Python o al ejecutar con runpy.
_RUTA_SRC = str(Path(__file__).resolve().parent / "src")
if _RUTA_SRC not in sys.path:
    sys.path.insert(0, _RUTA_SRC)


def ejecutar(experimento, familia='svc', n_iter=40, folds=5, modelo_uc=None,
             uri='databricks', formato='python'):
    import mlflow
    import mlflow.sklearn
    import numpy as np
    import pandas as pd
    import sklearn
    from mlflow import MlflowClient
    from sklearn.metrics import f1_score
    from taller3_pipeline.data import cargar_datos
    from taller3_pipeline.modelos import FAMILIAS
    from taller3_pipeline.pipeline import SEED
    from taller3_pipeline.seguimiento import (
        configurar_mlflow, entrenar_familia, ruta_del_csv,
    )

    if familia not in FAMILIAS:
        raise ValueError(f'Familia inválida. Opciones: {list(FAMILIAS)}')
    if not experimento.strip() or not uri.strip():
        raise ValueError('Configure experimento y URI de seguimiento.')
    if uri == 'databricks' and not experimento.startswith('/'):
        raise ValueError('Databricks requiere una ruta absoluta de experimento.')
    _, X_test, y_train, y_test = cargar_datos(seed=SEED)
    if n_iter < 1 or not 2 <= folds <= int(y_train.value_counts().min()):
        raise ValueError('n_iter debe ser positivo y folds entre 2 y la clase menor de entrenamiento.')
    if modelo_uc and (uri != 'databricks' or len(modelo_uc.split('.')) != 3
                      or not all(modelo_uc.split('.'))):
        raise ValueError('Unity Catalog requiere uri=databricks y catalogo.esquema.modelo.')
    if mlflow.active_run() is not None:
        raise RuntimeError('Finalice el run activo antes de ejecutar este punto de entrada.')

    configurar_mlflow(experimento=experimento, uri=uri)
    # Evita runs duplicados en computes que activan autolog automáticamente.
    mlflow.sklearn.autolog(disable=True)
    resultado = entrenar_familia(familia, n_iter=n_iter, folds=folds, n_jobs=1)
    with mlflow.start_run(run_id=resultado['run_id']):
        mlflow.set_tags({
            'formato': formato,
            'entorno': 'databricks' if uri == 'databricks' else 'local',
            'repositorio': 'https://github.com/Andyfer004/Ejercicio5-MLOPS',
            'origen_pipeline': 'https://github.com/DiegoLinares11/MLFlow',
        })
        recargado = mlflow.sklearn.load_model(resultado['model_uri'])
        predicciones = recargado.predict(X_test)
        f1_recargado = float(f1_score(y_test, predicciones, average='macro'))
        np.testing.assert_allclose(f1_recargado, resultado['metricas']['test_f1_macro'])
        mlflow.log_dict({
            'model_reload_verified': True,
            'test_rows': len(X_test),
            'reloaded_test_f1_macro': f1_recargado,
            'dataset_sha256': hashlib.sha256(Path(ruta_del_csv()).read_bytes()).hexdigest(),
            'mlflow_version': mlflow.__version__,
            'sklearn_version': sklearn.__version__,
            'pandas_version': pd.__version__,
        }, 'evaluacion/verificacion_recarga.json')
    resultado['recarga_verificada'] = True
    if modelo_uc:
        mlflow.set_registry_uri('databricks-uc')
        version = mlflow.register_model(resultado['model_uri'], modelo_uc)
        MlflowClient().set_registered_model_alias(modelo_uc, 'campeon', str(version.version))
        resultado['modelo_uc'] = modelo_uc
        resultado['version_uc'] = str(version.version)
    print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))
    return resultado


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experimento', required=True)
    parser.add_argument('--familia', default='svc')
    parser.add_argument('--n-iter', type=int, default=40)
    parser.add_argument('--folds', type=int, default=5)
    parser.add_argument('--modelo-uc', default=None)
    parser.add_argument('--uri', default='databricks', help='databricks o URI local explícita')
    args = parser.parse_args()
    ejecutar(args.experimento, args.familia, args.n_iter, args.folds,
             args.modelo_uc, uri=args.uri)
