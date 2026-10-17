# Guía de ejecución y cierre

El laboratorio ya fue ejecutado por el usuario en ambos formatos en Databricks. La evidencia recibida se publica en [VALIDACION_DATABRICKS.md](VALIDACION_DATABRICKS.md) y [reporte/evidencias/](reporte/evidencias/). Durante este cierre no se volvió a entrenar en Databricks ni se modificaron sus permisos.

## Consultar los entregables

- [Repositorio](https://github.com/Andyfer004/Ejercicio5-MLOPS).
- [Notebook real en Databricks](https://dbc-5490c6a5-5215.cloud.databricks.com/editor/notebooks/2665096834519332?o=7474655525361249).
- [Notebook en GitHub](notebooks/Champions_Databricks.ipynb), [script](pipeline_champions_databricks.py) y [PDF final](reporte/MLflow_Databricks.pdf).
- [JSON recibido](reporte/evidencias/resultados_databricks.json) y capturas de configuración y resultado del notebook en la misma carpeta.

## Configuración reproducible

La configuración publicada es `URI="databricks"`, `EXPERIMENTO="/Users/fue22944@uvg.edu.gt/Champions_Resultado_Databricks"`, `FAMILIA="svc"`, `N_ITER=40`, `FOLDS=5`, `MODELO_UC=None`.

El notebook detecta la raíz desde su ubicación conocida y el directorio actual, y añade raíz y `src/` a `sys.path`. Si serverless usa otro directorio, configure `RUTA_WORKSPACE` con la ruta absoluta real del Git folder. Ejecute esa celda después de cada reinicio de Python; la importación no depende de que sobreviva la instalación editable. Las dependencias externas sí deben existir en el entorno.

El archivo `.py` se ejecutó desde una celda con `runpy.run_path(..., run_name="__main__")`, conservando/restaurando `sys.argv`. No fue un Job independiente. La celda `runpy` está incluida sin salidas inventadas; repetirla deliberadamente crearía un run distinto. Los modelos se guardaron con MLflow Models y `version=null`, sin versión en Unity Catalog, sin alias nuevo ni endpoint.

Para ejecutar en local, seleccione explícitamente SQLite y un experimento local antes de entrenar; consulte [README](README.md#ejecutar-el-jupyter-notebook-localmente). Una prueba local no constituye una nueva validación de Databricks.

## Procedencia y entrega

No se recibió un notebook ejecutado exportado ni estaba incorporado en el remoto al iniciar el cierre. Se conservan las celdas existentes, se corrigen rutas/configuración y se documentan los resultados en Markdown/JSON. Los contadores y salidas del notebook de entrega siguen vacíos. Las capturas son las suministradas por el usuario; no se generaron logs ni capturas adicionales.

Entregables: PDF final, enlace de GitHub y enlace real del notebook. Los enlaces del workspace mantienen sus permisos existentes. El reporte y su fuente final se incorporaron íntegros desde los adjuntos; para recompilar con sus imágenes relativas use `cd reporte && tectonic MLflow_Databricks.tex`.
