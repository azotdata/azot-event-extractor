def meanshift(matrix):
    from sklearn import cluster
    #from sklearn.metrics import silhouette_samples, silhouette_score

    #quantile = [0.09,0.0099,0.005]
    #numbers = []
    #for q in quantile:
    bandwidth = cluster.estimate_bandwidth(matrix, quantile=0.03)
    ms = cluster.MeanShift(bandwidth=bandwidth)
    ms.fit(matrix)
    clusters = ms.labels_
    cluster_centers = ms.cluster_centers_
    #numbers.append(len(cluster_centers))
    #    n_clusters = len(cluster_centers)
    #    silhouette_avg = silhouette_score(dist, clusters)
    #    print("For n_clusters =", n_clusters,
    #      "The average silhouette_score is :", silhouette_avg)
    #logging.info('We actually have %d clusters' %len(cluster_centers))
    return clusters

def determine_clusters(matrix, n_clusters):
    pass

def kmeans(matrix, n_clusters):
    from sklearn import cluster
    from sklearn.metrics import silhouette_samples, silhouette_score

    clusterer = cluster.KMeans(n_clusters=n_clusters)
    cluster_fit = clusterer.fit_predict(matrix)
    cluster_labels = clusterer.labels_
    silhouette_avg = silhouette_score(matrix, cluster_fit)
    
    return cluster_labels


def hierarchical(matrix, label):
    import matplotlib
    #matplotlib.use('agg')
    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import ward, dendrogram, linkage
    from scipy.cluster.hierarchy import cophenet
    from scipy.spatial.distance import pdist


    linkage_matrix = linkage(matrix, 'ward')
    c, coph_dists = cophenet(linkage_matrix, pdist(matrix))

    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('articles')
    plt.ylabel('distance')

    fig, ax = plt.subplots(figsize=(15, 20))
    ax = dendrogram(
        linkage_matrix,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
        orientation="right",
        labels=label
    )
    plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

    plt.tight_layout() #show plot with tight layout

    plt.show()
    #print(linkage_matrix[0])
