from typing import Optional

from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from umap import UMAP


def kmeans_pipeline(vectors, n_components: Optional[int], n_clusters: int = 7):
    # vectors are normalized with L2
    # This implies that minimizing the Euclidean distance
    # between normalized vectors is equivalent to maximizing
    # cosine similarity, i.e., the two measures order
    # the vector pairs in the same way.

    # Create a normalizer that will apply L2 normalization after UMAP
    normalizer = Normalizer(norm="l2")

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)

    # Create pipeline: UMAP (if n_components is not None) -> L2 normalization -> KMeans
    if n_components:
        umap = UMAP(n_components=n_components, random_state=42, metric="cosine")
        pipeline = make_pipeline(umap, normalizer, kmeans)
    else:
        pipeline = make_pipeline(normalizer, kmeans)
    pipeline.fit(vectors)

    cluster_labels = pipeline.named_steps["kmeans"].labels_

    return cluster_labels
