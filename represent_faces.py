import json
import hashlib
import numpy as np
from pathlib import Path
from deepface import DeepFace
from image_handler import get_image_files

# Function to calculate the sha256 hash of a file
def sha256_hash(file):
    sha256 = hashlib.sha256()
    with file.open('rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

# Function to get the vector (embedding) for a given image
def get_vector(img_path, detector_backend="retinaface", model_name="ArcFace", enforce_detection=True):
    try:
        return DeepFace.represent(
            img_path=img_path,
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=enforce_detection,
        )
    except Exception as e:
        return f"Error: {str(e)}"

# Function to save embeddings as .npy files
def save_embedding(embedding, output_path):
    np.save(output_path, embedding)

# Function to store metadata and embeddings
def store_metadata_and_embeddings(images, metadata_output, embeddings_folder):
    database = {
        "params": {"model_name": "ArcFace", "detector_backend": "retinaface"},
        "images": []
    }

    for image in images:
        results = get_vector(image)  # Get embedding from DeepFace
        if isinstance(results, str):
            print(f"Skipping {image}: {results}")
            continue
        
        embedding = results[0]["embedding"]
        image_hash = sha256_hash(image)  # Generate hash for the image

        # Save embedding as a .npy file
        embedding_file_path = Path(embeddings_folder) / f"{image_hash}.npy"
        save_embedding(embedding, embedding_file_path)

        # Add metadata for the image
        database["images"].append({
            "label": image.parent.name,
            "image_path": str(image),
            "hash": image_hash,
            "embedding_path": str(embedding_file_path),
            "magnitude": np.linalg.norm(embedding)
        })

    # Save metadata to JSON
    with open(metadata_output, "w+") as file:
        json.dump(database, file, indent=4)

# Example usage: Save metadata and embeddings
images = get_image_files("database/images")
store_metadata_and_embeddings(images, "database/metadata.json", "database/embeddings")
