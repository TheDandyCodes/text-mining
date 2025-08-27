from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from umap import UMAP


def kmeans_pipeline(tf_vectors, n_clusters: int = 7):
    # vectors are normalized with L2
    # This implies that minimizing the Euclidean distance
    # between normalized vectors is equivalent to maximizing
    # cosine similarity, i.e., the two measures order
    # the vector pairs in the same way.
    umap = UMAP(n_components=300, random_state=42, metric="cosine")

    # Create a normalizer that will apply L2 normalization after UMAP
    normalizer = Normalizer(norm="l2")

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)

    # Create pipeline: UMAP -> L2 normalization -> KMeans
    pipeline = make_pipeline(umap, normalizer, kmeans)
    pipeline.fit(tf_vectors)

    cluster_labels = pipeline.named_steps["kmeans"].labels_

    return cluster_labels
