
import os
import numpy as np
import json
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam

LR_DIR = "/music-categorizer-data/lr-generator"
MODEL_DIR = "/music-categorizer-data/model"
AUTOENCODER_PATH = os.path.join(MODEL_DIR, "autoencoder.keras")
EMBEDDINGS_PATH = os.path.join(MODEL_DIR, "song_embeddings.json")
NUM_CLUSTERS = 10
ENCODING_DIM = 10

os.makedirs(MODEL_DIR, exist_ok=True)


def load_song_vectors():
    data = []
    for filename in os.listdir(LR_DIR):
        if filename.endswith(".csv") and filename.startswith("lr_"):
            path = os.path.join(LR_DIR, filename)
            try:
                matrix = np.loadtxt(path, delimiter=",")
                song_id = filename.replace("lr_", "").replace(".csv", "")
                vector = np.mean(matrix, axis=0)
                data.append((song_id, vector))
            except Exception as e:
                print(f"[!] Failed to load {filename}: {e}")
    return data


def build_autoencoder(input_dim, encoding_dim):
    inp = Input(shape=(input_dim,))
    encoded = Dense(32, activation='relu')(inp)
    encoded = Dense(encoding_dim, activation='relu')(encoded)
    decoded = Dense(32, activation='relu')(encoded)
    out = Dense(input_dim, activation='linear')(decoded)
    autoencoder = Model(inp, out)
    encoder = Model(inp, encoded)
    autoencoder.compile(optimizer=Adam(0.001), loss='mse')
    return autoencoder, encoder


def train_autoencoder(vectors):
    input_dim = vectors.shape[1]
    autoencoder, encoder = build_autoencoder(input_dim, ENCODING_DIM)
    autoencoder.fit(vectors, vectors, epochs=50, batch_size=8, verbose=1)
    autoencoder.save(AUTOENCODER_PATH)
    return encoder


def cluster_embeddings(encoder, song_data):
    ids = [s[0] for s in song_data] 
    vectors = np.array([s[1] for s in song_data])
    embeddings = encoder.predict(vectors)
    num_clusters = NUM_CLUSTERS
    if len(song_data) < NUM_CLUSTERS:
        print(f"[!] Not enough songs ({len(song_data)}) for {NUM_CLUSTERS} clusters. Adjusting to {len(song_data)}.")
        num_clusters = len(song_data)
    model = KMeans(n_clusters=num_clusters, random_state=42)
    labels = model.fit_predict(embeddings)

    db = []
    for i in range(len(ids)):
        db.append({
            "id": ids[i],
            "embedding": embeddings[i].tolist(),
            "cluster": int(labels[i])
        })

    with open(EMBEDDINGS_PATH, "w") as f:
        json.dump(db, f, indent=2)
    print(f"[+] Saved clustered embeddings for {len(db)} songs.")


def recommend(song_id, top_k=5):
    if not os.path.exists(EMBEDDINGS_PATH):
        print("[-] No embeddings found. Run with --train first.")
        return []
    with open(EMBEDDINGS_PATH, "r") as f:
        db = json.load(f)
    target = next((s for s in db if s["id"] == song_id), None)
    if not target:
        print(f"[-] Song ID '{song_id}' not found.")
        return []

    cluster = target["cluster"]
    same_cluster = [s for s in db if s["cluster"] == cluster and s["id"] != song_id]
    if not same_cluster:
        return []

    sims = cosine_similarity([target["embedding"]], [s["embedding"] for s in same_cluster])[0]
    ranked = np.argsort(sims)[::-1][:top_k]
    return [(same_cluster[i]["id"], sims[i]) for i in ranked]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true", help="Train autoencoder and cluster embeddings")
    parser.add_argument("--recommend", type=str, help="Recommend similar songs by embedding")
    parser.add_argument("--topk", type=int, default=5)
    args = parser.parse_args()

    if args.train:
        data = load_song_vectors()
        if not data:
            print("[-] No data found.")
            exit(1)
        vectors = np.array([v[1] for v in data])
        encoder = train_autoencoder(vectors)
        cluster_embeddings(encoder, data)

    elif args.recommend:
        results = recommend(args.recommend, args.topk)
        if results:
            print(f"Top {args.topk} recommendations for '{args.recommend}':")
            for i, (sid, score) in enumerate(results):
                print(f" {i+1}. {sid} (similarity: {score:.3f})")
        else:
            print("No recommendations found.")
    else:
        parser.print_help()
