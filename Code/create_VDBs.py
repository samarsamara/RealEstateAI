from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams
from qdrant_client.models import PointStruct
from qdrant_client.http.models import PointStruct
from qdrant_client.http.exceptions import ResponseHandlingException
import pandas as pd

def create_client(collection_name):
    """
    Connecting to Qdrant 
    """
    qdrant_client = QdrantClient(
        url="https://00408636-7100-4931-aaec-7626a00437cc.eu-central-1-0.aws.cloud.qdrant.io:6333",
        api_key="DU1L3IyEuy5m3_6pFj4UaIMao6kAiVc5CgLYrGRpyZ5ClXLMIPRxFg",
    )
    # Define a collection with 1536-dimensional vectors (size of OpenAI embeddings)
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance="Cosine")
    )
    return qdrant_client

def format_key_value_text(row):
    """
    Converts a DataFrame row into a structured text format: "Key: Value".
    If a value is empty or NaN, it remains empty after the colon.
    """
    return ", ".join([f"{col}: {row[col]}" for col in row.index])

def prepare_vectors(df, embeddings):
    """
    Prepare vectors to create the vector database
    """
    points = [
        PointStruct(
            id=row['index'],  # Use the index column as the ID
            vector=row['embeddings'],  # Use the precomputed embedding
            payload={"text": df.loc[row['index'], 'formatted_text']}  # Store the key-value text
        )
        for _, row in embeddings.iterrows()
    ]
    return points

def batch_upsert(client, collection_name, points, batch_size=500):
    """
    Upload points to Qdrant in batches.
    Args:
        client: Qdrant client instance.
        collection_name: Name of the Qdrant collection.
        points: List of PointStruct objects.
        batch_size: Number of points per batch.
    """
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        try:
            client.upsert(collection_name=collection_name, points=batch)
            print(f"Batch {i // batch_size + 1} uploaded successfully.")
        except ResponseHandlingException as e:
            print(f"Error uploading batch {i // batch_size + 1}: {e}")


if __name__ == "__main__":
    df = pd.read_csv("los_angeles.csv")
    df['formatted_text'] = df.apply(format_key_value_text, axis=1)  # Create key-value text

    embeddings = pd.read_parquet("los_angeles_embeddings_final.parquet")
    collection_name = "realestate_ai_final"
    qdrant_client = create_client(collection_name)
    points = prepare_vectors(df, embeddings)
    # Upload in batches
    batch_upsert(qdrant_client, collection_name=collection_name, points=points, batch_size=100)
