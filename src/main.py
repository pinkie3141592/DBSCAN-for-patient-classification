from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score


def export_cluster_ranges(df, original_names, output_file="cluster_report.txt"):
    
    clusters = sorted(df['cluster'].unique())
    
    with open(output_file, "w", encoding="utf-8") as f:
        
        for cluster_id in clusters:
            
            if cluster_id == -1:
                continue  # excluir ruido
            
            cluster_data = df[df['cluster'] == cluster_id].drop(columns=['cluster', 'var_1'])
            
            size = len(cluster_data)
            f.write("=====================================\n")
            f.write(f"Cluster {cluster_id}  |  Tamano: {size}\n")
            f.write("=====================================\n\n")

            f.write(f"{'Variable':<22}{'Media':>10}{'Std':>10}{'Q1':>10}{'Q3':>10}\n")
            f.write("-" * 62 + "\n")
                        
            means = cluster_data.mean()
            stds = cluster_data.std()
            q1 = cluster_data.quantile(0.25)
            q3 = cluster_data.quantile(0.75)
            
            
            for col in cluster_data.columns:
                
                var_index = int(col.split('_')[1]) - 1
                original_name = original_names[var_index]
                
                f.write(
                    f"{original_name:<22}"
                    f"{means[col]:>10.4f}"
                    f"{stds[col]:>10.4f}"
                    f"{q1[col]:>10.4f}"
                    f"{q3[col]:>10.4f}\n"
                )
    
    print(f"Reporte guardado en: {output_file}")


file_path = r"C:\Users\barba\Desktop\samsung2025\DBSCAN\data\metabolic_synthetic.csv"

df = pd.read_csv(file_path)
original_names = list(df.columns)
df.columns = [f'var_{i+1}' for i in range(len(df.columns))]


X = df[['var_2','var_3','var_4','var_5','var_6','var_7','var_8']]

X_scaled = StandardScaler().fit_transform(X)

#PARAMETROS
####################################################################################################################
eps_value = 0.9
min_samples_value = 2
####################################################################################################################

db = DBSCAN(eps=eps_value, min_samples=min_samples_value).fit(X_scaled)
df['cluster'] = db.labels_

'''print(set(db.labels_))
print(df['cluster'].value_counts())

n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
print("Número de clusters:", n_clusters)'''

labels = db.labels_

unique_clusters = set(labels)
cluster_counts = df['cluster'].value_counts()

n_clusters = len(unique_clusters) - (1 if -1 in labels else 0)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print (
    f"Clusters encontrados: {unique_clusters}\n"
    f"Número de clusters (sin ruido): {n_clusters}\n\n"
    f"{cluster_counts.to_string()}"
)


mask = labels != -1
if len(set(labels[mask])) > 1:
    score = silhouette_score(X_scaled[mask], labels[mask])
    print("Silhouette Score:", score)


clusters = sorted(df['cluster'].unique())


##################################################################################################
export_cluster_ranges(df, original_names, output_file="cluster_report.txt")
##################################################################################################


'''for cluster_id in clusters:
    
    if cluster_id == -1:
        continue   # excluir ruido
    
    cluster_data = df[df['cluster'] == cluster_id].drop(columns=['cluster'])
    
    print(f"\n==============================")
    print(f"Cluster {cluster_id}")
    print(f"==============================")
    
    # Tamaño
    size = len(cluster_data)
    print(f"Tamaño: {size}")
    
    # Media
    print("\nMedia:")
    print(cluster_data.mean())
    
    # Desviación estándar
    print("\nDesviación estándar:")
    print(cluster_data.std())
    
    # Rango intercuartil (Q1–Q3)
    print("\nRango intercuartil (Q1–Q3):")
    q1 = cluster_data.quantile(0.25)
    q3 = cluster_data.quantile(0.75)
    
    iqr_table = np.round(
        np.column_stack((q1, q3)),
        4
    )
    
    for i, col in enumerate(cluster_data.columns):
        print(f"{col}: [{iqr_table[i][0]} , {iqr_table[i][1]}]")'''


#plot

fig, (ax_plot, ax_text) = plt.subplots(
    2, 1,
    figsize=(10,6),
    gridspec_kw={'height_ratios': [3, 1]}
)

unique_clusters_no_noise = [c for c in unique_clusters if c != -1]

for cluster_id in unique_clusters_no_noise:
    cluster_points = X_pca[labels == cluster_id]
    centroid = cluster_points.mean(axis=0)
    
    # Centroide estrellita
    ax_plot.scatter(
        centroid[0],
        centroid[1],
        marker='*',
        s=350,
        edgecolor='black',
        linewidth=1.5
    )
    
    # Etiqueta del cluster
    ax_plot.text(
        centroid[0],
        centroid[1] + 0.15,
        f"Cluster {cluster_id}",
        fontsize=11,
        fontweight='bold',
        ha='center'
    )

ax_plot.scatter(X_pca[:,0], X_pca[:,1], c=labels)
ax_plot.set_xlabel("PC1")
ax_plot.set_ylabel("PC2")
ax_plot.set_title(f"DBSCAN (eps={eps_value}, min_samples={min_samples_value})")

ax_plot.xaxis.set_major_locator(plt.MultipleLocator(0.5))
ax_plot.yaxis.set_major_locator(plt.MultipleLocator(0.5))
ax_plot.grid(True)

info_text = (
    f"Clusters encontrados: {unique_clusters}\n"
    f"Número de clusters (sin ruido): {n_clusters}\n\n"
    f"{cluster_counts.to_string()}\n\n"
    f"Silhouette Score:, {score}"
)

ax_text.axis("off")
ax_text.text(0.01, 0.95, info_text, va='top', fontsize=10)

plt.tight_layout()
plt.show()

