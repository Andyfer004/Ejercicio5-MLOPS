"""Comandos del paquete (entry points ``console_scripts``).

``taller3-entrenar``
    Calibra una o varias familias y guarda cada una en un run de MLflow. Con
    ``--registrar`` registra la mejor (por F1 macro de validación cruzada) en
    el Model Registry y le pone el alias ``@campeon``. Es el comando que llama
    el ``MLproject`` de la raíz del repositorio (``mlflow run .``).

``taller3-demo``
    Evidencia de ejecución: imprime el equipo, el ambiente y las versiones, y
    corre una búsqueda corta con registro en MLflow. Basta con tomarle una
    captura de pantalla.
"""

from __future__ import annotations

import argparse
import sys

from .ambiente import describir_ambiente, describir_equipo
from .modelos import FAMILIAS
from .seguimiento import (
    ALIAS,
    EXPERIMENTO,
    MODELO_REGISTRADO,
    asignar_alias,
    configurar_mlflow,
    entrenar_familia,
    servidor_disponible,
    uri_de_seguimiento,
)


def _sin_servidor(uri: str) -> int:
    print(f"\n[ERROR] No responde el servidor de MLflow en {uri}.")
    print("Levántalo en otra terminal, desde la carpeta del repositorio:")
    print("    mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 8080")
    print("o usa una base local sin servidor:  --uri sqlite:///mlflow.db")
    return 1


def _tabla(resultados: list[dict]) -> None:
    print(f"\n{'familia':<24}{'CV F1 macro':>12}{'test acc':>10}{'test F1':>10}  run_id")
    for r in sorted(resultados, key=lambda r: -r["metricas"]["cv_f1_macro"]):
        m = r["metricas"]
        print(f"{r['familia']:<24}{m['cv_f1_macro']:>12.3f}{m['test_accuracy']:>10.3f}{m['test_f1_macro']:>10.3f}  {r['run_id']}")


def entrenar(argv: list[str] | None = None, prog: str = "taller3-entrenar") -> int:
    parser = argparse.ArgumentParser(prog=prog, description="Calibra familias de modelos y las registra en MLflow.")
    parser.add_argument("--familia", default="todas", help=f"todas o una de: {', '.join(FAMILIAS)}")
    parser.add_argument("--n-iter", type=int, default=40, help="combinaciones por familia (RandomizedSearchCV)")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--n-jobs", type=int, default=-1)
    parser.add_argument("--experimento", default=EXPERIMENTO)
    parser.add_argument("--uri", default=None, help="servidor de MLflow (por defecto MLFLOW_TRACKING_URI o http://127.0.0.1:8080)")
    parser.add_argument("--registrar", action="store_true", help=f"registra la mejor como {MODELO_REGISTRADO}@{ALIAS}")
    args = parser.parse_args(argv)

    familias = list(FAMILIAS) if args.familia == "todas" else [args.familia]
    desconocidas = [f for f in familias if f not in FAMILIAS]
    if desconocidas:
        parser.error(f"familia desconocida: {', '.join(desconocidas)}")
    uri = uri_de_seguimiento(args.uri)
    if not servidor_disponible(uri):
        return _sin_servidor(uri)

    import mlflow

    configurar_mlflow(args.experimento, uri)
    print(f"MLflow: {uri} · experimento {args.experimento}")
    resultados = []
    # Con varias familias se abre un run padre y cada familia queda como run hijo.
    # Si el comando lo lanza `mlflow run`, start_run retoma el run del proyecto.
    abri_padre = len(familias) > 1 and mlflow.active_run() is None
    if abri_padre:
        mlflow.start_run(run_name="comparacion-familias")
    try:
        for familia in familias:
            print(f"  calibrando {familia} ({args.n_iter} combinaciones)...")
            resultados.append(entrenar_familia(familia, n_iter=args.n_iter, folds=args.folds, n_jobs=args.n_jobs))
        _tabla(resultados)
        if args.registrar:
            mejor = max(resultados, key=lambda r: r["metricas"]["cv_f1_macro"])
            version = mlflow.register_model(mejor["model_uri"], MODELO_REGISTRADO).version
            asignar_alias(version)
            print(f"\nRegistrado: {MODELO_REGISTRADO} v{version} ({mejor['familia']}) -> alias @{ALIAS}")
    finally:
        if abri_padre:
            mlflow.end_run()
    return 0


def demo(argv: list[str] | None = None, prog: str = "taller3-demo") -> int:
    parser = argparse.ArgumentParser(prog=prog, description="Evidencia de ejecución con MLflow.")
    parser.add_argument("--uri", default=None)
    parser.add_argument("--n-iter", type=int, default=10)
    # Un solo proceso: la búsqueda de la demo es corta y así no depende de que joblib
    # pueda lanzar procesos en paralelo (en algunas terminales de Windows falla).
    parser.add_argument("--n-jobs", type=int, default=1)
    args = parser.parse_args(argv)

    import mlflow
    import sklearn

    print("=" * 72)
    print("TALLER 3 - MLflow con un pipeline de scikit-learn (UEFA Champions League)")
    print("=" * 72)
    equipo, ambiente = describir_equipo(), describir_ambiente()
    print(f"Equipo      : {equipo['hostname']} · {equipo['sistema']} · {equipo['fecha']}")
    print(f"Ambiente    : {ambiente['tipo']} '{ambiente['nombre']}' · Python {ambiente['python']}")
    print(f"Versiones   : mlflow {mlflow.__version__} · scikit-learn {sklearn.__version__}")
    uri = uri_de_seguimiento(args.uri)
    print(f"Seguimiento : {uri}")
    if not servidor_disponible(uri):
        return _sin_servidor(uri)

    configurar_mlflow("Taller3_Demo", uri)
    r = entrenar_familia("random_forest", n_iter=args.n_iter, n_jobs=args.n_jobs, nombre_run=f"demo-{equipo['hostname']}")
    _tabla([r])
    if uri.startswith("http"):
        experimento = mlflow.get_experiment_by_name("Taller3_Demo").experiment_id
        print(f"\nVer el run: {uri}/#/experiments/{experimento}/runs/{r['run_id']}")
    print("\n[OK] El pipeline se entrenó y quedó registrado en MLflow desde este equipo.")
    return 0


def main_entrenar() -> None:
    sys.exit(entrenar())


def main_demo() -> None:
    sys.exit(demo())
