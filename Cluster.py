from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans


def clusterWords(words: [str], num_clusters: str = 10) -> [[str]]:
    embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    words_embeddings = embedder.encode(words)

    # Perform kmean clustering
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(words_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for _ in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(words[sentence_id])

    return clustered_sentences
