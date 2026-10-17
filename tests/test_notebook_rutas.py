"""Regresión de importaciones tras reiniciar Python, sin ejecutar Databricks."""
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'notebooks/Champions_Databricks.ipynb'


def _code_with(text):
    nb = json.loads(NOTEBOOK.read_text())
    return next(''.join(c['source']) for c in nb['cells']
                if c['cell_type'] == 'code' and text in ''.join(c['source']))


@pytest.mark.parametrize('origen', ['directorio', 'ubicacion_notebook', 'workspace_explicito'])
def test_importar_sin_instalacion_editable(tmp_path, origen):
    source = _code_with('RUTA_WORKSPACE =')
    if origen == 'workspace_explicito':
        source = source.replace('RUTA_WORKSPACE = ""', f'RUTA_WORKSPACE = {str(ROOT)!r}')
    # Quita los atajos del paquete editable para reproducir la importación fallida.
    # El resto de dependencias sí está instalado en el entorno de prueba.
    programa = '''import sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path[:] = [p for p in sys.path if p not in (str(root), str(root / 'src'))]
sys.meta_path[:] = [f for f in sys.meta_path
                   if not getattr(f, '__module__', '').startswith('__editable__')]
namespace = {}
if sys.argv[3] == 'ubicacion_notebook':
    namespace['__vsc_ipynb_file__'] = str(root / 'notebooks' / 'Champions_Databricks.ipynb')
exec(sys.argv[2], namespace)
assert namespace['RAIZ'] == root
assert str(root) in sys.path and str(root / 'src') in sys.path
from taller3_pipeline.data import cargar_datos
assert tuple(map(len, cargar_datos())) == (115, 29, 115, 29)
'''
    subprocess.run([sys.executable, '-I', '-c', programa, str(ROOT), source, origen],
                   cwd=ROOT / 'notebooks' if origen == 'directorio' else tmp_path,
                   check=True, capture_output=True, text=True, timeout=60)


def test_runpy_main_y_restauracion_de_argumentos():
    source = _code_with('runpy.run_path')
    original = sys.argv[:]
    configuracion = dict(RAIZ=ROOT, URI='databricks',
                         EXPERIMENTO='/Users/fue22944@uvg.edu.gt/Champions_Resultado_Databricks',
                         FAMILIA='svc', N_ITER=40, FOLDS=5)
    def revisar(path, run_name):
        assert Path(path) == ROOT / 'pipeline_champions_databricks.py'
        assert run_name == '__main__'
        assert sys.argv[1:] == ['--uri', 'databricks', '--experimento', configuracion['EXPERIMENTO'],
                                '--familia', 'svc', '--n-iter', '40', '--folds', '5']
    # Solo comprueba el cableado: no ejecuta el script ni contacta Databricks.
    with patch('runpy.run_path', side_effect=revisar) as llamada:
        exec(source, configuracion)
        llamada.assert_called_once()
    assert sys.argv == original
