# Guía de ejecución y entrega

Esta guía adapta la del ZIP recibido. Las instrucciones vigentes de instalación, notebook y archivo Python están en [README.md](README.md#ejecutar-ambos-formatos-en-databricks).

1. Utilice en Databricks el Git folder de **https://github.com/Andyfer004/Ejercicio5-MLOPS.git** y abra `notebooks/Champions_Databricks.ipynb`.
2. Instale este paquete desde la raíz real del workspace y reinicie Python antes de las importaciones si se solicita. Las dependencias se declaran en `pyproject.toml`; el CSV está incluido en el paquete.
3. Configure `URI = "databricks"`, una ruta real de experimento y una prueba de 2 iteraciones / 3 folds. Luego ejecute con 40 / 5 para la búsqueda completa.
4. Ejecute también el script raíz con el bloque `runpy` del README. Esto usa su punto de entrada y registra un run con `formato=python`; el notebook registra `formato=notebook`.
5. Compruebe Experiments, Tracking y el MLflow Model. Debe existir el artefacto `evaluacion/verificacion_recarga.json` con `model_reload_verified: true`. Unity Catalog es opcional y requiere los permisos indicados en el README.
6. Guarde capturas de ambos runs, sus parámetros, métricas y modelo. Exporte el notebook ejecutado sin credenciales y actualice el archivo de `notebooks/`.
7. Comparta el notebook con el docente, copie el enlace real y agréguelo al README y a la sección 5 de `reporte/MLflow_Databricks.tex`. Recompile el PDF con Tectonic y revise su presentación.
8. Revise `git diff` y publique los nuevos entregables en este repositorio. Entregue el PDF, el enlace de GitHub y el enlace real de Databricks. Canva ya está preparado.

No se ha establecido conexión con Databricks en esta preparación. Las métricas históricas del PDF y del notebook de referencia son del Taller 3, no de Databricks. No las sustituya por resultados de una prueba corta ni declare ejecuciones que aún no realizó.
