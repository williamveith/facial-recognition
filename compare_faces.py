from deepface import DeepFace
from image_handler import get_image_files, pairwise_comparison
import json

def compare_faces(img1_path, img2_path, detector_backend="retinaface", model_name='ArcFace', distance_metric="cosine", enforce_detection=True):
    try:
        return DeepFace.verify(
            img1_path, img2_path, 
            model_name=model_name,
            distance_metric=distance_metric,
            detector_backend=detector_backend, 
            enforce_detection=enforce_detection
        )
        
    except Exception as e:
        return f"Error: {str(e)}"

images = get_image_files("/Users/main/Projects/Docker/faces/test_images")

results = pairwise_comparison(images, compare_faces)
print(json.dumps(results, indent=4, sort_keys=True))
