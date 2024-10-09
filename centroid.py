import numpy as np
import json
from image_handler import get_image_files
from pathlib import Path
from represent_faces import get_vector

"""
Closest match: Hunter Boon with distance 0.39313323365644914, file: 4.png
"""

def cosine_distance(A, B):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    cosine_similarity = dot_product / (norm_A * norm_B)
    return 1 - cosine_similarity

# Function to load embeddings from .npy files
def load_embedding(embedding_path):
    return np.load(embedding_path)

# Function to normalize vectors (unit norm for cosine similarity)
def normalize(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

# Function to calculate the centroid (average embedding) for a person
def calculate_centroid(embeddings):
    return np.mean(embeddings, axis=0)

# Example usage:
metadata_file = "database/metadata.json"
image_path = "testing/query_image.png"
embeddings_folder = "database/embeddings"

# Get the image file to process
image = get_image_files(image_path)[0]
query_vector = get_vector(image)[0]["embedding"]

# Normalize the query vector
query_vector = query_vector / np.linalg.norm(query_vector)

# Load metadata
with open(metadata_file) as file:
    data = json.load(file)
    saved_images = data["images"]

# Organize embeddings by person
person_embeddings = {}
for saved_image in saved_images:
    label = saved_image["label"]
    embedding_path = saved_image["embedding_path"]
    embedding = load_embedding(embedding_path)
    
    if label not in person_embeddings:
        person_embeddings[label] = []
    person_embeddings[label].append(embedding)

# Calculate centroids for each person
person_centroids = {}
for person, embeddings in person_embeddings.items():
    embeddings = np.array(embeddings)  # Convert to numpy array
    embeddings = normalize(embeddings)  # Normalize the embeddings
    person_centroids[person] = calculate_centroid(embeddings)  # Calculate centroid

# Initialize the list to hold distances
distances = {}

# Iterate through the person centroids and calculate cosine distance to query
for person, centroid in person_centroids.items():
    distances[person] = cosine_distance(query_vector, centroid)

# Find the person with the closest centroid
closest_person = min(distances, key=distances.get)
closest_distance = distances[closest_person]

# Find the corresponding image for the closest match
closest_image = None
for saved_image in saved_images:
    if saved_image["label"] == closest_person:
        closest_image = saved_image["image_path"]
        break

# Output result
import os
os.system('cls||clear')
print(f"Closest match: {closest_person} with distance {closest_distance}, file: {Path(closest_image).name}")
