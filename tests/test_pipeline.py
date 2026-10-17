"""Pruebas de integración locales: datos, tracking y modelos serializados reales."""
import json

import mlflow
import numpy as np
import pytest
from mlflow import MlflowClient
from sklearn.metrics import f1_score

from pipeline_champions_databricks import ejecutar
from taller3_pipeline.data import FEATURES, cargar_datos, extraer_datos, filtrar_datos
from taller3_pipeline.modelos import FAMILIAS


def test_dataset_y_particion():
    raw = extraer_datos()
    clean = filtrar_datos(raw)
    X_train, X_test, y_train, y_test = cargar_datos()
    assert (len(raw), len(clean), len(X_train), len(X_test)) == (151, 144, 115, 29)
    assert clean['result'].value_counts().to_dict() == {'Home Win': 71, 'Away Win': 48, 'Draw': 25}
    assert list(X_train.columns) == FEATURES
    assert {'score', 'winner', 'result'}.isdisjoint(X_train.columns)
    assert set(X_train.index).isdisjoint(X_test.index)
    assert set(y_train) == set(y_test) == {'Home Win', 'Away Win', 'Draw'}


@pytest.mark.parametrize('familia', list(FAMILIAS))
def test_tracking_modelo_y_recarga(tmp_path, familia, monkeypatch):
    # SQLite y artefactos aislados; nunca conecta a Databricks.
    monkeypatch.chdir(tmp_path)
    uri = 'sqlite:///' + str(tmp_path / 'tracking.db')
    r = ejecutar('Prueba_Local', familia=familia, n_iter=1, folds=2, uri=uri)
    client = MlflowClient(tracking_uri=uri)
    run = client.get_run(r['run_id'])
    assert run.info.status == 'FINISHED'
    assert run.data.tags['entorno'] == 'local'
    assert run.data.tags['formato'] == 'python'
    assert run.data.params['cv_folds'] == '2'
    assert len(run.inputs.dataset_inputs) == 2
    assert {d.tags[0].value for d in run.inputs.dataset_inputs} == {'training', 'testing'}
    for metric in ['cv_f1_macro', 'test_accuracy', 'test_f1_macro', 'baseline_test_f1_macro']:
        assert 0 <= run.data.metrics[metric] <= 1
    artifacts = {a.path for a in client.list_artifacts(r['run_id'], 'evaluacion')}
    assert {'evaluacion/matriz_confusion.png', 'evaluacion/reporte.txt',
            'evaluacion/verificacion_recarga.json'} <= artifacts
    path = client.download_artifacts(r['run_id'], 'evaluacion/verificacion_recarga.json')
    assert json.load(open(path))['model_reload_verified'] is True
    assert client.list_artifacts(r['run_id'], 'busqueda')[0].path == 'busqueda/cv_results.csv'
    info = mlflow.models.get_model_info(r['model_uri'])
    assert info.signature is not None
    model = mlflow.sklearn.load_model(r['model_uri'])
    _, X_test, _, y_test = cargar_datos()
    np.testing.assert_allclose(f1_score(y_test, model.predict(X_test), average='macro'),
                               r['metricas']['test_f1_macro'])
