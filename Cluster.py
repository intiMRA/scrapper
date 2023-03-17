from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

class Cluster:
    def clusterWords(self, words: [str]):
        embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        words_embeddings = embedder.encode(words)

        # Perform kmean clustering
        num_clusters = 10
        clustering_model = KMeans(n_clusters=num_clusters)
        clustering_model.fit(words_embeddings)
        cluster_assignment = clustering_model.labels_

        clustered_sentences = [[] for i in range(num_clusters)]
        for sentence_id, cluster_id in enumerate(cluster_assignment):
            clustered_sentences[cluster_id].append(words[sentence_id])

        for i, cluster in enumerate(clustered_sentences):
            print("Cluster ", i + 1)
            print(cluster)
            print("")