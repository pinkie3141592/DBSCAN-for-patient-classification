ESTO PROYECTO UTILIZO UN CODIGO GENERADO CON AYUDA DE IA.
EL ANALISIS DE CLASIFICACION Y  AGRUPAMIENTO FUERON HECHOS POR EL DEV.

# DBSCAN Clustering Analysis

Este proyecto implementa un flujo completo de análisis de clustering utilizando **DBSCAN** sobre un dataset tabular.

IMPORTANTE: Asegurate de cambiar la ruta del archivo .csv antes de correr el script. Esto debe encontrarse en la variable path.

## Funcionalidades

- Lectura de datos desde archivo `.csv`
- Preprocesamiento:
  - Estandarización con `StandardScaler`
- Clustering con:
  - Algoritmo **DBSCAN**
- Evaluación:
  - Cálculo de **Silhouette Score**
- Reducción de dimensionalidad:
  - PCA a 2 componentes para visualización
- Generación de reporte:
  - Exporta estadísticas por cluster (media, desviación estándar, Q1, Q3)
- Visualización:
  - Gráfica de clusters con centroides

---

## Salidas del programa

1. **Consola:**
   - Clusters encontrados
   - Número de clusters (sin ruido)
   - Conteo de elementos por cluster
   - Silhouette Score

2. **Archivo generado:**
   - `cluster_report.txt`
   - Contiene estadísticas detalladas por cluster

3. **Gráfica:**
   - Representación en 2D usando PCA
   - Centroides marcados con estrellas
   - Identificación visual de clusters

---

## Parámetros importantes

```python
eps_value = 0.9
min_samples_value = 2
