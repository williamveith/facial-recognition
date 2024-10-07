import numpy as np
import json
from image_handler import get_image_files
from pathlib import Path
from represent_faces import get_vector

def cosine_distance(A, B):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    cosine_similarity = dot_product / (norm_A * norm_B)
    return 1 - cosine_similarity

# Function to load embeddings from .npy files
def load_embedding(embedding_path):
    return np.load(embedding_path)

# Example usage:
metadata_file = "database/metadata.json"
image_path = "testing/query_image.png"
embeddings_folder = "database/embeddings"

# Get the image file to process
image = get_image_files(image_path)[0]
results = get_vector(image)

# Load metadata
with open(metadata_file) as file:
    data = json.load(file)
    saved_images = data["images"]

# Initialize the list to hold distances
distances = [None] * len(saved_images)

# Iterate through the saved images and calculate cosine distance
for index, saved_image in enumerate(saved_images):
    embedding_path = saved_image["embedding_path"]
    saved_embedding = load_embedding(embedding_path)
    distances[index] = cosine_distance(results[0]["embedding"], saved_embedding)
    
# Find the index of the closest image
closest_image_index = distances.index(min(distances))
person = saved_images[closest_image_index]["label"]
image_file_name = Path(saved_images[closest_image_index]["image_path"]).name

import os
os.system('cls||clear')
print(f"Closest match: {person} with distance {distances[closest_image_index]}, file: {image_file_name}")
